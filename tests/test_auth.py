
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "NewPassword123"
        }
    )

    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"
    assert "hashed_password" not in response.json()


def test_duplicate_email_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 409


def test_login_success(client):
    response = client.post(
        "/auth/token",
        data={
            "username": "test@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post(
        "/auth/token",
        data={
            "username": "test@example.com",
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
