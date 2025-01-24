from flask.testing import FlaskClient

from app.users import User


def test_can_view_users_page(client: FlaskClient, new_user: User) -> None:
    resp = client.get("/users/")
    assert resp.status_code == 200
    assert "All Users" in resp.text
    assert new_user.name in resp.text
    assert str(new_user.salary) in resp.text


def test_can_view_user_details(client: FlaskClient, new_user: User) -> None:
    # test user not found raises 404
    resp = client.get(f"/users/foo")
    assert resp.status_code == 404
    # test valid user id
    resp = client.get(f"/users/{new_user.id}")
    assert resp.status_code == 200
    assert new_user.name in resp.text


def test_can_edit_user(client: FlaskClient, new_user: User) -> None:
    # test user not found raises 404
    resp = client.get(f"/users/foo/edit")
    assert resp.status_code == 404

    url = f"/users/{new_user.id}/edit"
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Edit User" in resp.text

    payload = {
        "name": "new name",
        "gender": new_user.gender,
        "salary": new_user.salary,
        "date_of_birth": new_user.date_of_birth,
    }
    edit_resp = client.post(url, data=payload, follow_redirects=True)
    assert edit_resp.status_code == 200
    assert "Edit User" in edit_resp.text
    assert "new name" in edit_resp.text


def test_can_add_new_user(client: FlaskClient, db) -> None:
    url = "/users/add"
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Create User" in resp.text

    payload = {
        "name": "Test user",
        "gender": "male",
        "salary": 12000,
        "date_of_birth": "1990-04-12",
    }
    add_resp = client.post(url, data=payload, follow_redirects=True)
    assert add_resp.status_code == 200
    assert "All Users" in add_resp.text
    assert payload["name"] in add_resp.text
    assert str(payload["salary"]) in add_resp.text


def test_can_delete_new_user(client: FlaskClient, new_user: User) -> None:
    # test user not found raises 404
    resp = client.post(f"/users/foo/delete")
    assert resp.status_code == 404

    url = f"/users/{new_user.id}/delete"

    delete_resp = client.post(url, follow_redirects=True)
    assert delete_resp.status_code == 200
    assert "User deleted successfully" in delete_resp.text
    assert new_user.name not in delete_resp.text


def test_can_get_user_details_json(client: FlaskClient, new_user: User) -> None:
    # test user not found raises 404
    resp = client.get(f"/users/foo/details")
    assert resp.status_code == 404

    url = f"/users/{new_user.id}/details"

    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.json["age"] == new_user.get_age()
    assert resp.json["gender"] == new_user.gender
