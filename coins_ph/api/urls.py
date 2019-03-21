from django.urls import path

from coins_ph.api.views import PaymentView, ListAccountsView

app_name = 'api'
urlpatterns = [
    path('accounts/', ListAccountsView.as_view(), name='accounts'),
    path('payments/', PaymentView.as_view(), name='payments'),
]
