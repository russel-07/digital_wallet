from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ('post')
