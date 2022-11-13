from django.contrib import admin
from prescribing_management.models import Medicine,  MedicineType, Doctor
# Register your models here.
admin.site.register(Medicine)
admin.site.register(MedicineType)
admin.site.register(Doctor)
