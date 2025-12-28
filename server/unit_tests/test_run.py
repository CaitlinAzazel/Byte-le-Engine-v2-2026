from fastapi.testclient import TestClient


# Test Run methods in main.py

# Test get_run method
def test_get_runs_param(client: TestClient) -> None:
    """
    Tests getting the runs by using the tournament id and team uuid in the URL.
    :return: None
    """
    response = client.get('/runs?tournament_id=1&team_uuid=1')
    assert response.status_code == 200
    assert response.json() == [
        {
            "run_id": 1,
            "tournament_id": 1,
            "run_time": "2000-10-31T06:30:00Z",
            "seed": 1,
            "results": "test",
            "tournament": {
                "tournament_id": 1,
                "start_run": "2000-10-31T06:30:00Z",
                "launcher_version": "12",
                "runs_per_client": 1,
                "is_finished": True
            },
            "submission_run_infos": [
                {
                    "submission_run_info_id": 1,
                    "run_id": 1,
                    "submission_id": 1,
                    "error_txt": "error",
                    "player_num": 1,
                    "points_awarded": 100,
                    "submission": {
                        "submission_id": 1,
                        "submission_time": "2000-10-31T06:30:00Z",
                        "file_txt": "test",
                        "team": {
                            "uni_id": 1,
                            "team_type_id": 1,
                            "team_name": "Noobs"
                        }
                    }
                }
            ],
            "turns": []
        }
    ]


# Test run method
def test_get_runs(client: TestClient) -> None:
    """
    Tests getting all runs in the database via the URL.
    :return: None
    """
    response = client.get('/runs/')

    assert response.status_code == 200
    assert response.json() == [{"run_id": 1,
                                "tournament_id": 1,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 2,
                                "tournament_id": 1,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 2,
                                "results": "test"},
                               {"run_id": 3,
                                "tournament_id": 2,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 1,
                                "results": "test"},
                               {"run_id": 4,
                                "tournament_id": 2,
                                "run_time": "2000-10-31T06:30:00Z",
                                "seed": 2,
                                "results": "test"}
                               ]
