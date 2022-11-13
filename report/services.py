from collections import defaultdict
from datetime import datetime
from prescribing_management.models import Prescription, Invoice, InvoiceDetail
from django.db.models import Count, Sum, Avg
from itertools import chain


class ReportService:
    @staticmethod
    def get_general_report_by_date(from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte=from_date_range, created_at__date__lte=to_date_range)\
            .values('created_at__date')\
            .annotate(total=Sum('total')).annotate(invoice_count=Count('id'))\
            .values('created_at__date', 'invoice_count', 'total')
        prescription = Prescription.objects.filter(created_at__date__gte=from_date_range, created_at__date__lte=to_date_range)\
            .values('created_at__date')\
            .annotate(prescription_count=Count('id'))\
            .values('created_at__date', 'prescription_count')
        invoice_dict = {x['created_at__date']: {field: x.get(
            field, 0) for field in x.keys()} for x in invoice}
        prescription_dict = {x['created_at__date']: {field: x.get(
            field, 0) for field in x.keys()} for x in prescription}
        print(invoice_dict)
        print(prescription_dict)
        data = defaultdict(lambda: {'invoice_count': 0,
                                    'prescription_count': 0,
                                    'total': 0})
        for key in invoice_dict:
            print(key)
            for field in invoice_dict[key]:
                print(field)
                data[key][field] = invoice_dict[key][field]
        for key in prescription_dict:
            print(key)
            for field in prescription_dict[key]:
                print(field)
                data[key][field] = prescription_dict[key][field]

        return list(data.values())

    def get_revenue_data(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        invoice = Invoice.objects.filter(created_at__date__gte=from_date_range, created_at__date__lte=to_date_range)\
            .values('created_at__date')\
            .annotate(total=Sum('total')).annotate(invoice_count=Count('id'))\
            .values('created_at__date', 'invoice_count', 'total')
        return invoice

    def get_invoice_detail(self, from_date_range=datetime.now(), to_date_range=datetime.now()):
        medicine = InvoiceDetail.objects\
            .filter(invoice__created_at__date__gte=from_date_range, invoice__created_at__date__lte=to_date_range)\
            .values('medicine')\
            .annotate(total=Sum('line_total'), count=Count('medicine'))\
            .values('medicine__id', 'medicine__name', 'medicine__unit', 'total', 'count')
        return medicine
