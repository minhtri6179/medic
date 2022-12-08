# Create your views here.
from rest_framework import serializers
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
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
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


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
                res['total'] = int(invoice_model.objects.filter(
                    id=invoice).values()[0]['total'])
                res['is_paid'] = invoice_model.objects.filter(
                    id=invoice).values()[0]['is_paid']
            except:
                res['status'] = "fail"
                print("Invoice not found")
            break
        res['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, 'payment/result.html', context=res)


def charge(request, id):
    invoice_instance = get_object_or_404(Invoice, pk=id)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=int(invoice_instance.total),
                currency='vnd',
                description='Payment Gateway',
                source=request.POST.get('stripeToken')
            )
            invoice_instance.is_paid = True
            invoice_instance.save()
            return render(request, 'payment/charge.html')
        except stripe.error.CardError as e:
            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)

            return render(request, 'payment/cancel.html')


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
