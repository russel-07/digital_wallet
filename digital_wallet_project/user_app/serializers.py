from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def validate_password(self, value):
        password_validation.validate_password(value)
        return make_password(value)
