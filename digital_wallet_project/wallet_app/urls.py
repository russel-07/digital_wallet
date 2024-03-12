from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import WalletViewSet
from .views import TransactionListCreate, TransactionRetrieve


router = DefaultRouter()
router.register('wallets/transactions', TransactionListCreate,
                basename='Transaction')
router.register(r'wallets/(?P<wallet_name>[0-9, A-Z]+)/transactions',
                TransactionRetrieve, basename='Transaction')
router.register('wallets', WalletViewSet, basename='Wallet')


urlpatterns = [
    path('', include(router.urls)),
]
