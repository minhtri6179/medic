from dataclasses import field
from django import forms
from prescribing_management.models import Doctor
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class DoctorEditForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ['expertise', 'specialize']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
