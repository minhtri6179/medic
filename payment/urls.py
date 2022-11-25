from django.urls import path

from payment.views import PaymentSelectionView, InvoiceResult
app_name = 'payment'
urlpatterns = [
    path('', PaymentSelectionView.as_view(), name='payment_index'),
    path('result/', InvoiceResult.as_view(), name='invoice_result')
]
