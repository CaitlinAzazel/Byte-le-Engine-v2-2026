import importlib
import json
import logging
import sys
import threading
import traceback
from datetime import datetime

from tqdm import tqdm

from game.common.map.game_board import GameBoard
from game.common.player import Player
from game.config import *
from game.controllers.master_controller import MasterController
from game.utils.helpers import write_json_file
from game.utils.thread import Thread, CommunicationThread
from game.utils.validation import verify_code, verify_num_clients
from game.client.user_client import UserClient


class Engine:
    def __init__(self, quiet_mode=False):
        self.clients: list[Player] = list()
        self.master_controller = MasterController()
        self.tick_number = 0

        self.game_logs = dict()
        self.world = None
        self.current_world_key = None

        self.quiet_mode = quiet_mode

    # Starting point of the engine. Runs other methods then sits on top of a basic game loop until over
    def loop(self):
        source = None
        try:
            # If quiet mode is activated, replace stdout with devnull
            f = sys.stdout
            if self.quiet_mode:
                f = open(os.devnull, 'w')
                sys.stdout = f
            self.load()
            self.boot()
            for self.current_world_key in tqdm(
                    self.master_controller.game_loop_logic(),
                    bar_format=TQDM_BAR_FORMAT,
                    unit=TQDM_UNITS,
                    file=f):
                self.pre_tick()
                self.tick()
                self.post_tick()
                if self.master_controller.game_over:
                    break
                if self.tick_number >= MAX_TICKS:
                    break
        except Exception as e:
            print(f"Exception raised during runtime: {str(e)}")
            print(f"{traceback.print_exc()}")
            source = 'Game_error'
        finally:
            self.shutdown(source=source)

    # Finds, checks, and instantiates clients
    def boot(self):
        # Insert path of where clients are expected to be inside where python will look
        current_dir = os.getcwd()
        sys.path.insert(0, current_dir)
        sys.path.insert(0, f'{current_dir}/{CLIENT_DIRECTORY}')

        # Find and load clients in
        for filename in os.listdir(CLIENT_DIRECTORY):
            try:
                # Filter out files that do not contain CLIENT_KEYWORD in their filename (located in config)
                if CLIENT_KEYWORD.upper() not in filename.upper():
                    continue

                if not filename.endswith('.py'):
                    continue

                filename = filename.replace('.py', '')

                # Filter out folders
                if os.path.isdir(os.path.join(CLIENT_DIRECTORY, filename)):
                    continue

                # Otherwise, instantiate the player
                player = Player()
                self.clients.append(player)

                # Verify client isn't using invalid imports or opening anything
                imports, opening, printing = verify_code(filename + '.py')
                if len(imports) != 0:
                    player.functional = False
                    player.error = f'Player has attempted illegal imports: {imports}'

                if opening:
                    player.functional = False
                    player.error = 'Player is using "open" which is forbidden.'

                # Attempt creation of the client object
                obj: UserClient | None = None
                try:
                    # Import client's code
                    im = importlib.import_module(f'{filename}', CLIENT_DIRECTORY)
                    obj = im.Client()
                except Exception:
                    player.functional = False
                    player.error = str(traceback.format_exc())
                    continue

                player.code = obj
                thr = None
                try:
                    # Retrieve team name
                    thr = CommunicationThread(player.code.team_name, list(), str)
                    thr.start()
                    thr.join(0.01)  # Shouldn't take long to get a string

                    if thr.is_alive():
                        player.functional = False
                        player.error = 'Client failed to provide a team name in time.'

                    if thr.error is not None:
                        player.functional = False
                        player.error = str(thr.error)
                finally:
                    # Note: I keep the above thread for both naming conventions to check for client errors
                    try:
                        player.file_name = filename
                        player.team_name = thr.retrieve_value()
                    except Exception as e:
                        player.functional = False
                        player.error = f"{str(e)}\n{traceback.print_exc()}"
            except Exception as e:
                print(f"Bad client for {filename}: exception: {e}")
                print(f"{traceback.print_exc()}")
                player.functional = False

        # Verify correct number of clients have connected to start
        func_clients = [client for client in self.clients if client.functional]
        client_num_correct = verify_num_clients(func_clients,
                                                SET_NUMBER_OF_CLIENTS_START,
                                                MIN_CLIENTS_START,
                                                MAX_CLIENTS_START)

        if client_num_correct is not None:
            self.shutdown(source=f'Client_error ({client_num_correct})')
        else:
            # Sort clients based on name, for the client runner
            self.clients.sort(key=lambda clnt: clnt.team_name, reverse=True)
            # Finally, request master controller to establish clients with basic objects
            if SET_NUMBER_OF_CLIENTS_START == 1:
                self.master_controller.give_clients_objects(self.clients[:1], self.world)
            else:
                self.master_controller.give_clients_objects(self.clients, self.world)

    # Loads in the world
    def load(self):
        # Verify the log directory exists
        if not os.path.exists(LOGS_DIR):
            raise FileNotFoundError('Log directory not found.')

        # Verify the game map exists
        if not os.path.exists(GAME_MAP_FILE):
            raise FileNotFoundError('Game map not found.')

        # Delete previous logs
        for filename in os.listdir(LOGS_DIR):
            if os.path.join(LOGS_DIR, filename) == GAME_MAP_FILE:
                continue
            os.remove(os.path.join(LOGS_DIR, filename))

        world = None
        with open(GAME_MAP_FILE) as json_file:
            world = json.load(json_file)
            world['game_board'] = GameBoard().from_json(world['game_board'])
        self.world = world

    # Sits on top of all actions that need to happen before the player takes their turn
    def pre_tick(self):
        # Increment the tick
        self.tick_number += 1

        # Send current world information to master controller for purposes
        if SET_NUMBER_OF_CLIENTS_START == 1:
            self.master_controller.interpret_current_turn_data(self.clients[:1], self.world, self.tick_number)
        else:
            self.master_controller.interpret_current_turn_data(self.clients, self.world, self.tick_number)

    # Does actions like lets the player take their turn and asks master controller to perform game logic
    def tick(self):
        # Create list of threads to run client's code
        threads: list[Thread[list[ActionType]]] = list()
        for client in self.clients:
            # Skip non-functional clients
            if not client.functional:
                continue

            # Retrieve list of arguments to pass
            arguments = self.master_controller.client_turn_arguments(client, self.tick_number)

            # Create the thread, pass the arguments
            thr = Thread(func=client.code.take_turn, args=arguments)
            threads.append(thr)

        # Start all threads
        [thr.start() for thr in threads]

        # Time and wait for clients to be done
        start_time = datetime.now()
        for thr in threads:
            # We only want to wait a maximum of MAX_SECONDS_PER_TURN once all of the clients have started.
            # However, we can't simultaneously join threads without more threads or multiprocessing.
            # Solution: join one thread at a time, keep track of total running time between each join, and reduce the
            # join time, so it is always less than MAX_SECONDS_PER_TURN.
            # Get time elapsed in microseconds
            time_elapsed = datetime.now().microsecond - start_time.microsecond
            # Convert to seconds
            time_elapsed /= 1000000
            # Subtract value from MAX_SECONDS_PER_TURN to get time remaining
            time_remaining = MAX_SECONDS_PER_TURN - time_elapsed
            # Ensure value never goes negative
            time_remaining = max(0.0, time_remaining)

            thr.join(time_remaining)

        # Go through each thread and check if they are still alive
        for client, thr in zip(self.clients, threads):
            # Load actions into player
            client.actions = thr.result if thr.result is not None else []

            # If thread is no longer alive, mark it as non-functional, preventing it from receiving future turns
            if thr.is_alive():
                client.functional = False
                client.error = f'{client.id} failed to reply in time and has been dropped.'
                print(client.error)

            # Also check to see if the client had created an error and save it
            if thr.error is not None:
                client.functional = False
                client.error = thr.error
                print(thr.error)

        # Verify there are enough clients to continue the game
        func_clients = [client for client in self.clients if client.functional]
        client_num_correct = verify_num_clients(func_clients,
                                                SET_NUMBER_OF_CLIENTS_CONTINUE,
                                                MIN_CLIENTS_CONTINUE,
                                                MAX_CLIENTS_CONTINUE)
        if client_num_correct is not None:
            self.shutdown(source=f'Client_error ({client_num_correct})')

        # Finally, consult master controller for game logic
        # if SET_NUMBER_OF_CLIENTS_START == 1:
        #     self.master_controller.turn_logic(self.clients[0], self.tick_number)
        # else:
        self.master_controller.turn_logic(self.clients, self.tick_number)

    # Does any actions that need to happen after the game logic, then creates the game log for the turn
    def post_tick(self):
        # Add logs to logs list
        data = None
        # if SET_NUMBER_OF_CLIENTS_START == 1:
        #     data = self.master_controller.create_turn_log(self.clients[0], self.tick_number)
        # else:
        data = self.master_controller.create_turn_log(self.clients, self.tick_number)

        threading.Thread(target=write_json_file,
                         args=(data, os.path.join(LOGS_DIR, f'turn_{self.tick_number:04d}.json'))).start()

        # NOTE : this does not break the actual loop in Engine.loop(), so i moved the check there since
        # Engine.shutdown() still gets called in the finally clause
        # if self.master_controller.game_over:
        #     self.shutdown()

    # Attempts to safely handle an engine shutdown given any game state
    def shutdown(self, source=None):
        # Write log files
        write_json_file(self.game_logs, LOGS_FILE)

        # Retrieve and write results information
        results_information = None
        # if SET_NUMBER_OF_CLIENTS_START == 1:
        #     results_information = self.master_controller.return_final_results(self.clients[:1], self.tick_number)
        # else:
        results_information = self.master_controller.return_final_results(self.clients, self.tick_number)

        if source:
            results_information['reason'] = source

        write_json_file(results_information, RESULTS_FILE)

        # Exit game
        if source:
            output = "\n"
            for client in self.clients:
                if client.error != None:
                    output += client.error + "\n"
            print(f'\nGame has ended due to {source}: [{output}].')

            # Flush standard out
            sys.stdout.flush()

            os._exit(1)
        else:
            print(f'\nGame has successfully ended.')

            # Flush standard out
            sys.stdout.flush()

            # os._exit(0)

    # Debug print statement
    def debug(*args):
        if Debug.level >= DebugLevel.ENGINE:
            logging.basicConfig(level=logging.DEBUG)
            for arg in args:
                logging.debug(f'Engine: {arg}')
