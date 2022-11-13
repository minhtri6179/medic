from datetime import datetime
from invoice.models import Invoice
from patient.models import Patient
from django.db.models import Count
invoice = Invoice.objects.create(created_at = datetime(2022, 6, 10), patient = Patient.objects.get(pk=1), total=0)


Invoice.objects.filter(created_at__date__gte = datetime(2022, 9, 1), created_at__date__lte = datetime(2022, 9, 19))\
    .values('created_at__month')\
    .annotate(prescription_count = Count('id'))\
    .values('created_at__month', 'prescription_count')


from report.services import ReportService
from datetime import datetime
ReportService().get_general_report_by_date(datetime(2022, 9, 1), datetime.now())



medicine = InvoiceDetail.objects\
    .select_related('medicine')\
    .values('medicine')\
    .annotate(total = Sum('line_total'), count=Count('medicine'))\
    .values('medicine__id', 'medicine__name', 'total', 'count')\
    
