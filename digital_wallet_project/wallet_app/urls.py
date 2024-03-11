from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView

# from .views import UserViewSet
from .views import WalletViewSet
from .views import TransactionListCreate, TransactionRetrieve


router = DefaultRouter()
# router.register('user', UserViewSet, basename='User')
router.register(r'wallets/transactions/(?P<param>[0-9, A-Z]+)',
                TransactionRetrieve, basename='Transaction')
router.register('wallets/transactions', TransactionListCreate,
                basename='Transaction')
router.register('wallets', WalletViewSet, basename='Wallet')


urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
