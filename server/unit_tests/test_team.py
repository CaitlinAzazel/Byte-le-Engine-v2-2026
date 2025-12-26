from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_post_team(session: Session, client: TestClient, universities, team_types) -> None:
    """
    Tests that creating a team works as expected.
    :return: None
    """
    response = client.post('/team/',
                           json={"uni_id": 1,
                                 "team_type_id": 1,
                                 "team_name": "Noobss"}
                           )
    assert response.status_code == 200, response.json()['detail']
    assert response.json()['uni_id'] == 1
    assert response.json()['team_type_id'] == 1
    assert response.json()['team_name'] == "Noobss"
