from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import Wallet, Transaction


class IsWalletOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            wallet = get_object_or_404(Wallet, name=request.data['sender'])
            return bool(
                request.user and
                request.user.is_authenticated and
                request.user == wallet.owner
            )
        return True


class IsTransactionAuthor(BasePermission):
    def has_permission(self, request, view):
        param = view.kwargs.get('param')
        if param.isdigit():
            transaction = get_object_or_404(Transaction, pk=param)
            return bool(
                request.user and
                request.user.is_authenticated and
                (request.user == transaction.sender.owner or
                 request.user == transaction.receiver.owner)
                )
        wallet = get_object_or_404(Wallet, name=param)
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user == wallet.owner
        )
