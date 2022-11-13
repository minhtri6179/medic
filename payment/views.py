# Create your views here.
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

from prescribing_management.models import Payment
from prescribing_management.forms.medicine_forms import MedicineCreateForm, MedicineTypeForm
from base.views import LoginRequiredView


class PaymentSelectionView(View):
    model = Payment
    template_name: str = 'payment/payment_form.html'

    def get(self, request):

        return render(request, 'payment/payment_form.html')
