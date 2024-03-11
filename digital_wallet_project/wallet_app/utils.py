import string
import secrets

from .models import Wallet


def get_wallet_name() -> str:
    SYM_COUNT = 8
    wallet_name = ''.join(secrets.choice(string.ascii_uppercase+string.digits)
                          for _ in range(SYM_COUNT))
    return wallet_name


def get_bank_bonus(currency: str) -> float:
    RUB_BONUS = 100.00
    USD_EUR_BONUS = 3.00
    if currency == 'rub':
        bonus = RUB_BONUS
    else:
        bonus = USD_EUR_BONUS
    return bonus


def check_user_wallet_count(user) -> bool:
    MAX_USER_WALLET_COUNTER = 5
    user_wallet_counter = user.wallets.count()
    if user_wallet_counter >= MAX_USER_WALLET_COUNTER:
        return False
    return True


def check_currency_compatibility(sender_wallet: Wallet,
                                 receiver_wallet: Wallet) -> bool:
    if sender_wallet.currency != receiver_wallet.currency:
        return False
    return True


def check_money_in_wallet(sender_wallet: Wallet,
                          full_amount: float) -> bool:
    if sender_wallet.balance < full_amount:
        return False
    return True


def get_commission(sender_wallet: Wallet, receiver_wallet: Wallet,
                   transfer_amount: float) -> float:
    COMMISSION_COEFF = 0.10
    commission = 0.00
    if sender_wallet.owner != receiver_wallet.owner:
        commission = transfer_amount * COMMISSION_COEFF
    return commission
