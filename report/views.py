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
        from_date_range = datetime.strptime(
            request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(
            request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_general_report_by_date(from_date_range, to_date_range)
        time_data_day = [element['created_at__date'] for element in data]
        value_data_day = [int(element['total']) for element in data]

        time_data_month = []
        value_data_month = []
        total_month = 0

        cur_month = time_data_day[0].month
        flag = False
        for i in range(len(time_data_day)):
            if time_data_day[i].month == cur_month:
                total_month += value_data_day[i]
                flag = True
            else:
                time_data_month.append(cur_month)
                value_data_month.append(total_month)
                cur_month = time_data_day[i].month
                total_month = value_data_day[i]
                flag = False
        if flag:
            time_data_month.append(cur_month)
            value_data_month.append(total_month)
        value_data_day = [str(val) for val in value_data_day]
        value_data_month = [str(val) for val in value_data_month]

        if request.GET.get('by') == 'date':
            time_data = time_data_day
            value_data = value_data_day
        else:
            time_data = time_data_month
            value_data = value_data_month
        print(time_data)
        context = {
            'data': data,
            'time_data': time_data,
            'value_data': value_data
        }
        return render(request, 'report/general_report.html', context)


class RevenueChartView(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        from_date_range = datetime.strptime(
            request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(
            request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_revenue_data(from_date_range, to_date_range)
        context = {
            'data': data,
            'min': from_date_range,
            'max': to_date_range
        }
        return render(request, 'report/revenue_chart.html', context)


class InvoiceDetailReport(View):
    def get(self, request):
        now = datetime.strftime(datetime.now(), '%Y-%m-%d')
        from_date_range = datetime.strptime(
            request.GET.get('from', now), '%Y-%m-%d')
        to_date_range = datetime.strptime(
            request.GET.get('to', now), '%Y-%m-%d')
        group_by = request.GET.get('by', 'date')
        data = ReportService().get_invoice_detail(from_date_range, to_date_range)
        context = {
            'data': data,
        }
        return render(request, 'report/invoice_report.html', context)
