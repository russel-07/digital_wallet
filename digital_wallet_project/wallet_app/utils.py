import environ
import string
import secrets

from pathlib import Path

from .models import Wallet


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / '../.env')


def get_wallet_name() -> str:
    wallet_name = ''.join(secrets.choice(string.ascii_uppercase+string.digits)
                          for _ in range(int(env('WALLET_NAME_SYM_COUNT'))))
    return wallet_name


def get_bank_bonus(currency: str) -> float:
    match currency:
        case 'rub':
            bonus = env('BANK_BONUS_RUB')
        case 'usd':
            bonus = env('BANK_BONUS_USD')
        case 'eur':
            bonus = env('BANK_BONUS_EUR')
    return float(bonus)


def check_user_wallet_count(user) -> bool:
    return user.wallets.count() < int(env('MAX_USER_WALLET_COUNTER'))


def check_currency_compatibility(sender_wallet: Wallet,
                                 receiver_wallet: Wallet) -> bool:
    return sender_wallet.currency == receiver_wallet.currency


def check_money_in_wallet(sender_wallet: Wallet,
                          full_amount: float) -> bool:
    return sender_wallet.balance >= full_amount


def get_commission(sender_wallet: Wallet, receiver_wallet: Wallet,
                   transfer_amount: float) -> float:
    commission = 0.00
    if sender_wallet.owner != receiver_wallet.owner:
        commission = transfer_amount * float(env('COMMISSION_COEFF'))
    return commission
