import pytest


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='test_user',
                                                 password='test_password')


@pytest.fixture
def get_auth_user_token(user, client):
    data = {'username': 'test_user', 'password': 'test_password'}
    response = client.post('/api/v1/token/', data=data)
    token = {'Authorization': f"Bearer {response.json()['access']}"}
    return token


@pytest.fixture
def other_user(django_user_model):
    return django_user_model.objects.create_user(username='test_other_user',
                                                 password='test_password')


@pytest.fixture
def get_auth_other_user_token(other_user, client):
    data = {'username': 'test_other_user', 'password': 'test_password'}
    response = client.post('/api/v1/token/', data=data)
    token = {'Authorization': f"Bearer {response.json()['access']}"}
    return token
