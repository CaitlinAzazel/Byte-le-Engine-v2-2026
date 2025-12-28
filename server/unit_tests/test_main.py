from fastapi.testclient import TestClient

from server.unit_tests.conftest import EXAMPLE_DATETIME


def test_read_root(client: TestClient):
    response = client.get('/')
    assert response.json() == {'message': 'Hello World'}


def test_read_get_submission(client: TestClient, example_team, example_submission):
    response = client.get('/submission?submission_id=1&team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == {"submission_id": 1,
         "submission_time": "2000-10-31T01:30:00-05:00",
         "file_txt": "test",
         "team": {"uni_id": 1,
                  "team_type_id": 1,
                  "team_name": "Noobss"},
         "submission_run_infos": []}


def test_read_get_submissions(client: TestClient, example_submission):
    response = client.get('/submissions?team_uuid=1')
    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [{"submission_id": 1,
        "submission_time": "2000-10-31T01:30:00-05:00",
        "file_txt": "test",
        "team": {"uni_id": 1,
                "team_type_id": 1,
                "team_name": "Noobs"},
        "submission_run_infos": [{"submission_run_info_id": 1,
                                    "run_id": 1,
                                    "submission_id": 1,
                                    "error_txt": "error",
                                    "run": {"run_id": 1,
                                            "group_run_id": 1,
                                            "run_time": "2000-10-31T01:30:00-05:00",
                                            "seed": 1}}]},]
