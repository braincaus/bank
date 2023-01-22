import uuid

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class AccountType(models.Model):
    type = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.type


class Account(models.Model):
    account_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=250)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.account_number)


class TransactionType(models.Model):
    OPERATORS = (
        ('+', '+'),
        ('-', '-'),
    )
    type = models.CharField(max_length=20, unique=True)
    operator = models.CharField(max_length=1, default='+', choices=OPERATORS)

    def __str__(self):
        return self.type


class TransactionStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status


class Transaction(models.Model):
    TRANSACTION_ERRORS = (
        ('without_founds', 'WITHOUT FOUNDS'),
    )
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    account = models.ForeignKey(Account, to_field='account_number', on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])

    status = models.ForeignKey(TransactionStatus, default=1, on_delete=models.CASCADE)
    error = models.CharField(max_length=20, choices=TRANSACTION_ERRORS, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
