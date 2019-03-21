from django.test import TestCase

from tests.factories import AccountFactory


class TestTransactionAccount(TestCase):

    def test_update_balance(self):
        account = AccountFactory(balance=10)
        account.update_balance(42)
        account.refresh_from_db()
        self.assertEquals(account.balance, 52)
