"""
This file is the main entry point for the server, creating endpoints for the clients.
It should be noted that the runners do not require endpoints as they run on the server and utilize the crud files to
interact with the DB.
"""

from typing import Callable
from functools import wraps

import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from server.models.base import Base
from server.database import SessionLocal, engine
from server.crud import crud_submission, crud_team_type, crud_university, crud_team, crud_tournament, crud_run

# These models need to be imported to build the database correctly. DO NOT REMOVE THEM
from server.models.run import Run
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.team_type import TeamType
from server.models.turn import Turn
from server.models.university import University
from server.models.tournament import Tournament
from server.models.submission import Submission
from server.schemas.team.team_schema import TeamSchema

from server.schemas.tournament.tournament_base import TournamentBase
from server.schemas.tournament.tournament_schema import TournamentSchema
from server.schemas.run.run_base import RunBase
from server.schemas.run.run_schema import RunSchema
from server.schemas.submission.submission_base import SubmissionBase
from server.schemas.submission.submission_schema import SubmissionSchema
from server.schemas.submission.submission_w_team import SubmissionWTeam
from server.schemas.team.team_base import TeamBase
from server.schemas.team.team_id_schema import TeamIdSchema
from server.schemas.team_type.team_type_base import TeamTypeBase
from server.schemas.team_type.team_type_schema import TeamTypeSchema
from server.schemas.university.university_base import UniversityBase
from server.schemas.university.university_schema import UniversitySchema

# Creates the DB
Base().metadata.create_all(bind=engine)

# run in byte_engine folder: uvicorn server.main:app --reload
app = FastAPI()


