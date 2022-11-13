from django.urls import path

from report.views import GeneralReportView, InvoiceDetailReport, RevenueChartView
app_name = 'report'
urlpatterns = [
    path('', GeneralReportView.as_view(), name='general'),
    path('revenue', RevenueChartView.as_view(), name='chart'),
    path('invoice', InvoiceDetailReport.as_view(), name='invoice'),
]