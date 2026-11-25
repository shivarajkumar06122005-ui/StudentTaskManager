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

def test_unauthorized_access(client):
    # Remove the JWT authentication header
    client.headers.pop("Authorization", None)

    response = client.get("/tasks/")

    assert response.status_code == 401


def test_users_cannot_access_each_others_tasks(client):
    # User A creates a task
    task_response = client.post(
        "/tasks/",
        json={
            "title": "User A Private Task",
            "description": "This task belongs to User A",
            "completed": False
        }
    )

    assert task_response.status_code == 200
    task_id = task_response.json()["id"]

    # Register User B
    register_response = client.post(
        "/auth/register",
        json={
            "email": "userb@example.com",
            "password": "UserBPassword123"
        }
    )

    assert register_response.status_code == 201

    # Login as User B
    login_response = client.post(
        "/auth/token",
        data={
            "username": "userb@example.com",
            "password": "UserBPassword123"
        }
    )

    assert login_response.status_code == 200

    # Switch authentication to User B
    user_b_token = login_response.json()["access_token"]
    client.headers.update({
        "Authorization": f"Bearer {user_b_token}"
    })

    # User B tries to access User A's task
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"