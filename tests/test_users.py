from tests.mocks.pokemon import POKEMON_MOCKS


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "ash",
            "email": "ash@example.com",
            "password": "pikachu123",
            "pokemon_ids": [1, 3],
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["username"] == "ash"
    assert data["email"] == "ash@example.com"
    assert data["pokemon_ids"] == [1, 3]
    assert "password" not in data


def test_create_user_duplicate_email(client):
    user = {
        "username": "ash",
        "email": "ash@example.com",
        "password": "pikachu123",
        "pokemon_ids": [1],
    }

    first_response = client.post("/users", json=user)
    second_response = client.post("/users", json=user)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Email already registered"


def test_create_user_invalid_data(client):
    response = client.post(
        "/users",
        json={
            "username": "a",
            "email": "not-an-email",
            "password": "123",
            "pokemon_ids": [],
        },
    )

    assert response.status_code == 422


def test_get_all_users(client):
    client.post(
        "/users",
        json={
            "username": "ash",
            "email": "ash@example.com",
            "password": "pikachu123",
            "pokemon_ids": [1],
        },
    )

    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1
    assert users[0]["username"] == "ash"
    assert users[0]["pokemon_ids"] == [1]
    assert "password" not in users[0]


def test_get_user_not_found(client):
    response = client.get("/users/99999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_all_users_empty(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert response.json() == []


def test_update_user(client):
    created = client.post(
        "/users",
        json={
            "username": "ash",
            "email": "ash@example.com",
            "password": "pikachu123",
            "pokemon_ids": [1],
        },
    )

    user_id = created.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={"username": "ash_updated"},
    )

    assert response.status_code == 200
    assert response.json()["username"] == "ash_updated"
    assert response.json()["email"] == "ash@example.com"

    users = client.get("/users").json()

    assert users[0]["username"] == "ash_updated"


def test_delete_user(client):
    created = client.post(
        "/users",
        json={
            "username": "misty",
            "email": "misty@example.com",
            "password": "password123",
            "pokemon_ids": [7],
        },
    )

    user_id = created.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.content == b""

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 404


def test_get_user_with_pokemons(client, mock_pokemon_client):
    created = client.post(
        "/users",
        json={
            "username": "ash",
            "email": "ash@example.com",
            "password": "password123",
            "pokemon_ids": [1, 25],
        },
    )

    user_id = created.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "ash"
    assert data["pokemon_ids"] == [1, 25]
    assert data["pokemons"] == [
        POKEMON_MOCKS[1],
        POKEMON_MOCKS[25],
    ]
