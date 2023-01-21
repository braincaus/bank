import uuid

from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'SAVINGS'),
        ('checking', 'CHECKING'),
    )
    account_number = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPES)
    customer_name = models.CharField(max_length=250)
    balance = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.account_number)


class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('deposit', 'DEPOSIT'),
        ('withdraw', 'WITHDRAW'),
    )
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    account = models.ForeignKey(Account, to_field='account_number', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    amount = models.FloatField(
        validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
