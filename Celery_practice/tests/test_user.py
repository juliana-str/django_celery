import pytest
from django.urls import reverse

from .fixtures import (
    FIRST_NAME,
    PASSWORD,
    USER,
)

from .fixtures import USER_EMAIL


@pytest.mark.django_db(transaction=True)
class TestUser:

    @pytest.mark.django_db
    def test_register_user(self, client):
        payload = {"username": USER, "email": USER_EMAIL,
                   "first_name": FIRST_NAME, "password": PASSWORD}
        response = client.post("/api/users/", payload, format="json")

        assert response.status_code == 201
        assert response.data["username"] == payload["username"]
        assert response.data["email"] == payload["email"]
        assert "password" not in response.data

    @pytest.mark.django_db
    def test_register_user_validation_fail(self, client):
        payload = [
            {"username": USER, "email": USER_EMAIL},
            {"username": USER, "password": PASSWORD},
            {"email": USER_EMAIL, "password": PASSWORD},
        ]
        for field in payload:
            response = client.post(reverse("api:user-list"), field)
            assert response.status_code == 400

    @pytest.mark.django_db
    def test_login_user(self, user, client):
        response = client.post(
            reverse("api:login"), dict(email=USER_EMAIL, password=PASSWORD)
        )
        assert response.status_code == 200
        assert "auth_token" in response.data
        assert len(response.data["auth_token"]) == 40

    @pytest.mark.django_db
    def test_login_user_fail(self, client):
        response = client.post(
            reverse("api:login"), dict(email=USER_EMAIL, password=PASSWORD)
        )
        assert response.status_code == 400
        assert response.data["non_field_errors"][0] == (
                "Unable to log in with provided credentials.")

    @pytest.mark.django_db
    def test_logout_user(self, auth_client):
        response = auth_client.post(reverse("api:logout"))

        assert response.status_code == 204

    @pytest.mark.django_db
    def test_get_me(self, user, auth_client):
        response = auth_client.get(reverse("api:user-me"))

        assert response.status_code == 200
        assert response.data["id"] == user.id
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email
        assert "password" not in response.data

    # @pytest.mark.django_db
    # def test_patch_me_first_name(self, user, auth_client):
    #     payload = {"first_name": FIRST_NAME, }
    #     response = auth_client.patch(reverse("api:user-me"), payload)
    #
    #     assert response.status_code == 200
    #     assert response.data["id"] == user.id
    #     assert response.data["first_name"] == user.first_name == FIRST_NAME
    #
    # @pytest.mark.django_db
    # def test_patch_me_anonymous_fail(self, client):
    #     payload = {"first_name": FIRST_NAME,}
    #     response = client.patch(reverse("api:user-me"), payload)
    #
    #     assert response.status_code == 401
    #     assert response.data["type"] == "client_error"
    #     assert response.data["errors"][0]["code"] == "not_authenticated"
    #
    #
    # @pytest.mark.django_db
    # def test_delete_me(self, auth_client, user):
    #     response = auth_client.delete(reverse("api:user-me"))
    #
    #     assert response.status_code == 200
    #     assert response.data["username"] == user.username
    #     assert response.data["email"] == user.email
    #
    # @pytest.mark.django_db
    # def test_delete_me_anonymous_fail(self, client):
    #     response = client.delete(reverse("api:user-me"))
    #
    #     assert response.status_code == 401
    #     assert response.data["type"] == "client_error"
    #     assert response.data["errors"][0]["code"] == "not_authenticated"
