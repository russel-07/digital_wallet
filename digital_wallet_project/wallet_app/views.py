from django.db import transaction
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from decimal import Decimal

from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from .permissions import IsOwner
from .utils import get_wallet_name, get_bank_bonus, get_commission
from .utils import check_currency_compatibility, check_money_in_wallet
from .utils import check_user_wallet_count


User = get_user_model()


class WalletViewSet(viewsets.ModelViewSet):
    serializer_class = WalletSerializer
    http_method_names = ('get', 'post', 'delete')
    lookup_field = 'name'

    def get_queryset(self):
        return Wallet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if not check_user_wallet_count(self.request.user):
            raise ValidationError('Превышено количество кошельков '
                                  'на одного пользователя.')
        name = get_wallet_name()
        currency = self.request.data['currency']
        balance = get_bank_bonus(currency)
        serializer.save(owner=self.request.user, name=name, balance=balance)


class TransactionListCreate(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    http_method_names = ('get', 'post')

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Transaction.objects.filter(sender__owner=self.request.user)

    def perform_create(self, serializer):
        status = 'failed'
        sender = get_object_or_404(Wallet, name=self.request
                                   .data['sender'])
        receiver = get_object_or_404(Wallet, name=self.request
                                     .data['receiver'])
        amount = float(self.request.data['transfer_amount'])
        commission = get_commission(sender, receiver, amount)
        full_amount = amount + commission
        check_money = check_money_in_wallet(sender, full_amount)
        if (check_currency_compatibility(sender, receiver) and
                check_money):
            with transaction.atomic():
                sender.balance -= Decimal(full_amount)
                sender.save()
                receiver.balance += Decimal(amount)
                receiver.save()
                status = 'paid'
        elif not check_money:
            failed_msg = 'Недостаточно средств для перевода.'
        else:
            failed_msg = ('Перевод средств между кошельками'
                          ' с разной валютой невозможен.')
        serializer.save(sender=sender, receiver=receiver,
                        transfer_amount=amount, commission=commission,
                        status=status)
        if status == 'failed':
            raise ValidationError(failed_msg)


class TransactionRetrieve(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwner]
    http_method_names = ('get')

    def get_queryset(self):
        wallet = get_object_or_404(Wallet, name=self.kwargs
                                   .get('wallet_name'))
        wallet_transactions = (Transaction.objects
                               .filter(Q(sender=wallet) | Q(receiver=wallet)))
        return wallet_transactions
