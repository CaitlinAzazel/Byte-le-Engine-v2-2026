from fastapi.testclient import TestClient


# Test Team Types methods in main.py

# Test get method


def test_get_team_types(client: TestClient) -> None:
    """
    Tests that the team types are returned correctly.
    :return: None
    """
    response = client.get('/team_types/')

    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [{"team_type_id": 1,
                                "team_type_name": "Undergrad",
                                "eligible": True},
                               {"team_type_id": 2,
                                "team_type_name": "Graduate",
                                "eligible": False},
                               {"team_type_id": 3,
                                "team_type_name": "Alumni",
                                "eligible": False}]
