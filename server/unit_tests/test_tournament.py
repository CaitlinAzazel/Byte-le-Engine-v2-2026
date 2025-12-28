from fastapi.testclient import TestClient


# Test Submission methods in main.py

# Test get method

def test_get_tournaments(client: TestClient) -> None:
    """
    Tests getting the list of tournaments that are stored in teh database.
    :return: None
    """
    response = client.get('/tournaments/')

    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [
        {
            "tournament_id": 1,
            "start_run": "2000-10-31T06:30:00Z",
            "launcher_version": "12",
            "runs_per_client": 1,
            "is_finished": True,
            "runs": [
                {
                    "run_id": 1,
                    "tournament_id": 1,
                    "run_time": "2000-10-31T06:30:00Z",
                    "seed": 1,
                    "results": "test",
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
                },
                {
                    "run_id": 2,
                    "tournament_id": 1,
                    "run_time": "2000-10-31T06:30:00Z",
                    "seed": 2,
                    "results": "test",
                    "submission_run_infos": [],
                    "turns": []
                }
            ]
        },
        {
            "tournament_id": 2,
            "start_run": "2000-10-31T06:30:00Z",
            "launcher_version": "10",
            "runs_per_client": 2,
            "is_finished": False,
            "runs": [
                {
                    "run_id": 3,
                    "tournament_id": 2,
                    "run_time": "2000-10-31T06:30:00Z",
                    "seed": 1,
                    "results": "test",
                    "submission_run_infos": [],
                    "turns": []
                },
                {
                    "run_id": 4,
                    "tournament_id": 2,
                    "run_time": "2000-10-31T06:30:00Z",
                    "seed": 2,
                    "results": "test",
                    "submission_run_infos": [],
                    "turns": []
                }
            ]
        }
    ]
