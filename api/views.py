from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import AccountSerializer, TransactionSerializer
from core.models import Account, Transaction


# Create your views here.

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        serializer = AccountSerializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=True, url_path='transactions', url_name='get-account-transactions')
    def get_transactions(self, request, pk):
        account = self.get_object()
        transactions = TransactionSerializer(account.transaction_set.all(), many=True)
        return Response(transactions.data, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        return super(TransactionViewSet, self).create(request=request)
