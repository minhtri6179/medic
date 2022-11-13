from django.urls import path

from payment.views import PaymentSelectionView
app_name = 'payment'
urlpatterns = [
    path('', PaymentSelectionView.as_view(), name='payment_selection'),
]