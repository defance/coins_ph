from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITransactionTestCase, APITestCase

from coins_ph.core.models import Payment
from tests.factories import AccountFactory, CurrencyFactory, PaymentFactory


class TestPaymentCreation(APITransactionTestCase):
    def setUp(self):
        self.url = reverse('api:payments')
        self.currency = CurrencyFactory()

    def test_payment_is_created_with_normal_conditions(self):
        account1 = AccountFactory(currency=self.currency, balance=10)
        account2 = AccountFactory(currency=self.currency, balance=0)

        response = self.client.post(self.url, data={
            'from_account': account1.name,
            'to_account': account2.name,
            'amount': 1,
        })

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        account1.refresh_from_db()
        self.assertEquals(9, account1.balance)
        account2.refresh_from_db()
        self.assertEquals(1, account2.balance)
        self.assertEquals(1, Payment.objects.count())

    def test_payment_is_not_created_with_unsufficient_funds(self):
        account1 = AccountFactory(currency=self.currency, balance=0)
        account2 = AccountFactory(currency=self.currency, balance=0)

        response = self.client.post(self.url, data={
            'from_account': account1.name,
            'to_account': account2.name,
            'amount': 1,
        })

        self.assertContains(response, 'unsufficient funds', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEquals(0, Payment.objects.count())

    def test_payment_is_not_created_with_currency_mismatch_for_recipient(self):
        account1 = AccountFactory(currency=self.currency, balance=10)
        account2 = AccountFactory(currency=CurrencyFactory(), balance=10)

        response = self.client.post(self.url, data={
            'from_account': account1.name,
            'to_account': account2.name,
            'amount': 1,
        })

        self.assertContains(response, 'currency mismatch', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEquals(0, Payment.objects.count())

    def test_payment_is_not_created_with_currency_mismatch_for_sender(self):
        account1 = AccountFactory(currency=CurrencyFactory(), balance=10)
        account2 = AccountFactory(currency=self.currency, balance=10)

        response = self.client.post(self.url, data={
            'from_account': account1.name,
            'to_account': account2.name,
            'amount': 1,
        })

        self.assertContains(response, 'currency mismatch', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertEquals(0, Payment.objects.count())

    def test_payment_is_not_created_with_zero_amount(self):
        account1 = AccountFactory(currency=self.currency, balance=10)
        account2 = AccountFactory(currency=self.currency, balance=0)

        response = self.client.post(self.url, data={
            'from_account': account1.name,
            'to_account': account2.name,
            'amount': 0,
        })

        self.assertContains(response, 'amount must be positive', status_code=status.HTTP_400_BAD_REQUEST)


class TestListPayments(APITestCase):

    def setUp(self):
        self.url = reverse('api:payments')

    def test_empty_list(self):
        resp = self.client.get(self.url)
        self.assertListEqual([], resp.data)

    def test_non_empty_list(self):
        payment = PaymentFactory(amount=42)
        expected_dict = {
            'id': str(payment.id),
            'from_account': payment.from_account.name,
            'to_account': payment.to_account.name,
            'amount': '42.00',
            'currency': payment.currency.code,
        }
        resp = self.client.get(self.url)
        self.assertEqual([expected_dict], resp.data)


class TestListAccounts(APITestCase):

    def setUp(self):
        self.url = reverse('api:accounts')

    def test_empty_list(self):
        resp = self.client.get(self.url)
        self.assertListEqual([], resp.data)

    def test_non_empty_list(self):
        account = AccountFactory(balance=42)
        expected_dict = {
            'name': account.name,
            'balance': '42.00',
            'currency': account.currency.code,
        }
        resp = self.client.get(self.url)
        self.assertEqual([expected_dict], resp.data)
