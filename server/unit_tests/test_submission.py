from fastapi.testclient import TestClient

from server.unit_tests.conftest import EXPECTED_DATETIME, EXPECTED_SUBMISSION, EXPECTED_SUBMISSION_RESPONSE, EXPECTED_TEAM


def test_post_submission(client: TestClient, example_team) -> None:
    """
    Tests posting a submission via the URL.
    :return: None
    """
    response = client.post('/submission/',
                           json={"team_uuid": '1',
                                 "submission_id": 1,
                                 "submission_time": "2000-10-31T01:30:00-05:00",
                                 "file_txt": 'test'}
                           )
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == EXPECTED_SUBMISSION


# Test get methods

def test_get_submission(client: TestClient, example_submission, example_submission_run_info) -> None:
    """
    Tests getting a submission via the submission id and team uuid in the URL.
    :return: None
    """
    response = client.get('/submission?submission_id=1&team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == EXPECTED_SUBMISSION_RESPONSE


def test_get_submissions(client: TestClient, example_submission, example_submission_run_info, another_submission) -> None:
    """
    Tests getting all submissions given a team uuid in the URL.
    :return: None
    """
    response = client.get('/submissions?team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [
        EXPECTED_SUBMISSION_RESPONSE,
        {
            "submission_id": 2,
            "submission_time": EXPECTED_DATETIME,
            "file_txt": "test",
            "team": EXPECTED_TEAM,
            "submission_run_infos": []
        }
    ]


# Test read nonexistent submission/s

def test_get_nonexistent_submission(client: TestClient) -> None:
    """
    Tests that a non-existent submission cannot be retrieved; raises an error.
    :return: None
    """
    response = client.get('/submission?submission_id=2&team_uuid=2')
    assert response.status_code == 404, response.json()['detail']
    assert 'Submission not found' in response.json()['detail']
