from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from datetime import datetime

from .models import Wallet, Transaction
from .serializers import UserSerializer
from .serializers import WalletSerializer, TransactionSerializer
from .permissions import IsWalletOwner, IsTransactionAuthor
from .utils import get_wallet_name, get_bank_bonus, get_commission
from .utils import check_currency_compatibility, check_money_in_wallet
from .utils import check_user_wallet_count


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ('post')


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'name'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.wallets.all()

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user)
        if not check_user_wallet_count(user):
            raise PermissionDenied('Превышено количество кошельков '
                                   'на одного пользователя.')
        name = get_wallet_name()
        currency = self.request.data['currency']
        balance = get_bank_bonus(currency)
        serializer.save(owner=user, name=name, balance=balance)


class TransactionListCreate(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsWalletOwner]
    http_method_names = ('get', 'post')

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        wallets_transactions = Transaction.objects.none()
        user_wallets = user.wallets.all()
        for wallet in user_wallets:
            wallets_transactions |= wallet.outgoing_transactions.all()
        return wallets_transactions

    def perform_create(self, serializer):
        status = 'failed'
        sender = get_object_or_404(Wallet, name=self.request
                                   .data['sender'])
        receiver = get_object_or_404(Wallet, name=self.request
                                     .data['receiver'])
        amount = float(self.request.data['transfer_amount'])
        commission = get_commission(sender, receiver, amount)
        full_amount = amount + commission
        if check_currency_compatibility(sender, receiver):
            if check_money_in_wallet(sender, full_amount):
                with transaction.atomic():
                    sender.balance -= Decimal(full_amount)
                    sender.modified_on = datetime.now()
                    sender.save()
                    receiver.balance += Decimal(amount)
                    receiver.modified_on = datetime.now()
                    receiver.save()
                    status = 'paid'
            else:
                failed_msg = 'Недостаточно средств для перевода.'
        else:
            failed_msg = ('Перевод средств между кошельками'
                          ' с разной валютой невозможен.')
        serializer.save(sender=sender, receiver=receiver,
                        transfer_amount=amount, commission=commission,
                        status=status)
        if status == 'failed':
            raise PermissionDenied(failed_msg)


class TransactionRetrieve(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsTransactionAuthor]
    http_method_names = ('get')

    def get_queryset(self):
        param = self.kwargs.get('param')
        if param.isdigit():
            transaction = Transaction.objects.filter(pk=param)
            return transaction
        else:
            wallet = get_object_or_404(Wallet, name=param)
            wallet_transactions = (Transaction.objects
                                   .filter(Q(sender=wallet) |
                                           Q(receiver=wallet)))
            return wallet_transactions
