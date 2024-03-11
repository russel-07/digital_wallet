# from django.contrib.auth import get_user_model, password_validation
# from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Wallet, Transaction


# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):

#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'username', 'password']

#     def validate_password(self, value):
#         password_validation.validate_password(value)
#         return make_password(value)


class WalletSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    name = serializers.ReadOnlyField()

    class Meta:
        model = Wallet
        fields = ['id', 'owner', 'name', 'payment_system', 'currency',
                  'balance', 'created_on', 'modified_on']


class TransactionSerializer(serializers.ModelSerializer):

    sender = serializers.SlugRelatedField(many=False, slug_field='name',
                                          read_only=True)
    receiver = serializers.SlugRelatedField(many=False, slug_field='name',
                                            read_only=True)
    transfer_amount = serializers.ReadOnlyField()
    commission = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'transfer_amount',
                  'commission', 'status', 'timestamp']
