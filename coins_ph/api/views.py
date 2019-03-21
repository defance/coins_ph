from rest_framework.generics import ListAPIView, ListCreateAPIView

from coins_ph.core.models import Account, Payment
from coins_ph.core.serializers import PaymentSerializer, AccountSerializer


class ListAccountsView(ListAPIView):
    """
    Return list of all existing accounts in the following format:

        [
            {
                "name": account_name,
                "currency": currency_code,
                "balance": current_account_balance
            }
        ]
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class PaymentView(ListCreateAPIView):
    """
    get:
    Return list of all performed payments in the following format:

        [
            {
                "id": payment_uuid,
                "from_account": account_name,
                "to_account": account_name,
                "amount": payment_amount,
                "currency": currency_code
            }
        ]

    post:
    Attempts to create payment.

    Request body should be in json format. Example of request body:

        {
            "from_account": account_name,
            "to_account": account_name,
            "amount": payment_amount
        }

    The request will fail with corresponding message under following
    conditions:
        * Any of accounts (`from_account` or `to_account`) does not
          exist
        * Participants' currency are not the same (exchange is not
          supported)
        * Payment account exceeds source account's (`from_account`)
          balance
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
