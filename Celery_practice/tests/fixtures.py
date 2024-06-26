import pytest
from rest_framework.test import APIClient

from users.models import User

INVALID_ID = 1000

USER = "test_user"
USER_EMAIL = "test_user@test.com"
ADMIN = "TestAdmin"
ADMIN_EMAIL = "testadmin@good_food.fake"
PASSWORD = "test_password"
FIRST_NAME = "First"


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username=ADMIN, email=ADMIN_EMAIL, password=PASSWORD, is_staff=True
    )


@pytest.fixture
def user():
    return User.objects.create_user(
        username=USER,
        email=USER_EMAIL,
        password=PASSWORD,
        first_name=FIRST_NAME
    )


@pytest.fixture
def user1(django_user_model):
    return django_user_model.objects.create_user(
        username="Testuser1",
        email="testuser1@good_food.fake",
        password="1234567",
    )


@pytest.fixture
def user2(django_user_model):
    return django_user_model.objects.create_user(
        username="Testuser2",
        email="testuser2@good_food.fake",
        password="1234567"
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client_first(client, user2):
    client.force_authenticate(user=user2)
    return client


@pytest.fixture
def auth_admin(client, admin):
    client.force_authenticate(user=admin)
    return client
