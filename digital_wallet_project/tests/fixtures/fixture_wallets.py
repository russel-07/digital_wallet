import pytest


@pytest.fixture
def wallet(user, client, get_auth_user_token):
    data = {'currency': 'rub', 'payment_system': 'mastercard'}
    response = client.post('/api/v1/wallets/', data=data,
                           headers=get_auth_user_token)
    return response.json()['name']


@pytest.fixture
def other_rub_wallet(other_user, client, get_auth_other_user_token):
    data = {'currency': 'rub', 'payment_system': 'mastercard'}
    response = client.post('/api/v1/wallets/', data=data,
                           headers=get_auth_other_user_token)
    return response.json()['name']


@pytest.fixture
def other_usd_wallet(other_user, client, get_auth_other_user_token):
    data = {'currency': 'usd', 'payment_system': 'mastercard'}
    response = client.post('/api/v1/wallets/', data=data,
                           headers=get_auth_other_user_token)
    return response.json()['name']
