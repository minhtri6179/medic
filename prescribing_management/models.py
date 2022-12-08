from pyexpat import model
from django.db import models
import datetime
from base.models import SoftDeleteAbstractModel
from account.models import User
from django.core.validators import MinLengthValidator
from django.utils.timezone import now


class Specialist(models.TextChoices):
    Family_medicine = 'Family medicine'
    Internal_Medicine = 'Internal Medicine'
    Pediatrician = 'Pediatrician'
    Obstetricians_Gynecologist = 'Obstetricians/gynecologist (OBGYNs)'
    Cardiologist = 'Cardiologist'
    Oncologist = 'Oncologist'
    Gastroenterologist = 'Gastroenterologist'
    Pulmonologist = 'Pulmonologist'
    Infectious_disease = 'Infectious disease'
    Nephrologist = 'Nephrologist'
    Endocrinologist = 'Endocrinologist'
    Ophthalmologist = 'Ophthalmologist'
    Otolaryngologist = 'Otolaryngologist'
    Dermatologist = 'Dermatologist'
    Psychiatrist = 'Psychiatrist'
    Neurologist = 'Neurologist'
    Radiologist = 'Radiologist'
    Anesthesiologist = 'Anesthesiologist'
    Surgeon = 'Surgeon'
    Physician_executive = 'Physician executive'
# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_doctor")
    expertise = models.CharField(max_length=200, default='Dermatology')
    specialize = models.CharField(max_length=50, default='Level II')
    specialist = models.CharField(max_length=50,
                                  choices=Specialist.choices)

    def __str__(self):
        return self.user.name


class Patient(SoftDeleteAbstractModel):
    class Gender(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        UNKNOWN = 'unknown'
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20,
                              choices=Gender.choices,
                              default=Gender.UNKNOWN)
    address = models.CharField(max_length=500, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    temperature = models.FloatField(default=37, blank=True, null=True)
    bood_pressure = models.FloatField(blank=True, null=True)
    heart_rate = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class Schedule(SoftDeleteAbstractModel):
    class Status(models.TextChoices):
        waiting = 'waiting'
        pending = 'pending'
        done = 'done'
    id = models.BigAutoField(primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=12, default="")
    email = models.EmailField(
        max_length=70, blank=True, null=True, default=None, unique=True)
    specialist = models.CharField(max_length=50,
                                  choices=Specialist.choices)
    appointment_date = models.DateField(default=None)
    appointment_time = models.TimeField(default=None)
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.waiting)
    note_to_doctor = models.TextField(blank=True, null=True, default=None)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                               blank=True, null=True)

    def __str__(self) -> str:
        return self.patient_name


class MedicineType(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Medicine(SoftDeleteAbstractModel):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    stock_quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=30)
    usage = models.CharField(max_length=100, blank=True)
    origin_price = models.FloatField()
    sale_price = models.FloatField()
    dose_per_day = models.FloatField()
    medicine_type = models.ForeignKey(MedicineType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Prescription(SoftDeleteAbstractModel):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    diagnosis = models.CharField(max_length=300)
    note = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(
        Medicine, through="PrescriptionDetail", through_fields=['prescription', 'medicine'])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    cur_height = models.FloatField(blank=True, null=True)
    cur_wight = models.FloatField(blank=True, null=True)
    cur_temperature = models.FloatField(blank=True, null=True)
    cur_blood_pressure = models.FloatField(blank=True, null=True)
    cur_heart_rate = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{str(self.patient)} {self.diagnosis} {self.created_at.strftime('%d/%m/%Y')}"


class PrescriptionDetail(SoftDeleteAbstractModel):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    usage = models.CharField(max_length=100)
    number = models.IntegerField(default=0)

    class Meta:
        unique_together = (("prescription", "medicine"),)


class Invoice(SoftDeleteAbstractModel):
    id = models.BigAutoField(primary_key=True, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    medicines = models.ManyToManyField(
        to=Medicine, through='InvoiceDetail', through_fields=['invoice', 'medicine'])
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    stripe_invoice_id = models.CharField(max_length=100, default="")

    def __str__(self) -> str:
        return 'invoice - ' + str(self.id)

    def soft_delete(self):
        self.invoicedetail_set.all().update(deleted_at=datetime.now())
        return SoftDeleteAbstractModel.soft_delete()

    def restore(self):
        self.invoicedetail_set.all().update(deleted_at=None)
        return SoftDeleteAbstractModel.restore()

    @property
    def get_total(self):
        # invoice = Invoice.objects.get(pk=self.id)
        query_result = self.invoicedetail_set.all().aggregate(
            total_price=models.Sum('line_total'))
        return query_result['total_price']


class InvoiceDetail(SoftDeleteAbstractModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    unit_price = models.FloatField(default=0)
    line_total = models.FloatField(default=0)

    @property
    def get_line_total(self):
        return self.quantity * self.unit_price\


    def save(self, *args, **kwargs) -> None:
        self.line_total = self.get_line_total
        return super(InvoiceDetail, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'invoice detail I{self.invoice.id} - M{self.medicine.id}'

    class Meta:
        unique_together = (('invoice', 'medicine'),)
