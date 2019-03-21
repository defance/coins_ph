from factory import DjangoModelFactory, SubFactory, Sequence, SelfAttribute

from coins_ph.core.models import Account, Currency, Payment


class CurrencyFactory(DjangoModelFactory):
    code = Sequence('currency_{}'.format)

    class Meta(object):
        model = Currency
        django_get_or_create = ('code',)


class AccountFactory(DjangoModelFactory):
    balance = 0
    currency = SubFactory(CurrencyFactory)
    name = Sequence('username_{}'.format)

    class Meta(object):
        model = Account


class PaymentFactory(DjangoModelFactory):
    currency = SubFactory(CurrencyFactory)
    from_account = SubFactory(AccountFactory, currency=SelfAttribute('..currency'))
    to_account = SubFactory(AccountFactory, currency=SelfAttribute('..currency'))
    amount = 0

    class Meta(object):
        model = Payment

