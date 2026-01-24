from dataclasses import dataclass
import itertools
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import threading
import time
from typing import Literal
import schedule
import traceback
import time
import random

from datetime import datetime, UTC
from queue import Queue
from sqlalchemy.exc import IntegrityError

from server.runner_utils import DB, run_runner
from server import runner_utils
from server.crud import crud_tournament, crud_submission, crud_run, crud_submission_run_info, crud_turn, \
    crud_university, crud_team_type
from server.models.submission import Submission
from server.models.tournament import Tournament
from server.schemas.run.run_base import RunBase
from server.schemas.submission_run_info.submission_run_info_base import SubmissionRunInfoBase
from server.schemas.team_type.team_type_base import TeamTypeBase
from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.turn.turn_base import TurnBase
from server.schemas.university.university_base import UniversityBase
from server.server_config import Config
from server.enums import RunnerOptions

# Config for loggers
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class ClientRunner:
    """
    This class is responsible for running submitted client bots against each other and getting the results from the
    games.
    """

    def __init__(self):
        """
        Class variables
        ---------------

            self.config: Creates an instance of the Config class in ``server_config.py``. That file stores values that
            are used by the client_runner and visualizer_runner. Use that file to change the values, and **DO NOT**
            change them in any other file.

            self.total_number_of_games: An int representing the number of games to run during a tournament.

            self.number_of_unique_games: An int representing the unique number of combinations of clients to match them
            against each other.

            self.index_to_seed_id: Maps a seed index to a database seed_id.

            self.job_queues: A list of Queue objects to handle computations in threads. This helps improve the
            performance of running clients against each other. Without this, tournaments would be significantly slower.

            self.version: The version number of the project.

            self.best_run_for_client: A dict that contains the information of the best performance of a client.

            self.runner_temp_dir: A string representing the directory path to place the runner_temp folder.

            self.seed_path: A string representing the directory path used to place the ``seeds`` file in the runner_temp
            folder.

            self.total_number_of_games_for_one_client: An int representing the number of times a client will run against
            the opponents.

            self.tournament: This will either be an int to represent the tournament_id that can be accessed from the
            database, or a Tournament object itself with all the information needed.
        """
        self.config: Config = Config()

        self.total_number_of_games: int = -1

        # IE how many combinations of clients can you make
        self.number_of_unique_games: int = -1

        # Maps a seed_index to a database seed_id
        self.index_to_seed_id: dict[int, int] = {}

        # needs 6 queues for tasks to complete
        self.jobqueues: list[Queue] = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]

        self.version: str = self.get_version_number()

        self.best_run_for_client: dict = {}
        self.runner_temp_dir: str = os.path.join(os.getcwd(), 'server', 'runner_temp')
        self.seed_path: str = os.path.join(self.runner_temp_dir, 'seeds')

        # Number of times a client runs against the opponents
        self.total_number_of_games_per_client: int = 0

        self.tournament: Tournament | Literal[-1] = -1

        # Based on the sleep time specified in ``server_config.py``, this will have the client runner run until the
        # ending date and time of the competition. This code doesn't need to be changed, but the values in
        # ``server_config.py`` will need to be. This also calls the ``external_runner() method``.
        (schedule.every(self.config.SLEEP_TIME_SECONDS_BETWEEN_RUNS)
         .seconds
         .until(self.config.END_DATETIME)
         .do(self.external_runner))
        (schedule.every()
         .day
         .at(self.config.END_DATETIME.split()[-1])
         .do(self.close_server))

        # Creates the Univeristies and Team Types in the database
        self.buffUpData()

        # An infinite loop to keep the schedule object running
        try:
            while 1:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.warning("Ending runner due to Keyboard Interrupt")
        except Exception as e:
            logging.warning("\nEnding runner due to {0}\n{1}\n".format(e, e.args))
            traceback.print_exc()
        finally:
            self.close_server()

    def external_runner(self) -> None:
        """
        This method is extensive and has different steps to it. Print statements help show where the runner is in the
        process.

        #. Step 1: Get the most recent submission for every team that is in the database.
        #. Step 2:
            * a) If there are less than 2 total submissions, end the method; nothing can be done
            * b) Otherwise, proceed to the next step
        #. Step 3: Get all team pairings based on all clients in the database. This will be the pairings for each game.
        #. Step 4: Assign a value to ``self.total_number_of_games_for_one_client`` based on what's returned from the
        ``self.count_number_of_game_appearances()`` method.
        #. Step 5: Insert a new tournament into the database and assign it to ``self.tournament``.
        #. Step 6: Delete all turns from the database. Witihout doing so, the Turns table will continue to accumulate
        data for each new tournament and become very cumbersome.
        #. Step 7: Make the ``runner_temp`` and ``seeds`` folders
        #. Step 8: For the amount of games against the same client specified in ``server_config.py``, run the runner.
        #. Step 9: Run the games in parallel with each other to increase performance.
        :return: None
        """
        print('running')
        self.best_run_for_client = {}
        with DB() as db:
            submissions = crud_submission.get_latest_submission_for_each_team(db)

        if len(submissions) < 1:
            print(f'not enough submissions')
            return

        # get the games as a list of client tuples
        # submission_id_list = list(map(lambda x: x["submission_id"], clients))
        # games: list[Submission] = self.return_team_parings(submissions)
        # NOTE: normally these would be set inside `return_team_parings`
        self.number_of_unique_games = len(submissions)
        self.total_number_of_games = self.number_of_unique_games * self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM

        self.total_number_of_games_per_client = 1 # self.count_number_of_game_appearances(games)
        self.tournament = self.insert_new_tournament()

        self.delete_turns()

        if not os.path.exists(self.runner_temp_dir):
            os.mkdir(self.runner_temp_dir)

        if not os.path.exists(self.seed_path):
            os.mkdir(self.seed_path)

        random.seed(time.time())
        for index in range(self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM):
            path: str = os.path.join(self.seed_path, str(index))
            self.index_to_seed_id[index] = random.randint(0, 1000000000)

        # then run them in parallel using their index as a unique identifier
        assert self.total_number_of_games > 0
        [self.jobqueues[i % 6].put((self.internal_runner, submissions[i], i)) for i in range(self.total_number_of_games)]
        threads: list[threading.Thread] = [
            threading.Thread(target=runner_utils.worker_main, args=(self.jobqueues[i],)) for i in range(6)]
        [t.start() for t in threads]
        [t.join() for t in threads if t.is_alive()]
        self.read_best_logs_and_insert()
        self.delete_runner_temp()
        self.update_tournament_finished()
        self.tournament = -1
        print('Job completed\n')
        logging.info(
            f'Sleeping for {self.config.SLEEP_TIME_SECONDS_BETWEEN_RUNS} seconds')

    def internal_runner(self, submission: Submission, index: int) -> None:
        """
        :param submission_tuple:
        :param index:
        :return:
        """
        logging.info(f'internal runner started for submission {submission.submission_id}')
        score_for_each_submission: dict[int, int] = {}
        results = dict()

        # Run game
        # Create a folder for this client and seed
        end_path = os.path.join(self.runner_temp_dir, str(index))
        if not os.path.exists(end_path):
            os.mkdir(end_path)

        shutil.copy('launcher.pyz', end_path)

        # Write the clients into the folder
        # for index_2, submission in enumerate(submission_tuple):
            # runner will run -fn argument, which makes the file name the file name
            # So we can grab the submission_id out of the results later
        with open(os.path.join(end_path, f'client_{index}_{submission.submission_id}.py'), 'x') as f:
            f.write(str(submission.file_txt, 'utf-8'))

        # Determine what seed this run needs based on it's serial index
        seed_index = index // self.number_of_unique_games
        logging.info(f'generating game map for run {index} for submission (id={submission.submission_id}), using seed index {seed_index}')

        seed = self.index_to_seed_id.get(seed_index)
        assert seed is not None, f'cannot find seed for submission with id={submission.submission_id}, index={index}'

        run_runner(end_path, RunnerOptions.GENERATE, seed=seed)

        logging.info(f'running run {index} for game (id={submission.submission_id}), using seed index {seed_index}')

        try:
            res = run_runner(end_path, RunnerOptions.RUN)

            results_filepath = os.path.join(end_path, 'logs', 'results.json')
            if os.path.exists(results_filepath):
                with open(results_filepath, 'r') as f:
                    results: dict = json.load(f)
        except Exception as e:
            logging.error(e)
        finally:
            player_sub_ids: list[int] = [int(x["file_name"].split("_")[-1]) for x in results['players']]
            assert self.tournament != -1
            run_id: int = self.insert_run(
                self.tournament.tournament_id,
                seed,
                results)
            assert results.get('reason') is None, f'{results['reason']}\n{json.dumps(results, indent=4)}'
            for i, result in enumerate(results["players"]):
                self.insert_submission_run_info(player_sub_ids[i], run_id, result["error"], i,
                                                result["avatar"]["score"])
                score_for_each_submission[player_sub_ids[i]] = result["avatar"]["score"]

            # don't store logs with non-eligible teams
            # if any([not submission.team.team_type.eligible for submission in submission_tuple]):
            #     return
            if not submission.team.team_type.eligible:
                return

            # Update information in best run dict
            # for submission in submission_tuple:
            if (score_for_each_submission[submission.submission_id] >
                    self.best_run_for_client.get(submission.submission_id, {'score': -2})['score']):
                self.best_run_for_client[submission.submission_id] = {}
                self.best_run_for_client[submission.submission_id]["log_path"] = os.path.join(end_path, 'logs')
                self.best_run_for_client[submission.submission_id]["run_id"] = run_id
                self.best_run_for_client[submission.submission_id]["score"] = score_for_each_submission[
                    submission.submission_id]

    def get_version_number(self) -> str:
        """
        runs a script in the runner folder.
        end path is where the runner is located
        runner is the name of the script (no extension)
        """

        stdout = run_runner(os.getcwd(), RunnerOptions.VERSION)
        return stdout.decode("utf-8").split('\n')[-1]

    def insert_new_tournament(self) -> Tournament:
        """
        Inserts a new Tournament in the database and returns it. Relates all the runs in this process together
        :return: a Tournament object
        """
        print("inserting tournament")
        with DB() as db:
            return crud_tournament.create(db, TournamentBase(tournament_id=0,
                                                             start_run=datetime.now(UTC),
                                                             launcher_version=self.get_version_number(),
                                                             runs_per_client=self.total_number_of_games_per_client,
                                                             is_finished=False))

    def insert_run(self, tournament_id: int, seed_id: int, results: dict) -> int:
        """
        Inserts a new Run in the database and returns it.
        :param tournament_id:
        :param seed_id:
        :param results:
        :return: the newly inserted Run's id
        """
        print("inserting run")
        with DB() as db:
            return crud_run.create(db, RunBase(run_id=0,
                                               tournament_id=tournament_id,
                                               run_time=datetime.now(UTC),
                                               seed=seed_id,
                                               results=json.dumps(results).encode("utf-8"))).run_id

    def insert_submission_run_info(self, submission_id: int, run_id: int, error: str | None, player_num: int,
                                   points_awarded: int) -> None:
        """
        Inserts a new SubmissionRunInfo entry in the database.
        :param submission_id:
        :param run_id:
        :param error:
        :param player_num:
        :param points_awarded:
        :return: None
        """
        if error is None:
            error = ''

        with DB() as db:
            submission_run_info = crud_submission_run_info.create(
                db, SubmissionRunInfoBase(submission_run_info_id=0,
                                          submission_id=submission_id,
                                          run_id=run_id,
                                          error_txt=error,
                                          player_num=player_num,
                                          points_awarded=points_awarded))

    def delete_tournament_cascade(self, tournament_id: int) -> None:
        """
        Deletes the specified Tournament from the database by using the given id.
        :param tournament_id:
        :return: None
        """
        with DB() as db:
            crud_tournament.delete(db, tournament_id)

    def read_best_logs_and_insert(self) -> None:
        """
        Finds the best logs from the client and inserts them into the database
        :return: None
        """
        for submission_id in self.best_run_for_client:
            path = self.best_run_for_client[submission_id]["log_path"]
            turn_logs: list[TurnBase] = []
            for file in os.listdir(path):
                if file in ['game_map.json', 'results.json', 'turn_logs.json']:
                    continue
                with open(os.path.join(path, file)) as fl:
                    turn_logs.append(TurnBase(turn_number=int(file[-9:-5]), run_id=self.best_run_for_client[
                        submission_id]["run_id"], turn_data=bytes(fl.read(), 'utf-8')))

            self.insert_logs(turn_logs)

    def insert_logs(self, logs: list[TurnBase]) -> None:
        """
        Inserts the given logs in the database.
        :param logs: a list of Turn objects to insert into the database
        :return: None
        """
        try:
            with DB() as db:
                crud_turn.create_all(db, logs)

        # do nothing if fails to insert due to records already existing
        except IntegrityError:
            ...

    def close_server(self) -> None:
        """
        This method will delete the tournament from the database if it exists and is not finished with all the games.
        Regardless, the ``runner_temp`` folder will be deleted.
        :return: None
        """
        if self.tournament != -1 and not self.tournament.is_finished:
            self.delete_tournament_cascade(self.tournament.tournament_id)
        else:
            logging.warning("Not deleting any tournaments")
        self.delete_runner_temp()
        schedule.clear()
        sys.exit(0)

    def delete_runner_temp(self) -> None:
        """
        Continually tries to delete the ``runner_temp`` folder.
        :return: None
        """
        while True:
            try:
                if os.path.exists(self.runner_temp_dir):
                    shutil.rmtree(self.runner_temp_dir)
                break
            except PermissionError:
                continue

    def delete_turns(self) -> None:
        """
        Deletes all entries from the Turn datatable.
        :return: None
        """
        with DB() as db:
            crud_turn.delete_all(db)

    def return_team_parings(self, submissions: list[Submission]) -> list[tuple[Submission, Submission]]:
        """
        This method will take a list of Submission entries and a list with every pairing of them. Also considers
        the number of games against the same team and increases the pairings by that value.
        :param submissions:
        :return: a list of tuples that has the submissions of each team pairing
        """
        # do not remove comment below:
        # noinspection PyTypeChecker
        fixtures: list[tuple[Submission, Submission]] = list(itertools.permutations(submissions, 2))

        temp: list[tuple[Submission, ...]]
        self.number_of_unique_games = len(fixtures)
        repeated = fixtures * self.config.NUMBER_OF_GAMES_AGAINST_SAME_TEAM
        self.total_number_of_games = len(repeated)
        return repeated

    def count_number_of_game_appearances(self, games: list[tuple[Submission, Submission]]) -> int:
        """
        Returns the number of games a client appears in.
        :param games:
        :return: the count of games a client appears in
        """
        one_id: int = games[0][0].submission_id
        count: int = sum([1 for game_tuple in games
                          if game_tuple[0].submission_id == one_id
                          or game_tuple[1].submission_id == one_id])
        return count

    def update_tournament_finished(self) -> None:
        """
        Updates the tournament to have the ``is_finished`` bool to be True.
        :return: None
        """
        self.tournament.is_finished = True
        with DB() as db:
            self.tournament = crud_tournament.update(db, self.tournament.tournament_id,
                                                     TournamentBase(**self.tournament.__dict__))

    def buffUpData(self) -> None:
        """
        This will create the different universities and team types to add to the database. This can be modified for
        different competitions; add or subtract from it as needed.
        :return: None
        """
        with DB() as db:
            try:
                crud_university.create(db, UniversityBase(
                    uni_id=1,
                    uni_name='NDSU'
                ))
                print('NDSU Added')
            except IntegrityError:
                print('NDSU Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=2,
                    uni_name='MSUM'
                ))
                print('MSUM Added')
            except IntegrityError:
                print('MSUM Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=3,
                    uni_name='UND'
                ))
                print('UND Added')
            except IntegrityError:
                print('UND Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=4,
                    uni_name='Concordia'
                ))
                print('Concordia Added')
            except IntegrityError:
                print('Concordia Already Exists')

            try:
                crud_university.create(db, UniversityBase(
                    uni_id=5,
                    uni_name='U of M'
                ))
                print('U of M Added')
            except IntegrityError:
                print('U of M Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=1,
                    team_type_name='Undergrad',
                    eligible=True
                ))
                print('Undergrad Added')
            except IntegrityError:
                print('Undergrad Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=2,
                    team_type_name='Graduate',
                    eligible=False
                ))
                print('Graduate Added')
            except IntegrityError:
                print('Graduate Already Exists')

            try:
                crud_team_type.create(db, TeamTypeBase(
                    team_type_id=3,
                    team_type_name='Alumni',
                    eligible=False
                ))
                print('Alumni Added')
            except IntegrityError:
                print('Alumni Already Exists')


if __name__ == "__main__":
    ClientRunner()
