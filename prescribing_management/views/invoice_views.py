from typing import Dict, Any, Optional
import io
from xhtml2pdf import pisa
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.views import View
from django.template.loader import get_template

from account.mixins import RoleRequiredMixin
from account.models import User
from prescribing_management.models import Invoice
from prescribing_management.services.invoice_services import InvoiceService
from prescribing_management.forms.invoice_forms import InvoiceCreateOrEditForm, InvoiceFullForm


class InvoiceListView(RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.BASE]
    template_name: str = 'invoice/index.html'
    model = Invoice
    paginate_by: int = 10
    # context_object_name: Optional[str] = 'invoice_list'

    def get_queryset(self, **kwargs: Any) -> Dict[str, Any]:
        query = self.request.GET.get('q', '')

        object_list = Invoice.objects.filter(
            patient__name__contains=query).order_by('-modified_at')
        return object_list


class InvoiceDetailView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]
    model = Invoice

    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        context = {
            'invoice': invoice
        }
        return render(request, 'invoice/detail.html', context)

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(request.POST, instance=invoice)
        medicine_ids = request.POST.getlist('medicine-ids')
        medicine_quantities = request.POST.getlist('medicine-quantities')
        medicine_prices = request.POST.getlist('medicine-unit-prices')

        service = InvoiceService()
        if service.edit_invoice_and_detail(form, medicine_ids=medicine_ids, medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(
                request=request, message='Edit invoice successfully')
            return redirect('prescribing_management:invoice_index')
        else:
            return render(request, 'invoice/invoice_form.html', context={'form': form})

    def delete(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        messages.success(
            request=request, message='Delete invoice successfully')
        return redirect('prescribing_management:invoice_index')


class InvoiceCreateView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]

    model = Invoice

    def get(self, request):
        form = InvoiceCreateOrEditForm()
        patient_id = request.GET.get('patient')
        prescription_id = request.GET.get('prescription')
        service = InvoiceService()

        if patient_id:
            empty_invoice = service.get_empty_invoice_with_patient_id(
                patient_id)
            if not empty_invoice:
                raise Http404
            form = InvoiceCreateOrEditForm(instance=empty_invoice)

        if prescription_id:
            empty_invoice, invoice_details = service.get_empty_invoice_and_details_from_prescription_id(
                prescription_id)
            form = InvoiceCreateOrEditForm(instance=empty_invoice)
            if not empty_invoice or not invoice_details:
                raise Http404
            return render(request, 'invoice/invoice_form.html', {'form': form, 'details': invoice_details})

        return render(request, 'invoice/invoice_form.html', {'form': form})

    def post(self, request):
        form = InvoiceCreateOrEditForm(request.POST)
        medicine_ids = [i for i in request.POST.getlist('medicine-ids')]
        medicine_quantities = [
            i for i in request.POST.getlist('medicine-quantities')]
        medicine_prices = [
            i for i in request.POST.getlist('medicine-unit-prices')]
        service = InvoiceService()
        username = request.user.username
        if service.create_invoice_and_detail(form, username, medicine_ids=medicine_ids,
                                             medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(
                request=request, message='Create invoice successfully')
            return redirect('prescribing_management:invoice_index')
        else:
            return render(request, 'invoice/invoice_form.html', context={'form': form})


class InvoiceEditView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]
    model = Invoice

    def get(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(instance=invoice)
        context = {
            'form': form,
            'details': invoice.invoicedetail_set.all(),
            'action': 'edit',
            'pk': pk
        }
        return render(request, 'invoice/invoice_form.html', context=context)

    def post(self, request, pk):
        invoice = Invoice.objects.get(pk=pk)
        form = InvoiceCreateOrEditForm(request.POST, instance=invoice)
        medicine_ids = request.POST.getlist('medicine-ids')
        medicine_quantities = request.POST.getlist('medicine-quantities')
        medicine_prices = request.POST.getlist('medicine-unit-prices')
        service = InvoiceService()
        if service.edit_invoice_and_detail(form, medicine_ids=medicine_ids, medicine_quantities=medicine_quantities, medicine_prices=medicine_prices):

            messages.success(
                request=request, message='Edit invoice successfully')
            return redirect('prescribing_management:invoice_index')
        else:
            messages.error(request=request, message='Failed to edit invoice')
            context = {
                'form': form,
                'details': invoice.invoicedetail_set.all(),
                'action': 'edit',
                'pk': pk
            }
            return render(request, 'invoice/invoice_form.html', context=context)

            # return render(request, 'invoice/invoice_form.html', context={'form': form })


class InvoiceDeleteView(RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.BASE]
    model = Invoice
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:invoice_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:invoice_index')


class InvoicePrintView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]

    def get(self, request, pk) -> Dict[str, Any]:
        invoice = Invoice.objects.get(pk=pk)
        context = {'invoice': invoice}
        template = get_template('pdf/invoice_pdf.html')
        html = template.render(context)
        result = io.BytesIO()
        # pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-16")), result)
        pdf = pisa.pisaDocument(io.BytesIO(
            html.encode("utf-8")), result, encoding='utf-8')
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf; encoding="utf-8"')
        return None


class InvoiceFullFormView(View):
    model = Invoice

    def get(self, request):
        form = InvoiceFullForm()
        context = {
            'form': form,
        }
        return render(request, 'invoice/invoice_form.html', context=context)

    def post(self, request):
        form = InvoiceFullForm(request.POST)
        context = {
            'form': form,
        }
        return render(request, 'invoice/invoice_form.html', context=context)
