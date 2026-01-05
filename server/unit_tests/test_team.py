import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from server.crud import crud_team
from server.schemas.team.team_base import TeamBase


@pytest.fixture
def request_json():
    return {
        "uni_id": 1,
        "team_type_id": 1,
        "team_name": "Noobss",
    }

def test_post_team(client: TestClient, request_json: dict) -> None:
    """
    Tests that creating a team works as expected.
    :return: None
    """
    response = client.post('/team/', json=request_json)
    assert response.status_code == 200, response.json()['detail']
    assert response.json()['uni_id'] == request_json['uni_id']
    assert response.json()['team_type_id'] == request_json['team_type_id']
    assert response.json()['team_name'] == request_json['team_name']

def test_post_team_invalid_team_type(client: TestClient, request_json: dict) -> None:
    request_json['team_type_id'] = -1

    response = client.post('/team/', json=request_json)
    assert response.status_code == 500, response.json()['detail']

def test_post_team_invalid_university(client: TestClient, request_json: dict) -> None:
    request_json['uni_id'] = -1

    response = client.post('/team/', json=request_json)
    assert response.status_code == 500, response.json()['detail']

def test_post_team_empty_name(client: TestClient, request_json: dict) -> None:
    request_json['team_name'] = ''

    response = client.post('/team/', json=request_json)
    assert response.status_code == 500, response.json()['detail']

def test_post_team_duplicate_name(session: Session, client: TestClient, request_json: dict) -> None:
    crud_team.create(TeamBase(**request_json), session)

    response = client.post('/team/', json=request_json)
    assert response.status_code == 500, response.json()['detail']

