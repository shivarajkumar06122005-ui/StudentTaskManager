def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={
            "title": "Learn FastAPI",
            "description": "Practice backend development",
            "completed": False
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn FastAPI"
    assert response.json()["completed"] is False


def test_get_all_tasks(client):
    client.post(
        "/tasks/",
        json={"title": "Learn Python"}
    )

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_single_task(client):
    create_response = client.post(
        "/tasks/",
        json={"title": "Learn MySQL"}
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["title"] == "Learn MySQL"


def test_update_task(client):
    create_response = client.post(
        "/tasks/",
        json={"title": "Learn Python"}
    )

    task_id = create_response.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn Advanced Python",
            "description": "Updated task",
            "completed": True
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Advanced Python"
    assert response.json()["completed"] is True


def test_delete_task(client):
    create_response = client.post(
        "/tasks/",
        json={"title": "Delete this task"}
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200

    check_response = client.get(f"/tasks/{task_id}")

    assert check_response.status_code == 404