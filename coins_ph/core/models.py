import uuid

from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)

    def reselect_for_update(self):
        return Account.objects.select_for_update().get(pk=self.pk)

    def update_balance(self, amount):
        self.balance += amount
        self.save()

    class Meta(object):
        app_label = 'coins_ph'


class Currency(models.Model):
    code = models.CharField(max_length=3, primary_key=True)

    class Meta(object):
        app_label = 'coins_ph'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='payments_outgoing')
    to_account = models.ForeignKey('Account', on_delete=models.PROTECT, related_name='payments_incoming')
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta(object):
        app_label = 'coins_ph'
