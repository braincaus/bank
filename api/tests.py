import uuid

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.


class AccountTests(APITestCase):

    def test_get_all_accounts(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('accounts-list')
        response = self.client.get(url,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account_with_account_number_declared(self):
        url = reverse('accounts-list')
        data = {
            "account_number": str(uuid.uuid4()),
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_account_without_account_number_declared(self):
        url = reverse('accounts-list')
        data = {
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_duplicated_account(self):
        url = reverse('accounts-list')
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_account(self):
        url = reverse('accounts-list')

        data = {
            "account_type": "savings",
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

    def test_create_deposit_with_transaction_id_declared(self):
        url = reverse('accounts-list')
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('transactions-list')
        transaction_id = str(uuid.uuid4())
        data = {
            "transaction_id": transaction_id,
            "transaction_type": "deposit",
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

    def test_create_deposit_without_transaction_id_declared(self):
        url = reverse('accounts-list')
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('transactions-list')
        data = {
            "transaction_type": "deposit",
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
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('transactions-list')
        data = {
            "transaction_type": "withdraw",
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


    def test__fail_withdraw(self):
        url = reverse('accounts-list')
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('transactions-list')
        data = {
            "transaction_type": "withdraw",
            "amount": 800.0,
            "account": account_number
        }
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_fail_duplicated_transaction_id(self):
        url = reverse('accounts-list')
        account_number = str(uuid.uuid4())

        data = {
            "account_number": account_number,
            "account_type": "savings",
            "customer_name": "Efrain Rodriguez",
            "initial_deposit": {
                "amount": 500.0
            }
        }
        response = self.client.post(path=url, data=data, format='json')

        url = reverse('transactions-list')
        transaction_id = str(uuid.uuid4())
        data = {
            "transaction_id": transaction_id,
            "transaction_type": "deposit",
            "amount": 300.0,
            "account": account_number
        }
        response = self.client.post(path=url, data=data, format='json')
        response = self.client.post(path=url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
