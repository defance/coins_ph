from django.contrib import admin

from coins_ph.core.models import Account, Currency, Payment

admin.site.register(Account)
admin.site.register(Currency)
admin.site.register(Payment)
