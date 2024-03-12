import pytest

from django.conf import settings

from wallet_app.models import Wallet


class TestCreateWallet:

    @pytest.mark.django_db(transaction=True)
    def test_create_wallet_by_auth_user(self, client, get_auth_user_token):
        data = {'currency': 'rub', 'payment_system': 'mastercard'}
        response = client.post('/api/v1/wallets/', data=data,
                               headers=get_auth_user_token)
        assert response.status_code == 201, 'Новый кошелек не создан.'
        assert Wallet.objects.count() == 1, 'Новый кошелек не создан.'

    @pytest.mark.django_db(transaction=True)
    def test_create_wallet_by_unauth_user(self, client):
        data = {'currency': 'rub', 'payment_system': 'mastercard'}
        response = client.post('/api/v1/wallets/', data=data)
        assert response.status_code == 401, \
            'Новый кошелек создан неавторизованным пользователем.'
        assert Wallet.objects.count() == 0, \
            'Новый кошелек создан неавторизованным пользователем.'

    @pytest.mark.django_db(transaction=True)
    def test_create_max_wallet_count(self, client, get_auth_user_token):
        data = {'currency': 'rub', 'payment_system': 'mastercard'}
        for _ in range(settings.WALLET_NAME_SYM_COUNT + 1):
            response = client.post('/api/v1/wallets/', data=data,
                                   headers=get_auth_user_token)
        assert response.status_code == 400, \
            'Превышено количество кошельков на одного пользователя.'
        assert Wallet.objects.count() == 5, \
            'Превышено количество кошельков на одного пользователя.'


class TestGetWallet:

    def test_list_user_wallets(self, client, wallet, get_auth_user_token):
        response = client.get('/api/v1/wallets/', headers=get_auth_user_token)
        assert response.status_code == 200, 'Кошельки не отображаются.'
        assert len(response.json()) == 1, \
            'Отображается неверное количество кошельков.'

    def test_get_user_wallet_by_owner(self, client, wallet,
                                      get_auth_user_token):
        response = client.get(f'/api/v1/wallets/{wallet}/',
                              headers=get_auth_user_token)
        assert response.status_code == 200, 'Кошелек не отображается.'

    def test_get_user_wallet_by_not_owner(self, client, wallet,
                                          get_auth_other_user_token):
        response = client.get(f'/api/v1/wallets/{wallet}/',
                              headers=get_auth_other_user_token)
        assert response.status_code == 404, \
            'Кошелек отображается другому пользователю.'


class TestDeleteWallet:

    def test_delete_wallet_by_owner(self, client, wallet,
                                    get_auth_user_token):
        response = client.delete(f'/api/v1/wallets/{wallet}/',
                                 headers=get_auth_user_token)
        assert response.status_code == 204, 'Кошелек не удален.'
