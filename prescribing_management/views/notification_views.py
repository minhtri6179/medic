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
from prescribing_management.models import Schedule

from prescribing_management.forms.doctor_forms import DoctorEditForm
from prescribing_management.forms.schedule_form import ScheduleCreateForm


class NotiListView(LoginRequiredView, RoleRequiredMixin, ListView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Schedule
    template_name = 'notifications/index.html'
    paginate_by: int = 10

    def get_queryset(self):
        keyword = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        return queryset.filter(
            Q(name__contains=keyword) | Q(status__contains=keyword)
        ).order_by('-created_at')


class NotiDoneView(LoginRequiredView, RoleRequiredMixin, UpdateView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Schedule
    fields = ['status']
    template_name: str = 'doctor/schedule_form.html'

    def get_success_url(self) -> str:
        messages.success(self.request, 'This Appointment is done')
        return reverse('prescribing_management:notifications_index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['action'] = 'edit'
        context['pk'] = self.kwargs.get('pk')
        return context


class ScheduleDeleteView(LoginRequiredView, RoleRequiredMixin, DeleteView):
    roles_required = [User.UserRole.ASSISTANT]
    model = Schedule
    success_url: Optional[str] = reverse_lazy(
        'prescribing_management:notifications_index')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Delete successfully')
        return reverse('prescribing_management:notifications_index')

    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.soft_delete()
        return HttpResponseRedirect(success_url)
