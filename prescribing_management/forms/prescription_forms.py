from prescribing_management.models import Prescription, PrescriptionDetail
from django.forms import ModelForm


class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        exclude = ('created_at', 'medicines', 'deleted_at',  'created_by')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PrescriptionDetailForm(ModelForm):
    class Meta:
        model = PrescriptionDetail
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
