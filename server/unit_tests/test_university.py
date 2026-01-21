from fastapi.testclient import TestClient


# Test University methods in main.py

# Test get method

def test_get_universities(client: TestClient) -> None:
    """
    Tests that getting the universities in from the database works.
    :return: None
    """
    response = client.get('/universities/')

    assert response.status_code == 200, response.json()['detail']
    assert response.json() == [{"uni_id": 1,
                                "uni_name": "NDSU"},
                               {"uni_id": 2,
                                "uni_name": "MSUM"},
                               {"uni_id": 3,
                                "uni_name": "UND"},
                               {"uni_id": 4,
                                "uni_name": "Concordia"},
                               {"uni_id": 5,
                                "uni_name": "U of M"}]
