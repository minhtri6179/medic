from django.urls import path
from prescribing_management.views.patient_views import PatientUpload, PatientExport, PatientCreateView, PatientListView, PatientDetailView, PatientEditView, PatientDeleteView
from prescribing_management.views.medicine_views import upload, MedicineListView, MedicineCreateView, MedicineDeleteView, MedicineDetailView, MedicineEditView, MedicineTypeCreateView, MedicineTypeDeleteView, MedicineTypeEditView, MedicineTypeListView
from prescribing_management.views.invoice_views import InvoiceFullFormView, InvoiceListView, InvoiceCreateView, InvoiceDeleteView, InvoiceDetailView, InvoiceEditView, InvoicePrintView
from prescribing_management.views.prescription_views import PrescriptionListView, PrescriptionCreateView, PrescriptionDeleteView, PrescriptionDetailView, PrescriptionEditView, PrescriptionPrintView
from prescribing_management.views.doctor_views import MakeAppointmentView, DoctorEditView, DoctorListView, DoctorDeleteView
from prescribing_management.views.notification_views import NotiListView, NotiDoneView, ScheduleDeleteView
app_name = 'prescribing_management'
urlpatterns = [
    # Patient Views URLs
    path('patient', PatientListView.as_view(), name='patient_index'),
    path('patient/<int:pk>', PatientDetailView.as_view(), name="patient_detail"),
    path('patient/create', PatientCreateView.as_view(), name="patient_create"),
    path('patient/<int:pk>/delete',
         PatientDeleteView.as_view(), name="patient_delete"),
    path('patient/<int:pk>/edit', PatientEditView.as_view(), name="patient_edit"),
    path('patient/upload', PatientUpload, name='patient_upload'),
    path('patient/export', PatientExport, name='patient_export'),

    # Medicine Views URLs
    path('medicine', MedicineListView.as_view(), name='medicine_index'),
    path('medicine/<int:pk>', MedicineDetailView.as_view(), name="medicine_detail"),
    path('medicine/create', MedicineCreateView.as_view(), name="medicine_create"),
    path('medicine/<int:pk>/delete',
         MedicineDeleteView.as_view(), name="medicine_delete"),
    path('medicine/<int:pk>/edit', MedicineEditView.as_view(), name="medicine_edit"),
    path('medicine/type', MedicineTypeListView.as_view(),
         name="medicine_type_index"),
    path('medicine/type/create', MedicineTypeCreateView.as_view(),
         name="medicine_type_create"),
    path('medicine/type/<int:pk>/edit',
         MedicineTypeEditView.as_view(), name="medicine_type_edit"),
    path('medicine/type/<int:pk>/delete',
         MedicineTypeDeleteView.as_view(), name="medicine_type_delete"),
    path('medicine/upload', upload, name='medicine_upload'),

    # Invoice Views URLs
    path('invoice', InvoiceListView.as_view(), name='invoice_index'),
    path('invoice/<int:pk>', InvoiceDetailView.as_view(), name="invoice_detail"),
    path('invoice/create', InvoiceCreateView.as_view(), name="invoice_create"),
    path('invoice/create/fullform',
         InvoiceFullFormView.as_view(), name="invoice_fullform"),
    path('invoice/<int:pk>/delete',
         InvoiceDeleteView.as_view(), name="invoice_delete"),
    path('invoice/<int:pk>/edit', InvoiceEditView.as_view(), name="invoice_edit"),
    path('invoice/<int:pk>/print', InvoicePrintView.as_view(), name="invoice_print"),

    # Prescription Views URLs
    path('prescription', PrescriptionListView.as_view(), name='prescription_index'),
    path('prescription/<int:pk>', PrescriptionDetailView.as_view(),
         name="prescription_detail"),
    path('prescription/create', PrescriptionCreateView.as_view(),
         name="prescription_create"),
    path('prescription/<int:pk>/delete',
         PrescriptionDeleteView.as_view(), name="prescription_delete"),
    path('prescription/<int:pk>/edit',
         PrescriptionEditView.as_view(), name="prescription_edit"),
    path('prescription/<int:pk>/print',
         PrescriptionPrintView.as_view(), name="prescription_print"),


    # Doctor views urls
    path('doctor', DoctorListView.as_view(), name='doctor_index'),
    path('doctor/<int:pk>/edit', DoctorEditView.as_view(), name='doctor_edit'),
    path('doctor/<int:pk>/delete', DoctorDeleteView.as_view(), name='doctor_delete'),
    path('doctor/appointment', MakeAppointmentView.as_view(),
         name='make_appointment'),
    # path('Doctor/<int:pk>', PatientDetailView.as_view(), name="patient_detail"),
    # path('Doctor/create', PatientCreateView.as_view(), name="patient_create"),
    # path('Doctor/<int:pk>/delete', PatientDeleteView.as_view(), name="patient_delete"),
    # path('Doctor/<int:pk>/edit', PatientEditView.as_view(), name="patient_edit"),


    # Notifications
    path('notifications', NotiListView.as_view(), name='notifications_index'),
    path('notification/<int:pk>/done',
         NotiDoneView.as_view(), name='notification_done'),
    path('schedule/<int:pk>/delete',
         ScheduleDeleteView.as_view(), name='schedule_delete'),
]
