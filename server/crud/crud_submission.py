import uuid
from typing import Type

from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from server.models.submission import Submission
from server.models.team import Team
from server.schemas.submission.submission_w_team import SubmissionWTeam


# create method for submission
def create(submission: SubmissionWTeam, db: Session) -> Submission:
    """
    This method will create an entry in the ``Submission`` table based on the submission.py file. Refer to the
    ``models`` package for more information about submission.py.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    db_submission: Submission = Submission(**submission.model_dump(exclude={'submission_id'}))
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


# read most recent submission
def read(db: Session, id: int, eager: bool = False) -> Submission | None:
    """
    This gets information from the Run table and returns it. Eager loading will determine whether to only return the
    entry in the Run table or to return it with more information from the tables that it's related to.
    :param db:
    :param id:
    :param eager:
    :return:
    """
    return (db.query(Submission)
            .filter(Submission.submission_id == id)
            .first() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter(Submission.submission_id == id)
            .first())


# read submission based off team id
def read_all_by_team_id(db: Session, team_uuid: uuid, eager: bool = False) -> [Submission]:
    """
    Similar functionality to the read_all() method, but this filters based on the given team uuid.
    :param db:
    :param team_uuid:
    :param eager:
    :return:
    """
    return (db.query(Submission)
            .filter(Submission.team_uuid == team_uuid)
            .all() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter(Submission.team_uuid == team_uuid)
            .all())


# read a specified submission
def read_all_W_filter(db: Session, eager: bool = False, **kwargs) -> [Submission]:
    """
    Similar functionality to the read_all() method, but this filters based on the given information which is unpacked
    by using ``**``.
    :param db:
    :param eager:
    :param kwargs:
    :return:
    """
    return (db.query(Submission)
            .filter_by(**kwargs)
            .all() if not eager
            else db.query(Submission)
            .options(joinedload(Submission.submission_run_infos),
                     joinedload(Submission.team))
            .filter_by(**kwargs)
            .all())


# update a submission
def update(db: Session, id: int, submission: SubmissionWTeam) -> Submission | None:
    """
    This method takes a Run object and updates the specified Run in the database with it. If there is nothing to
    update, returns None.
    :param db:
    :param id:
    :param submission:
    :return:
    """
    db_submission: Submission | None = (db.query(Submission)
                                        .filter(and_(Submission.submission_id == id,
                                                     Submission.team_uuid == submission.team_id_uuid))
                                        .one_or_none())
    if db_submission is None:
        return

    for key, value in submission.model_dump().items():
        setattr(db_submission, key, value) if value is not None else None

    db.commit()
    db.refresh(db_submission)
    return db_submission


# delete a submission
def delete(db: Session, id: int, submission: SubmissionWTeam) -> None:
    """
    Deletes the specified Submission entity from the database.
    :param db:
    :param id:
    :param submission:
    :return: None
    """
    db_submission: Submission | None = (db.query(Submission)
                                        .filter(and_(Submission.submission_id == id,
                                                     Submission.team_uuid == submission.team_id_uuid))
                                        .one_or_none())
    if db_submission is None:
        return

    db.delete(db_submission)
    db.commit()


def get_latest_submission_for_each_team(db: Session) -> list[Submission]:
    return (db.query(Submission)
            .filter(Submission.submission_id.in_(
                    db.query(
                        func.max(Submission.submission_id))
                    .group_by(Submission.team_uuid)))
            .options(joinedload(Submission.team)
                     .joinedload(Team.team_type))
            .all())
