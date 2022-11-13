import pandas as pd
from django.forms import formset_factory
from django.core.files.storage import FileSystemStorage
import csv
import os
from typing import Optional, Dict, Any
import tablib
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from account.models import User
from account.mixins import RoleRequiredMixin
from base.views import LoginRequiredView
from tablib import Dataset
from prescribing_management.models import Patient
from prescribing_management.forms.patient_forms import PatientCreateUpdateForm, ImportForm
from django.shortcuts import render
from django.views import View
from django.templatetags.static import static
from import_export import resources


class PatientResource(resources.ModelResource):
    class Meta:
        model = Patient


class PatientCreateView(LoginRequiredView, RoleRequiredMixin, CreateView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Patient
    template_name: str = 'patient/patient_form.html'
    form_class = PatientCreateUpdateForm
    context_object_name: Optional[str] = 'form'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message='Create patient successfully')
        return reverse('prescribing_management:patient_index')


class PatientEditView(LoginRequiredView, RoleRequiredMixin, UpdateView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Patient
    template_name: str = 'patient/patient_form.html'
    form_class = PatientCreateUpdateForm
    context_object_name: Optional[str] = 'form'

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message="Edit patient successfully")
        return reverse('prescribing_management:patient_index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context


class PatientListView(LoginRequiredView, RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.BASE]
    model = Patient
    template_name = 'patient/index.html'
    context_object_name: Optional[str] = 'patients'
    paginate_by: int = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        return queryset.filter(
            Q(name__contains=keyword) | Q(
                address__contains=keyword) | Q(phone__contains=keyword)
        ).order_by('-created_at')


class PatientDetailView(RoleRequiredMixin, DetailView):
    roles_required = [User.UserRole.BASE]
    model = Patient
    template_name: str = 'patient/detail.html'
    context_object_name: Optional[str] = 'patient'


class PatientDeleteView(LoginRequiredView, RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Patient
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:patient_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:patient_index')

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


def PatientUpload(request):
    if request.method == 'POST' and request.FILES['upload_patient']:
        upload = request.FILES['upload_patient']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        file_url = 'static'+file_url
        ArticleFormSet = formset_factory(
            Patient, formset=PatientCreateUpdateForm)
        respone = {
            'status': True,
            'image_url': '',
            'message': 'File upload success'
        }
        with open(file_url, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                d = {
                    'name': row[0],
                    'age': row[1],
                    'phone': row[2],
                    'gender': row[3],
                    'address': row[4],
                    'height': row[5],
                    'weight': row[6],
                    'temperature': row[7],
                    'blood_pressure': row[8],
                    'heart_rate': row[9],
                    'doctor': row[10],
                }
                formset = ArticleFormSet(d)
                if formset.is_valid() == False:
                    respone = {
                        'status': False,
                        'image_url': '',
                        'message': 'Upload file failed'
                    }
                if formset.is_valid():
                    formset.save()
        import glob

        files = glob.glob('static/media/*')
        print(files)
        print(file_url)
        for f in files:
            os.remove(f)

        return render(request, 'patient/upload.html', {'respone': respone})
    return render(request, 'patient/upload.html')


def PatientExport(request):
    print("export comming!!!!")
    dataset = PatientResource().export()
    csv_raw = dataset.csv
    txts = csv_raw.split(',')
    start = 0
    rows = []
    for i, t in enumerate(txts):
        if '\n' in t:
            row = txts[start:i+1]
            row[-1] = row[-1][:-1]
            rows.append(row)
            start = i+1

    rows[0] = rows[0][1:]
    df = pd.DataFrame(rows[1:], columns=rows[0])

    df.to_csv('patient_export.csv', sep='\t', encoding='utf-8', index=False)
    df.to_excel('patient_export.xlsx', index=None, header=True)
    if os.path.exists('patient_export.xlsx'):
        with open('patient_export.xlsx', 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + \
                'patient_export.xlsx'
            return response

    raise Http404