def get_db():
    """
    Get a database session for orm and query execution
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_with_return_to_client(func: Callable) -> Callable:
    """
    A decorator for returning errors to the client instead of leaving errors on serverside only
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wraps the function
        :param args:
        :param kwargs:
        :return:
        """
        try:
            return func(*args, **kwargs)
        # keep the status code if e was an HTTPException
        except HTTPException as e:
            raise e
        # otherwise default to 500 since the error WAS serverside
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper


# API

@app.get('/')
def root():
    """
    Root endpoint.
    :return:
    """
    return {"message": "Hello World"}


# post submission
@app.post('/submission/', response_model=SubmissionBase)
@run_with_return_to_client
def post_submission(submission: SubmissionWTeam, db: Session = Depends(get_db)):
    """
    Submission post endpoint.
    :param submission: Submission with Team schema (dict) is what is expected in the request body.
    :param db: DB session.
    :return:
    """
    return crud_submission.create(submission, db)


# post team endpoint
@app.post('/team/', response_model=TeamIdSchema)
@run_with_return_to_client
def post_team(team: TeamBase, db: Session = Depends(get_db)):
    """
    Team post endpoint.
    :param team: Team base schema (dict) is what is expected in the request body.
    :param db: DB session.
    :return:
    """
    # Throw error when team name already exists
    try:
        return crud_team.create(team, db)
    except IntegrityError as err:
        raise Exception('Encountered an Integrity Error, most likely due to your team name matching a pre-existing '
                        'team name. Please choose a different name.')


@app.get('/team_info', response_model=TeamIdSchema)
@run_with_return_to_client
def get_team_info(uuid: str, db: Session = Depends(get_db)):
    """
    This endpoint is currently unused, this endpoint could be used to get the team information.
    :param uuid: UUID of the team, also known as vID.
    :param db: DB session.
    :return:
    """
    return crud_team.read(db, uuid, True)


# gets the INDIVIDUAL submission data of a specific team
@app.get('/submission', response_model=SubmissionSchema)
@run_with_return_to_client
def get_submission(submission_id: int, team_uuid: str, db: Session = Depends(get_db)):
    """
    Gets the submission information for an id provided.
    :param submission_id: An int representing the submission id.
    :param team_uuid: A string representing the team Universally Unique Identifier.
    :param db: DB session.
    :return:
    """
    # Retrieves a list of submissions where the submission id and uuids match
    submission_list: list[Submission] | None = crud_submission.read_all_W_filter(
        db, submission_id=submission_id, team_uuid=team_uuid)

    if submission_list is None or len(submission_list) == 0:
        raise HTTPException(status_code=404, detail="Submission not found!")

    return submission_list[0]  # returns a single SubmissionSchema to give the submission data to the user


# get all runs in a selected group run that a team was a part of
@app.get('/runs', response_model=list[RunSchema])
@run_with_return_to_client
def get_runs(tournament_id: int, team_uuid: str | None = None, db: Session = Depends(get_db)):
    """
    Gets the runs for a given tournament and given team, if provided.
    :param tournament_id: An int representing the tournament id.
    :param team_uuid: A string representing the team Universally Unique Identifier.
    :param db: DB session.
    :return:
    """
    run_list: list[Run] | None = crud_run.read_all_W_filter(
        db, tournament_id=tournament_id)

    # getting a run list where the team_uuid exists in the submission_run_info
    if team_uuid is not None:
        run_list = [run for run in run_list if team_uuid in [submission_run.submission.team.team_uuid if
                                                             submission_run.submission is not None else None for
                                                             submission_run in run.submission_run_infos]]

    if run_list is None:
        raise HTTPException(status_code=404, detail="Run not found D:")

    return run_list


# gets MULTIPLE submissions
# get submissions
@app.get('/submissions', response_model=list[SubmissionSchema])
@run_with_return_to_client
def get_submissions(team_uuid: str, db: Session = Depends(get_db)):
    """
    Gets the submissions for a given team.
    :param team_uuid: A string representing the team Universally Unique Identifier.
    :param db: DB session.
    :return:
    """
    return crud_submission.read_all_by_team_id(db, team_uuid)


# get team types
@app.get('/team_types/', response_model=list[TeamTypeBase])
@run_with_return_to_client
def get_team_types(db: Session = Depends(get_db)):
    """
    Gets the team types in the DB.
    :param db: DB session.
    :return:
    """
    return crud_team_type.read_all(db)


# get universities
@app.get('/universities/', response_model=list[UniversityBase])
@run_with_return_to_client
def get_universities(db: Session = Depends(get_db)):
    """
    Gets the universities in the DB.
    :param db: DB session.
    :return:
    """
    return crud_university.read_all(db)


# get runs
@app.get('/runs/', response_model=list[RunBase])
@run_with_return_to_client
def get_runs(db: Session = Depends(get_db)):
    """
    Gets the runs in the DB. This is currently unused and would be a resource intensive call if it was used.
    :param db: DB session.
    :return:
    """
    return crud_run.read_all(db)


# get tournaments
@app.get('/tournaments/', response_model=list[TournamentBase])
@run_with_return_to_client
def get_tournaments(db: Session = Depends(get_db)):
    """
    Gets the tournaments from the DB.
    :param db: DB session.
    :return:
    """
    temp: list[Tournament] = crud_tournament.read_all(db)

    if len(temp) == 0:
        raise Exception('No tournaments found.')

    return temp


# get tournament by id
@app.get('/tournament', response_model=TournamentSchema)
@run_with_return_to_client
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """
    Gets a single tournament from the DB by id.
    :param tournament_id: An int representing the id of a tournament.
    :param db: DB session.
    :return:
    """
    temp: Tournament = crud_tournament.read(db, tournament_id, eager=True)

    if temp is None:
        raise Exception('No tournaments found.')

    return temp


@app.get('/latest_tournament/', response_model=TournamentSchema)
@run_with_return_to_client
def get_latest_tournament(db: Session = Depends(get_db)):
    """
    An endpoint to retrieve the latest tournament.
    :param db: DB session.
    :return:
    """
    temp: Tournament = crud_tournament.get_latest_tournament(db)

    if temp is None:
        raise Exception('No tournaments found.')

    return temp

# main should NOT be able to delete data (we do not want the public to be able to delete), so no deletion endpoints
