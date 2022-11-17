from django.urls import path

from report.views import GeneralReportView, InvoiceDetailReport, MedicineBestseller, RedirectReport
app_name = 'report'
urlpatterns = [
    path('', RedirectReport.as_view(), name='redirect'),
    path('revenue', GeneralReportView.as_view(), name='revenue'),
    path('bestseller', MedicineBestseller.as_view(), name='bestseller'),
    path('invoice', InvoiceDetailReport.as_view(), name='invoice'),
]
