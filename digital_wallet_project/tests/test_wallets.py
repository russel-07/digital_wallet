import pytest

from wallet_app.models import Wallet


class TestCreateWallet:

    def test_create_wallet_by_auth_user(
            self, client, get_user_1_token, wallet_url, post_wallet_data):
        assert Wallet.objects.count() == 0
        response = client.post(wallet_url, data=post_wallet_data,
                               headers=get_user_1_token)
        assert response.status_code == 201
        assert Wallet.objects.count() == 1

    @pytest.mark.django_db(transaction=True)
    def test_create_wallet_by_unauth_user(
            self, client, wallet_url, post_wallet_data):
        response = client.post(wallet_url, data=post_wallet_data)
        assert response.status_code == 401
        assert Wallet.objects.count() == 0

    def test_create_max_wallet_count(
            self, client, get_user_1_token, wallet_url,
            post_wallet_data, create_five_wallets):
        assert Wallet.objects.count() == 5
        response = client.post(wallet_url, data=post_wallet_data,
                               headers=get_user_1_token)
        assert response.status_code == 400
        assert Wallet.objects.count() == 5


class TestGetWallet:

    @pytest.mark.django_db(transaction=True)
    def test_list_user_wallets(self, client, wallet_1_rub,
                               get_user_1_token, wallet_url):
        assert Wallet.objects.count() == 1
        response = client.get(wallet_url, headers=get_user_1_token)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_user_wallet_by_owner(self, client, get_user_1_token,
                                      wallet_url_with_wallet_name):
        response = client.get(wallet_url_with_wallet_name,
                              headers=get_user_1_token)
        assert response.status_code == 200

    def test_get_user_wallet_by_not_owner(self, client, get_user_2_token,
                                          wallet_url_with_wallet_name):
        response = client.get(wallet_url_with_wallet_name,
                              headers=get_user_2_token)
        assert response.status_code == 404


class TestDeleteWallet:

    def test_delete_wallet_by_owner(self, client, get_user_1_token,
                                    wallet_url_with_wallet_name):
        assert Wallet.objects.count() == 1
        response = client.delete(wallet_url_with_wallet_name,
                                 headers=get_user_1_token)
        assert response.status_code == 204
        assert Wallet.objects.count() == 0
