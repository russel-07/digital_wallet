import pytest


@pytest.fixture
def trans(client, wallet, other_rub_wallet, get_auth_user_token):
    data = {
        'sender': wallet,
        'receiver': other_rub_wallet,
        'transfer_amount': 10
        }
    response = client.post('/api/v1/wallets/transactions/', data=data,
                           headers=get_auth_user_token)
    return response.json()['id']
