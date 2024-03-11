import string
import secrets

from .models import Wallet


WALLET_NAME_SYM_COUNT = 8
BANK_BONUS_RUB = 100.00
BANK_BONUS_USD = 3.00
BANK_BONUS_EUR = 3.00
MAX_USER_WALLET_COUNTER = 5
COMMISSION_COEFF = 0.10


def get_wallet_name() -> str:
    wallet_name = ''.join(secrets.choice(string.ascii_uppercase+string.digits)
                          for _ in range(WALLET_NAME_SYM_COUNT))
    return wallet_name


def get_bank_bonus(currency: str) -> float:
    match currency:
        case 'rub':
            bonus = BANK_BONUS_RUB
        case 'usd':
            bonus = BANK_BONUS_USD
        case 'eur':
            bonus = BANK_BONUS_EUR
    return bonus


def check_user_wallet_count(user) -> bool:
    return user.wallets.count() < MAX_USER_WALLET_COUNTER


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
        commission = transfer_amount * COMMISSION_COEFF
    return commission
