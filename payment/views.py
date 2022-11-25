# Create your views here.
from rest_framework import serializers
from datetime import datetime
from django.shortcuts import render
from django.views import View
from django.utils import timezone
#from report.services import ReportService
from typing import Optional, Dict, Any

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.views import View
from django.views.generic.edit import DeleteView, UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from account.mixins import RoleRequiredMixin
from account.models import User
from prescribing_management.models import Schedule
import stripe
from prescribing_management.models import Payment, Invoice
from prescribing_management.forms.medicine_forms import MedicineCreateForm, MedicineTypeForm
from base.views import LoginRequiredView

stripe.api_key = "sk_test_51M7WJ2He0kxdqOahEAfTBDUrGrKCdY8lzo6xAiXiTF0gFAXvCeaiBAyjxcpjJRlCrmIbqTrWhIeiQnd6kFpKcPGQ00H7Pq5gxf"


class PaymentSelectionView(View):
    model = Payment

    template_name: str = 'payment/index.html'

    def get(self, request):
        print('hehe')
        return render(request, 'payment/index.html')

    def post(self, request):
        invoice_model = Invoice
        invoice_ids = request.POST['invoice-id-payment'].split(',')
        res = {}
        for invoice in invoice_ids:
            try:
                res['status'] = "success"
                res['id'] = invoice_model.objects.filter(
                    id=invoice).values()[0]['id']
                res['patient_id'] = invoice_model.objects.filter(
                    id=invoice).values()[0]['patient_id']
                res['total'] = invoice_model.objects.filter(
                    id=invoice).values()[0]['total']
                res['is_paid'] = invoice_model.objects.filter(
                    id=invoice).values()[0]['is_paid']
            except:
                res['status'] = "Fail"
                print("Invoice not found")
            break

        return render(request, 'payment/index.html', context=res)


class InvoiceResult(View):
    template_name: str = 'payment/index.html'
