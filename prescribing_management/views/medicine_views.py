from django import forms
import csv
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
from django.core.files.storage import FileSystemStorage
from django.forms import formset_factory
from prescribing_management.models import Medicine, MedicineType
from prescribing_management.forms.medicine_forms import MedicineCreateForm, MedicineTypeForm
from django.shortcuts import render


class MedicineListView(RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.BASE]
    model = Medicine
    template_name: str = 'medicine/index.html'
    context_object_name: Optional[str] = 'medicine_list'
    paginate_by: int = 10
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['medicines'] = Medicine.objects.all()
    #     return context

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = Medicine.objects.filter(
            Q(name__contains=query) | Q(medicine_type__name__contains=query)
        )\
            .order_by('name')
        return object_list


class MedicineDeleteView(RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.BASE]

    model = Medicine
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:medicine_index')


class MedicineDetailView(RoleRequiredMixin, DetailView):
    roles_required = [User.UserRole.BASE]

    model = Medicine
    template_name: str = 'medicine/detail.html'
    context_object_name: Optional[str] = 'medicine'


class MedicineEditView(RoleRequiredMixin, UpdateView):
    roles_required = [User.UserRole.BASE]
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_index')

    def get_success_url(self) -> str:
        messages.success(request=self.request, message='Update successfully')
        return reverse('prescribing_management:medicine_index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context


class MedicineCreateView(RoleRequiredMixin, CreateView):
    roles_required = [User.UserRole.BASE]
    model = Medicine
    template_name: str = 'medicine/medicine_form.html'
    form_class = MedicineCreateForm
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_index')

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message="Create new medicine successfully")
        return reverse('prescribing_management:medicine_index')


class MedicineTypeListView(RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.BASE]
    model = MedicineType
    template_name: str = 'medicine/medicine_type_index.html'
    context_object_name: Optional[str] = 'medicine_type_list'
    paginate_by: int = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = MedicineType.objects.filter(
            Q(name__contains=query)
        )\
            .order_by('name')
        return object_list


class MedicineTypeCreateView(RoleRequiredMixin, CreateView):
    roles_required = [User.UserRole.BASE]
    model = MedicineType
    form_class = MedicineTypeForm
    template_name = 'medicine/medicine_type_form.html'
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_type_index')

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message="Create new medicine type successfully")
        return reverse('prescribing_management:medicine_type_index')


class MedicineTypeEditView(RoleRequiredMixin, UpdateView):
    roles_required = [User.UserRole.BASE]
    form_class = MedicineTypeForm
    model = MedicineType
    template_name = 'medicine/medicine_type_form.html'
    context_object_name: Optional[str] = 'form'
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_type_index')

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message='Update medicine type successfully')
        return reverse('prescribing_management:medicine_type_index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context


class MedicineTypeDeleteView(RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.BASE]
    model = MedicineType
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:medicine_type_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete medicine type successfully')
        return reverse('prescribing_management:medicine_type_index')


def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        file_url = 'static'+file_url
        ArticleFormSet = formset_factory(Medicine, formset=MedicineCreateForm)
        flag = True
        response = {
            'status': flag,
            'image_url': '',
            'message': 'File Uploaded Successfully'
        }
        with open(file_url, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) != 8:
                    flag = False
                    break
                m_type = MedicineType.objects.filter(
                    name=row[7]).values_list('id', flat=True)
                m_name = Medicine.objects.filter(
                    name=row[0]).values_list('id', flat=True)
                if len(m_type) != 0 and len(m_name) != 0:
                    medicine_quantity = Medicine.objects.filter(
                        name=row[0], medicine_type=MedicineType(id=m_type[0]))

                    quantity_updated = medicine_quantity[0].stock_quantity+int(
                        row[1])
                    medicine_quantity.update(stock_quantity=quantity_updated)
                    continue

                if len(m_type) == 0:
                    medicine_type = MedicineType(name=row[7])
                    medicine_type.save()
                    m_type = MedicineType.objects.filter(
                        name=row[7]).values_list('id', flat=True)
                m_type = m_type[0]
                d = {
                    'name': row[0],
                    'stock_quantity': row[1],
                    'unit': row[2],
                    'usage': row[3],
                    'origin_price': row[4],
                    'sale_price': row[5],
                    'dose_per_day': row[6],
                    'medicine_type': m_type
                }
                formset = ArticleFormSet(d)
                if formset.is_valid() == False:
                    flag = False
                    break
                if formset.is_valid():
                    formset.save()
        if flag is False:
            response = {
                'status': flag,
                'image_url': '',
                'message': 'File Upload Failed'
            }
        return render(request, 'medicine/upload.html', {'response': response})
    return render(request, 'medicine/upload.html')
