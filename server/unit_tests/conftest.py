import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from server.crud import crud_team_type, crud_university
from server.main import app, get_db
from server.models.base import Base
from server.schemas.team_type.team_type_base import TeamTypeBase
from server.schemas.university.university_base import UniversityBase


"""
https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
this file is used by pytest to share the fixtures below with other files that contain tests in this folder
"""


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
        crud_university.create(session, UniversityBase(
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
        crud_team_type.create(session, TeamTypeBase(
            team_type_id=i+1,
            team_type_name=data[0],
            eligible=data[1],
        ))
