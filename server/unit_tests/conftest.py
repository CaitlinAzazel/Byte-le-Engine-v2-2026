import json
import pytest

from datetime import datetime, timezone 
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from server.main import app, get_db
from server.models.base import Base
from server.models.submission import Submission
from server.models.submission_run_info import SubmissionRunInfo
from server.models.team import Team
from server.models.run import Run
from server.models.team_type import TeamType
from server.models.tournament import Tournament
from server.models.university import University


"""
https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
this file is used by pytest to share the fixtures below with other files that contain tests in this folder
"""


EXAMPLE_DATETIME = datetime.fromisoformat('2000-10-31T01:30:00-05:00')
EXAMPLE_DATETIME_UTC = EXAMPLE_DATETIME.astimezone(timezone.utc)

# datetimes in fastapi responses are represented as strings in ISO 8601 format https://fastapi.tiangolo.com/tutorial/extra-data-types/#other-data-types
# our datetimes will always be in UTC
# -> so their UTC offset is 0
# -> which is replaced with a Z in ISO 8601 https://en.wikipedia.org/wiki/ISO_8601#:~:text=If%20the%20time%20is%20in%20UTC
EXPECTED_DATETIME = EXAMPLE_DATETIME_UTC.isoformat().replace('+00:00', 'Z')
EXPECTED_TEAM = {
    "uni_id": 1,
    "team_type_id": 1,
    "team_name": "Noobss"
}
EXPECTED_RUN = {
    "run_id": 1,
    "tournament_id": 1,
    "run_time": EXPECTED_DATETIME,
    "seed": 1,
    "results": 'test'
}
EXPECTED_TOURNAMENT = {
    "tournament_id": 1,
    "start_run": EXPECTED_DATETIME,
    "launcher_version": "12",
    "runs_per_client": 1,
    "is_finished": True
}
EXPECTED_SUBMISSION_RUN_INFO = {
    "submission_run_info_id": 1,
    "run_id": 1,
    "submission_id": 1,
    "error_txt": "error",
    "player_num": 1,
    "points_awarded": 100,
}
EXPECTED_SUBMISSION = {
    "submission_id": 1,
    "submission_time": EXPECTED_DATETIME,
    "file_txt": "test",
}


EXPECTED_SUBMISSION_RESPONSE = {
    **EXPECTED_SUBMISSION,
    "submission_run_infos": [
        {
            **EXPECTED_SUBMISSION_RUN_INFO,
            "run": EXPECTED_RUN,
        }
    ],
    "team": EXPECTED_TEAM,
} 
EXPECTED_RUN_RESPONSE = {
    **EXPECTED_RUN,
    "tournament": EXPECTED_TOURNAMENT,
    "submission_run_infos": [
        {
            **EXPECTED_SUBMISSION_RUN_INFO,
            "submission": {
                **EXPECTED_SUBMISSION,
                "team": EXPECTED_TEAM,
            }
        }
    ],
    "turns": []
}

@pytest.fixture(name='session')
def session_fixture():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={
            'check_same_thread': False,
        },
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture(name='client')
def client_fixture(session: Session):
    def get_db_override():
        return session

    # https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency
    app.dependency_overrides[get_db] = get_db_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def universities(session: Session):
    university_names = [
        'NDSU',
        'MSUM',
        'UND',
        'Concordia',
        'U of M',
    ]
    for i, name in enumerate(university_names):
        # NOTE: the value of uni_id is not actually used since it's an auto-incremented field
        session.add(University(
            uni_id=i+1,
            uni_name=name,
        ))

@pytest.fixture(autouse=True)
def team_types(session: Session):
    team_type_data = [
        ('Undergrad', True),
        ('Graduate', False), 
        ('Alumni', False),
    ]
    for i, data in enumerate(team_type_data):
        # NOTE: the value of team_type_id is not actually used since it's an auto-incremented field
        session.add(TeamType(
            team_type_id=i+1,
            team_type_name=data[0],
            eligible=data[1],
        ))

@pytest.fixture
def example_team(session: Session):
    session.add(Team(
        uni_id=1,
        team_type_id=1,
        team_name="Noobss",
        team_uuid="1",
    ))

@pytest.fixture
def example_submission(session: Session, example_team):
    session.add(Submission(
        submission_id=1,
        submission_time=EXAMPLE_DATETIME,
        file_txt='test'.encode(),
        team_uuid='1',
    ))

@pytest.fixture
def another_submission(session: Session, example_submission):
    session.add(Submission(
        submission_id=2,
        submission_time=EXAMPLE_DATETIME,
        file_txt='test'.encode(),
        team_uuid='1',
    ))

@pytest.fixture
def example_tournament(session: Session):
    session.add(Tournament(
        start_run=EXAMPLE_DATETIME,
        launcher_version='12',
        runs_per_client=1,
        is_finished=True,
    ))

@pytest.fixture
def another_tournament(session: Session, example_tournament):
    session.add(Tournament(
        tournament_id=2,
        start_run=EXAMPLE_DATETIME,
        launcher_version='10',
        runs_per_client=2,
        is_finished=False,
    ))

@pytest.fixture
def example_run(session: Session, example_tournament):
    session.add(Run(
        run_id=1,
        tournament_id=1,
        run_time=EXAMPLE_DATETIME,
        seed=1,
        results='test'.encode()
    ))

@pytest.fixture
def more_runs(session: Session, example_run, another_tournament):
    session.add_all([
        Run(
            run_id=2,
            tournament_id=1,
            run_time=EXAMPLE_DATETIME,
            seed=2,
            results='test'.encode()
        ),
        Run(
            run_id=3,
            tournament_id=2,
            run_time=EXAMPLE_DATETIME,
            seed=1,
            results='test'.encode()
        ),
        Run(
            run_id=4,
            tournament_id=2,
            run_time=EXAMPLE_DATETIME,
            seed=2,
            results='test'.encode()
        )
    ])

@pytest.fixture
def example_submission_run_info(session: Session, example_run, example_submission):
    session.add(SubmissionRunInfo(
        run_id=1,
        submission_id=1,
        error_txt='error'.encode(),
        player_num=1,
        points_awarded=100,
    ))
