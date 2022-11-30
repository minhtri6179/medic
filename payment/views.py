# Create your views here.
from rest_framework import serializers
from datetime import datetime
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
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
from prescribing_management.models import Invoice
from prescribing_management.forms.medicine_forms import MedicineCreateForm, MedicineTypeForm
from base.views import LoginRequiredView

stripe.api_key = "sk_test_51M7WJ2He0kxdqOahEAfTBDUrGrKCdY8lzo6xAiXiTF0gFAXvCeaiBAyjxcpjJRlCrmIbqTrWhIeiQnd6kFpKcPGQ00H7Pq5gxf"


class PaymentSelectionView(View):
    model = Invoice

    template_name: str = 'payment/index.html'

    def get(self, request):
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
                res['status'] = "fail"
                print("Invoice not found")
            break
        print(res)
        return render(request, 'payment/result.html', context=res)


class PaymentPageView(View):
    model = Invoice
    template_name = "payment/hihi.html"

    def post(self, request):
        return render(request, 'payment/hihi.html')


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Invoice.objects.get(id=self.kwargs["pk"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.stripe_price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)


class InvoiceResult(View):
    template_name: str = 'payment/index.html'


class Pay(View):
    template_name = "payment/index.html"


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
