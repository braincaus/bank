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

    def create(self, validated_data):
        if validated_data['transaction_type'] == 'withdraw':
            account = validated_data['account']
            if account.balance < validated_data['amount']:
                raise WithoutFoundsException
        result = super(TransactionSerializer, self).create(validated_data=validated_data)
        if result.transaction_type == 'deposit':
            result.account.balance += result.amount
        elif result.transaction_type == 'withdraw':
            result.account.balance -= result.amount
        result.account.save()
        return result


class TransactionCreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']

    def create(self, validated_data):
        result = super(TransactionCreateAccountSerializer, self).create(validated_data=validated_data)

        return result


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
        result.transaction_set.create(transaction_type='deposit', amount=transaction.get('amount'))
        return result
