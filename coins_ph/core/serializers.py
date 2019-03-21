from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from coins_ph.core.models import Payment, Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Account
        fields = ('name', 'balance', 'currency',)


class PaymentSerializer(serializers.ModelSerializer):
    currency = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta(object):
        model = Payment
        fields = ('id', 'from_account', 'to_account', 'currency', 'amount')

    @transaction.atomic
    def create(self, validated_data):
        # Select user accounts again with locking, DRF just ensures that they exist
        from_account = validated_data['from_account'].reselect_for_update()
        to_account = validated_data['to_account'].reselect_for_update()
        self._validate_transaction(from_account, to_account, validated_data['amount'])
        from_account.update_balance(-validated_data['amount'])
        to_account.update_balance(validated_data['amount'])
        return Payment.objects.create(
            from_account=from_account, to_account=to_account,
            amount=validated_data['amount'], currency=from_account.currency
        )

    @staticmethod
    def _validate_transaction(from_account, to_account, amount):
        if amount <= 0:
            raise ValidationError('amount must be positive')
        if from_account.currency != to_account.currency:
            raise ValidationError('currency mismatch')
        if from_account.balance < amount:
            raise ValidationError('unsufficient funds')
