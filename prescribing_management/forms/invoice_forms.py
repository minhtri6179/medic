from typing import Any
from django import forms
from django.forms import ModelForm
from prescribing_management.models import Invoice, InvoiceDetail
from django.core.exceptions import ValidationError
from django import forms


class InvoiceCreateOrEditForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ('created_at', 'modified_at', 'total',
                   'medicines', 'deleted_at', 'created_by',
                   'is_paid', 'stripe_invoice_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class InvoiceDetailForm(ModelForm):
    class Meta:
        model = InvoiceDetail
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MultipleValueWidget(forms.NumberInput):
    def value_from_datadict(self, data, files, name):
        return data.getlist(name)


class MultipleValueField(forms.Field):
    widget = MultipleValueWidget


def clean_int(x):
    try:
        return int(x)
    except ValueError:
        raise ValidationError("Cannot convert to integer: {}".format(repr(x)))


class MultipleIntField(MultipleValueField):
    def clean(self, value):
        return [clean_int(x) for x in value]


class InvoiceFullForm(InvoiceCreateOrEditForm):
    medicine_ids = MultipleIntField()
    medicine_unit_prices = MultipleIntField()
    medicine_quantities = MultipleIntField()
