from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'name', 'payment_system', 'currency',
                  'balance', 'created_on', 'modified_on']
        read_only_fields = ['name']


class TransactionSerializer(serializers.ModelSerializer):

    sender = serializers.ReadOnlyField(source='sender.name')
    receiver = serializers.ReadOnlyField(source='receiver.name')

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount',
                  'commission', 'status', 'timestamp']
        read_only_fields = ['commission', 'status']
