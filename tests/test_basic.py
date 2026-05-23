from main import app


def test_home_route():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200
        assert b"FASTQ Analysis Pipeline" in response.data


def test_status_unknown_task():
    with app.test_client() as client:
        response = client.get("/status/test-task-id")
        assert response.status_code == 200
        assert response.json["status"] == "pending"
