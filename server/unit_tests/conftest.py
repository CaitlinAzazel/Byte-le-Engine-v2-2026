from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from server.main import app, get_db
from server.models.base import Base
from server.models.submission import Submission
from server.models.team import Team
from server.models.run import Run
from server.models.team_type import TeamType
from server.models.university import University


"""
https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
this file is used by pytest to share the fixtures below with other files that contain tests in this folder
"""


EXAMPLE_DATETIME = datetime.fromisoformat('2000-10-31T01:30:00-05:00')


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
        submission_time=EXAMPLE_DATETIME,
        file_txt='test'.encode(),
        team_uuid='1',
    ))

@pytest.fixture
def example_run(session: Session):
    session.add(Run(
        tournament_id=0,
        run_time=EXAMPLE_DATETIME,
        seed=0,
    ))
