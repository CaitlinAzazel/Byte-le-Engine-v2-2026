from fastapi.testclient import TestClient

from server.unit_tests.conftest import EXPECTED_SUBMISSION_RESPONSE



def test_read_root(client: TestClient):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}

def test_read_get_submission(client: TestClient, example_team, example_submission, example_submission_run_info):
    response = client.get('/submission?submission_id=1&team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == EXPECTED_SUBMISSION_RESPONSE

def test_read_get_submissions(client: TestClient, example_team, example_submission, example_submission_run_info):
    response = client.get('/submissions?team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [EXPECTED_SUBMISSION_RESPONSE]
