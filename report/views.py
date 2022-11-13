from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from report.services import ReportService
# Create your views here.
class GeneralReportView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        from_date_range = datetime.strptime(request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_general_report_by_date(from_date_range, to_date_range)
        context = {
            'data': data,
            
        }
        return render(request, 'report/general_report.html', context)

class RevenueChartView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        from_date_range = datetime.strptime(request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_revenue_data(from_date_range, to_date_range)
        context = {
            'data': data,
            'min': from_date_range,
            'max': to_date_range
        }
        print(context)
        return render(request, 'report/revenue_chart.html', context)

class InvoiceDetailReport(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        from_date_range = datetime.strptime(request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_invoice_detail(from_date_range, to_date_range)
        context = {
            'data': data,
        }
        print(context)
        return render(request, 'report/invoice_report.html', context)
