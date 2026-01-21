from fastapi.testclient import TestClient

from server.unit_tests.conftest import EXPECTED_TOURNAMENT


# Test Submission methods in main.py

# Test get method

def test_get_tournaments(client: TestClient, example_tournament, another_tournament) -> None:
    """
    Tests getting the list of tournaments that are stored in teh database.
    :return: None
    """
    response = client.get('/tournaments/')

    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [
        EXPECTED_TOURNAMENT,
        {
            "tournament_id": 2,
            "start_run": "2000-10-31T06:30:00Z",
            "launcher_version": "10",
            "runs_per_client": 2,
            "is_finished": False,
        }
    ]
