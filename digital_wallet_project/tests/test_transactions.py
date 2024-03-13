import pytest


class TestCreateTransaction:

    @pytest.mark.django_db
    def test_paid_transaction(self, client, get_user_1_token,
                              post_paid_transaction_data, transaction_url):
        response = client.post(transaction_url,
                               data=post_paid_transaction_data,
                               headers=get_user_1_token)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_failed_transaction_with_other_currency(
            self, client, get_user_1_token, transaction_url,
            post_failed_transaction_data_with_other_currency):
        response = client.post(
            transaction_url, headers=get_user_1_token,
            data=post_failed_transaction_data_with_other_currency)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_failed_transaction_with_missing_amount_money(
            self, client, get_user_1_token, transaction_url,
            post_failed_transaction_data_with_missing_amount_money):
        response = client.post(
            transaction_url, headers=get_user_1_token,
            data=post_failed_transaction_data_with_missing_amount_money)
        assert response.status_code == 400


class TestGetTransaction:

    @pytest.mark.django_db
    def test_list_user_transactions(self, client, transaction,
                                    get_user_1_token, transaction_url):
        response = client.get(transaction_url, headers=get_user_1_token)
        assert response.status_code == 200
        assert len(response.json()) == 1

    @pytest.mark.django_db
    def test_get_user_transaction_by_owner(
            self, client, get_user_1_token, transaction_url_with_id):
        response = client.get(transaction_url_with_id,
                              headers=get_user_1_token)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_user_transaction_by_not_owner(
            self, client, get_user_2_token, transaction_url_with_id):
        response = client.get(transaction_url_with_id,
                              headers=get_user_2_token)
        assert response.status_code == 404


class TestGetWalletTransactions:

    @pytest.mark.django_db
    def test_get_user_transaction_by_owner(
            self, client, wallet_transactions_url, get_user_1_token):
        response = client.get(wallet_transactions_url,
                              headers=get_user_1_token)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_user_transaction_by_not_owner(
            self, client, wallet_transactions_url, get_user_2_token):
        response = client.get(wallet_transactions_url,
                              headers=get_user_2_token)
        assert response.status_code == 403
