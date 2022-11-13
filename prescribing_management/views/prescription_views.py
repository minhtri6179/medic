from typing import Any, Dict, Optional
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.views import View
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.template.loader import render_to_string, get_template
from django.template import engines
from django.conf import settings

import io
from django.http import FileResponse

from xhtml2pdf import pisa
from account.mixins import RoleRequiredMixin
from account.models import User

from prescribing_management.models import Patient, Prescription, PrescriptionDetail
from prescribing_management.forms.prescription_forms import PrescriptionForm
from prescribing_management.services.prescription_services import PrescriptionService
# Create your views here.


class PrescriptionListView(RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.BASE]
    template_name: str = 'prescription/index.html'
    model = Prescription
    paginate_by: int = 10
    # context_object_name: Optional[str] = 'prescription_list'

    def get_queryset(self, **kwargs: Any) -> Dict[str, Any]:
        query = self.request.GET.get('q', '')

        object_list = Prescription.objects.filter(
            Q(diagnosis__contains=query) | Q(patient__name__contains=query)
        ).order_by('-modified_at')
        return object_list


class PrescriptionDetailView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]
    model = Prescription

    def get(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        context = {
            'prescription': prescription
        }
        return render(request, 'prescription/detail.html', context)

    def post(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionForm(request.POST, instance=prescription)
        medicine_ids = request.POST.getlist('medicine-ids')
        medicine_numbers = request.POST.getlist('medicine-numbers')
        medicine_usages = request.POST.getlist('medicine-usages')
        service = PrescriptionService()
        if service.edit_prescription_and_detail(form, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(
                request=request, message='Edit prescription successfully')
            return redirect('prescribing_management:prescription_index')
        else:
            return render(request, 'prescription/prescription_form.html', context={'form': form})

    def delete(self, request, pk):
        prescription = get_object_or_404(Prescription, pk=pk)
        prescription.delete()
        messages.success(
            request=request, message='Delete prescription successfully')
        return redirect('prescribing_management:prescription_index')


class PrescriptionCreateView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.DOCTOR]

    model = Prescription

    def get(self, request):
        form = PrescriptionForm()
        patient_id = request.GET.get('patient')
        service = PrescriptionService()
        if patient_id:
            prescription = service.get_empty_prescription_with_patient_id(
                patient_id)
            if not prescription:
                raise Http404
            form = PrescriptionForm(instance=prescription)

        return render(request, 'prescription/prescription_form.html', {'form': form})

    def post(self, request):
        username = request.user.username

        form = PrescriptionForm(request.POST)
        medicine_ids = [i for i in request.POST.getlist('medicine-ids')]
        medicine_numbers = [
            i for i in request.POST.getlist('medicine-numbers')]
        medicine_usages = [i for i in request.POST.getlist('medicine-usages')]
        service = PrescriptionService()
        if service.create_prescription_and_detail(form, username, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(
                request=request, message='Create prescription successfully')
            return redirect('prescribing_management:prescription_index')
        else:
            return render(request, 'prescription/prescription_form.html', context={'form': form})


class PrescriptionEditView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.DOCTOR]
    model = Prescription

    def get(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionForm(instance=prescription)
        context = {
            'form': form,
            'details': prescription.prescriptiondetail_set.all(),
            'action': 'edit',
            'pk': pk
        }
        return render(request, 'prescription/prescription_form.html', context=context)

    def post(self, request, pk):
        prescription = Prescription.objects.get(pk=pk)
        form = PrescriptionForm(request.POST, instance=prescription)
        medicine_ids = request.POST.getlist('medicine-ids')
        medicine_numbers = request.POST.getlist('medicine-numbers')
        medicine_usages = request.POST.getlist('medicine-usages')
        service = PrescriptionService()
        if service.edit_prescription_and_detail(form, medicine_ids=medicine_ids, medicine_numbers=medicine_numbers, medicine_usages=medicine_usages):

            messages.success(
                request=request, message='Edit prescription successfully')
            return redirect('prescribing_management:prescription_index')
        else:
            messages.error(request=request,
                           message='Failed to edit prescription')
            return render(request, 'prescription/prescription_form.html', context={'form': form})


class PrescriptionDeleteView(RoleRequiredMixin, DeleteView):
    model = Prescription
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:prescription_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:prescription_index')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class PrescriptionPrintView(RoleRequiredMixin, View):
    roles_required = [User.UserRole.BASE]

    def get(self, request, pk) -> Dict[str, Any]:
        prescription = Prescription.objects.get(pk=pk)
        context = {'prescription': prescription}
        template = get_template('pdf/prescription_pdf.html')
        html = template.render(context)
        result = io.BytesIO()
        # pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-16")), result)
        pdf = pisa.pisaDocument(io.BytesIO(
            html.encode("utf-8")), result, encoding='utf-8')
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf; encoding="utf-8"')
        return None

# class PdfView(View):
#     def get(self, request, pk) -> Dict[str, Any]:
#         prescription = Prescription.objects.get(pk=pk)
#         context = { 'prescription': prescription}
#         template = get_template('pdf/prescription_pdf.html')
#         html  = template.render(context)
#         result = io.BytesIO()
#         pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1", 'ignore')), result)
#         if not pdf.err:
#             return HttpResponse(html)
#         return None
