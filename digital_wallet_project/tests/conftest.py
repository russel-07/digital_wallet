import pytest

from rest_framework_simplejwt.tokens import RefreshToken

from wallet_app.models import Wallet, Transaction


@pytest.fixture
def user_1(django_user_model):
    user = django_user_model.objects.create_user(username='test_user_1',
                                                 password='test_password')
    yield user
    user.delete()


@pytest.fixture
def user_2(django_user_model):
    user = django_user_model.objects.create_user(username='test_user_2',
                                                 password='test_password')
    yield user
    user.delete()


@pytest.fixture
def get_user_1_token(user_1):
    refresh = RefreshToken.for_user(user_1)
    token = {'Authorization': f'Bearer {str(refresh.access_token)}'}
    return token


@pytest.fixture
def get_user_2_token(user_2):
    refresh = RefreshToken.for_user(user_2)
    token = {'Authorization': f'Bearer {str(refresh.access_token)}'}
    return token


@pytest.fixture
def wallet_1_rub(user_1):
    wallet = Wallet.objects.create(name='RUB12345', owner=user_1, balance=100,
                                   currency='rub', payment_system='visa')
    yield wallet
    wallet.delete()


@pytest.fixture
def wallet_2_rub(user_2):
    wallet = Wallet.objects.create(name='RUB67890', owner=user_2, balance=100,
                                   currency='rub', payment_system='visa')
    yield wallet
    wallet.delete()


@pytest.fixture
def wallet_2_usd(user_2):
    wallet = Wallet.objects.create(name='USD12345', owner=user_2, balance=3,
                                   currency='usd', payment_system='visa')
    yield wallet
    wallet.delete()


@pytest.fixture
def create_five_wallets(user_1):
    for i in range(5):
        Wallet.objects.create(name=123456 + i, owner=user_1, balance=100,
                              currency='rub', payment_system='visa')
    yield
    Wallet.objects.all().delete()


@pytest.fixture
def transaction(wallet_1_rub, wallet_2_rub):
    transaction = Transaction.objects.create(sender=wallet_1_rub,
                                             receiver=wallet_2_rub,
                                             transfer_amount=50,
                                             commission=5, status='paid')
    yield transaction
    transaction.delete()


@pytest.fixture
def user_url():
    return '/api/v1/user/'


@pytest.fixture
def wallet_url():
    return '/api/v1/wallets/'


@pytest.fixture
def wallet_url_with_wallet_name(wallet_url, wallet_1_rub):
    return f'{wallet_url}{wallet_1_rub.name}/'


@pytest.fixture
def transaction_url():
    return '/api/v1/wallets/transactions/'


@pytest.fixture
def transaction_url_with_id(transaction_url, transaction):
    return f'{transaction_url}{transaction.id}/'


@pytest.fixture
def wallet_transactions_url(transaction):
    return f'/api/v1/wallets/{transaction.sender}/transactions/'


@pytest.fixture
def post_success_user_data():
    data = {'username': 'test_user', 'password': 'test_password'}
    return data


@pytest.fixture
def post_failed_user_data():
    data = {'username': 'test_user', 'password': '123'}
    return data


@pytest.fixture
def post_wallet_data():
    data = {'currency': 'rub', 'payment_system': 'mastercard'}
    return data


@pytest.fixture
def post_paid_transaction_data(wallet_1_rub, wallet_2_rub):
    data = {
        'sender': wallet_1_rub,
        'receiver': wallet_2_rub,
        'transfer_amount': 50
        }
    return data


@pytest.fixture
def post_failed_transaction_data_with_other_currency(
        wallet_1_rub, wallet_2_usd):
    data = {
        'sender': wallet_1_rub,
        'receiver': wallet_2_usd,
        'transfer_amount': 50
        }
    return data


@pytest.fixture
def post_failed_transaction_data_with_missing_amount_money(
        wallet_1_rub, wallet_2_rub):
    data = {
        'sender': wallet_1_rub,
        'receiver': wallet_2_rub,
        'transfer_amount': 200
        }
    return data
