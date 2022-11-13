from dataclasses import field
from socket import MsgFlag
from django import forms
from prescribing_management.models import Schedule
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class ScheduleCreateForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise ValidationError(_('This field is required the number.'))
        return phone

    def clean_appointment_date(self):
        data = self.cleaned_data['appointment_date']

        print(data)
        print(type(data))
        if data < datetime.today().date():
            raise ValidationError(_('Invalid date - renewal in past'))

        return data

    def clean_appointment_time(self):
        data = self.cleaned_data['appointment_time']
        data = data.replace(tzinfo=None)
        if data < datetime.today().time():
            raise ValidationError(_('Invalid time - renewal in past'))

        return data

    class Meta:
        model = Schedule
        exclude = ('deleted_at', 'status')

        widgets = {
            'appointment_date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.widgets.TimeInput(attrs={'type': 'time'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Your email address'}),
            'note_to_doctor': forms.TextInput(attrs={'placeholder': 'Your problems'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
