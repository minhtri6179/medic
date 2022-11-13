from django.contrib import admin
from .models import User
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'is_staff', 'is_active', 'is_superuser', 'role', )
    list_filter = ('username', 'is_staff', 'is_active', 'is_superuser', 'role', )
    fieldsets = (
        (None, {'fields': ('username', 'name', 'phone', 'email', 'gender', 'birth', 'address',  'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'phone', 'email', 'gender', 'birth', 'address', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'role')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
