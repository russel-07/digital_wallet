from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import Wallet


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if 'wallet_name' in view.kwargs.keys():
            wallet = get_object_or_404(Wallet, name=view.kwargs
                                       .get('wallet_name'))
        else:
            wallet = get_object_or_404(Wallet, name=request.data['sender'])
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user == wallet.owner
        )
