from celery import shared_task

from core.models import Transaction


@shared_task(name='apply_transaction')
def apply_transaction(transaction_id: int):
    transaction = Transaction.objects.get(pk=transaction_id)
    if transaction.status_id == 1:
        if transaction.transaction_type.operator == '+':
            transaction.status_id = 2
            transaction.account.balance += transaction.amount

        elif transaction.transaction_type.operator == '-':
            if transaction.account.balance > transaction.amount:
                transaction.status_id = 2
                transaction.account.balance -= transaction.amount
            else:
                transaction.status_id = 3
                transaction.error = 'without_founds'

        transaction.account.save()
        transaction.save()

        return True
    return False
