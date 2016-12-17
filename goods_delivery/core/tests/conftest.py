import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def authorized_client():
    user = mixer.blend(User, username="a")
    token = mixer.blend(Token, user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture
def unauthorized_client():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token XPTO')
    return client
