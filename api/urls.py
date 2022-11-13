from django.urls import path
from .views import MedicineDetaiView, MedicineListView, MedicineQuantityValidationView, MedicineValidationFormView, PatientValidationFormView, ScheduleCheck


app_name = 'api'
urlpatterns = [
    path('medicine', MedicineListView.as_view(), name='medicine_list'),
    path('medicine/<int:id>', MedicineDetaiView.as_view(), name='medicine_detail'),
    path('medicine/validate', MedicineValidationFormView.as_view(), name='medicine_validation'),
    path('medicinetype/validate', MedicineValidationFormView.as_view(), name='medicine_type_validation'),
    path('patient/validate', PatientValidationFormView.as_view(), name='patient_validation'),
    path('medicine/<int:pk>/quantity/validate', MedicineQuantityValidationView.as_view(), name='medicine_quantity_validation'),
    path('schedule/validate', ScheduleCheck.as_view(), name='schedule_check')
]

