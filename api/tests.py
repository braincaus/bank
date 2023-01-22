import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.tasks import apply_transaction


# Create your tests here.


class AccountTests(APITestCase):

    def test_get_all_accounts(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('accounts-list')
        response = self.client.get(url,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        url = reverse('accounts-list')
        data = {
            "account_type": 1,
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_account(self):
        url = reverse('accounts-list')

        data = {
            "account_type": 1,
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        account_number = response.json()['account_number']

        url = reverse('accounts-detail', args=[account_number])
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_deposit(self):
        url = reverse('accounts-list')

        data = {
            "account_type": 1,
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        account_number = response.json()['account_number']

        url = reverse('transactions-list')
        data = {
            "transaction_type": 1,
            "amount": 300.0,
            "account": account_number
        }

        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('accounts-detail', args=[account_number])
        response = self.client.get(path=url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['balance'], 800.00)

    def test_create_withdraw(self):
        url = reverse('accounts-list')

        data = {
            "account_type": 1,
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        account_number = response.json()['account_number']

        url = reverse('transactions-list')
        data = {
            "transaction_type": 2,
            "amount": 300.0,
            "account": account_number
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('accounts-detail', args=[account_number])
        response = self.client.get(path=url)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result['balance'], 200.00)

    def test_fail_withdraw(self):
        url = reverse('accounts-list')

        data = {
            "account_type": 1,
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        account_number = response.json()['account_number']

        url = reverse('transactions-list')
        data = {
            "transaction_type": 2,
            "amount": 800.0,
            "account": account_number
        }
        response = self.client.post(path=url, data=data, format='json')
        transaction_id = response.json()['transaction_id']

        apply_transaction(transaction_id=transaction_id)

        url = reverse('transactions-detail', args=[transaction_id])
        response = self.client.get(path=url)
        _status = response.json()['status']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(_status, 3)
