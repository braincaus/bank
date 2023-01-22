from rest_framework import serializers
from rest_framework.exceptions import APIException

from core.models import Account, Transaction


class WithoutFoundsException(APIException):
    status_code = 409
    default_detail = 'Without founds for this operation.'
    default_code = 'without_founds'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['status', 'error', ]


class TransactionCreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']


class AccountSerializer(serializers.ModelSerializer):
    initial_deposit = TransactionCreateAccountSerializer(write_only=True)

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['balance', ]

    def create(self, validated_data):
        transaction = validated_data.pop('initial_deposit')
        validated_data['balance'] = transaction.get('amount')
        result = super(AccountSerializer, self).create(validated_data=validated_data)
        result.transaction_set.create(transaction_type_id=1, status_id=2, amount=transaction.get('amount'))
        return result
