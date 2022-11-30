from django.urls import path

from payment.views import PaymentSelectionView, InvoiceResult, Pay, CancelView, SuccessView, PaymentPageView
app_name = 'payment'
urlpatterns = [
    path('', PaymentSelectionView.as_view(), name='payment_index'),
    path('result/', InvoiceResult.as_view(), name='invoice_result'),
    path('<int>/pay/', Pay.as_view(), name='pay'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
    path('asas/', PaymentPageView.as_view(), name='landing'),

]
