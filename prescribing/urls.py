"""prescribing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView  # new
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # path('patient/', include('patient.urls')),
    # path('medicine/', include('medicine.urls')),
    # path('prescription/', include('prescription.urls')),
    # path('invoice/', include('invoice.urls')),
    path('payment/', include('payment.urls')),
    path('report/', include('report.urls')),
    path('', include('prescribing_management.urls')),
    path('api/', include('api.urls')),
    path('superuser/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(),
         name='change_password'),
    path('change-password/done', auth_views.PasswordChangeDoneView.as_view(),
         name='done_change_password'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
