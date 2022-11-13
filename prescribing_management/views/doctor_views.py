from typing import Optional, Dict, Any

from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.db.models import Q
from account.models import User
from account.mixins import RoleRequiredMixin
from base.views import LoginRequiredView
from django.urls import reverse_lazy
from prescribing_management.models import Doctor, Schedule
from prescribing_management.forms.doctor_forms import DoctorEditForm
from prescribing_management.forms.schedule_form import ScheduleCreateForm


class DoctorEditView(LoginRequiredView, UpdateView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Doctor
    template_name: str = 'doctor/doctor_form.html'
    form_class = DoctorEditForm
    context_object_name: Optional[str] = 'form'

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message="Edit Doctor successfully")
        return reverse('prescribing_management:doctor_index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context


class DoctorListView(ListView):
    model = Doctor
    template_name = 'Doctor/index.html'
    context_object_name: Optional[str] = 'doctors'
    paginate_by: int = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = Doctor.objects.filter(
            Q(specialize__contains=query) | Q(expertise__contains=query)
        )
        return object_list


class DoctorDeleteView(LoginRequiredView, RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.ASSISTANT]
    model = User
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:doctor_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:doctor_index')

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)


class MakeAppointmentView(CreateView):
    model = Schedule
    template_name: str = 'doctor/schedule_form.html'
    form_class = ScheduleCreateForm
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:doctor_index')

    def get_success_url(self) -> str:
        messages.success(request=self.request,
                         message="Make new appointment succeccelly")
        return reverse('prescribing_management:doctor_index')
