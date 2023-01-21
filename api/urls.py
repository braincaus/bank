from django.urls import path, include
from rest_framework import routers

from api.views import AccountViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet, 'accounts')
router.register(r'transactions', TransactionViewSet, 'transactions')

# import pprint
# pprint.pprint(router.get_urls())

urlpatterns = [
    path('', include(router.urls)),
]
