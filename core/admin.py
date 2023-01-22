from django.contrib import admin

from core.models import AccountType, Account, TransactionType, TransactionStatus, Transaction


# Register your models here.


@admin.register(AccountType)
class AccountTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionStatus)
class TransactionStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass

