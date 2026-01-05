from fastapi.testclient import TestClient

from server.unit_tests.conftest import EXPECTED_DATETIME, EXPECTED_RUN_RESPONSE



# Test Run methods in main.py

# Test get_run method
def test_get_runs_param(client: TestClient, example_run, example_submission_run_info, example_tournament) -> None:
    """
    Tests getting the runs by using the tournament id and team uuid in the URL.
    :return: None
    """
    response = client.get('/runs?tournament_id=1&team_uuid=1')
    assert response.status_code == 200
    assert response.json() == [EXPECTED_RUN_RESPONSE]


# Test run method
def test_get_runs(client: TestClient, more_runs) -> None:
    """
    Tests getting all runs in the database via the URL.
    :return: None
    """
    response = client.get('/runs/')

    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [{"run_id": 1,
                                "tournament_id": 1,
                                "run_time": EXPECTED_DATETIME,
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 2,
                                "tournament_id": 1,
                                "run_time": EXPECTED_DATETIME,
                                "seed": 2,
                                "results": "test"},
                               {"run_id": 3,
                                "tournament_id": 2,
                                "run_time": EXPECTED_DATETIME,
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 4,
                                "tournament_id": 2,
                                "run_time": EXPECTED_DATETIME,
                                "seed": 2,
                                "results": "test"}
                               ]
