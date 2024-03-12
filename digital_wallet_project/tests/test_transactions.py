import pytest

from wallet_app.models import Transaction


class TestCreateTransaction:

    @pytest.mark.django_db(transaction=True)
    def test_paid_transaction(self, client, get_auth_user_token,
                              wallet, other_rub_wallet):
        data = {
            'sender': wallet,
            'receiver': other_rub_wallet,
            'transfer_amount': 50
            }
        response = client.post('/api/v1/wallets/transactions/', data=data,
                               headers=get_auth_user_token)
        assert response.status_code == 201, 'Новая транзакция не создана.'

    @pytest.mark.django_db(transaction=True)
    def test_failed_transaction_with_other_currency(
            self, client, get_auth_user_token, wallet, other_usd_wallet):
        data = {
            'sender': wallet,
            'receiver': other_usd_wallet,
            'transfer_amount': 50
            }
        response = client.post('/api/v1/wallets/transactions/', data=data,
                               headers=get_auth_user_token)
        assert response.status_code == 400, \
            'Cоздана транзакция между кошельками с разной валютой.'

    @pytest.mark.django_db(transaction=True)
    def test_failed_transaction_with_missing_amount_money(
            self, client, get_auth_user_token, wallet, other_rub_wallet):
        data = {
            'sender': wallet,
            'receiver': other_rub_wallet,
            'transfer_amount': 200
            }
        response = client.post('/api/v1/wallets/transactions/', data=data,
                               headers=get_auth_user_token)
        assert response.status_code == 400, \
            'Cоздана транзакция между кошельком на котором не хватает средств'


class TestGetTransaction:

    def test_list_user_transactions(self, client, trans,
                                    get_auth_user_token):
        response = client.get('/api/v1/wallets/transactions/',
                              headers=get_auth_user_token)
        assert response.status_code == 200, 'Транзакции не отображается.'
        assert len(response.json()) == 1, \
            'Отображается неверное количество транзакций.'

    def test_get_user_transaction_by_owner(self, client, trans,
                                           get_auth_user_token):
        response = client.get(f'/api/v1/wallets/transactions/{trans}/',
                              headers=get_auth_user_token)
        assert response.status_code == 200, 'Транзакция не отображается.'

    def test_get_user_transaction_by_not_owner(self, client, trans,
                                               get_auth_other_user_token):
        response = client.get(f'/api/v1/wallets/transactions/{trans}/',
                              headers=get_auth_other_user_token)
        assert response.status_code == 404, \
            'Транзакция отображается другому пользователю.'


class TestGetWalletTransactions:

    def test_get_user_transaction_by_owner(self, client, trans,
                                           get_auth_user_token):
        wallet_name = getattr(Transaction.objects.get(id=trans), 'sender')
        response = client.get(f'/api/v1/wallets/{wallet_name}/transactions/',
                              headers=get_auth_user_token)
        assert response.status_code == 200, \
            'Транзакции кошелька не отображаются.'

    def test_get_user_transaction_by_not_owner(self, client, trans,
                                               get_auth_other_user_token):
        wallet_name = getattr(Transaction.objects.get(id=trans), 'sender')
        response = client.get(f'/api/v1/wallets/{wallet_name}/transactions/',
                              headers=get_auth_other_user_token)
        assert response.status_code == 403, \
            'Транзакции кошелька отображаются другому пользователю.'
