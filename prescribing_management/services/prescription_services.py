from prescribing_management.models import PrescriptionDetail, Medicine, Prescription, Patient
from prescribing_management.forms.prescription_forms import PrescriptionForm
from account.models import User


class PrescriptionService:
    def __init__(self) -> None:
        pass

    def get_empty_prescription_with_patient_id(self, patient_id: int or str):
        try:
            return Prescription(patient=Patient.objects.get(pk=patient_id))
        except Patient.DoesNotExist:
            return None

    def is_prescription_detail_valid(self, medicine_ids, medicine_numbers, medicine_usages) -> bool:
        return len(medicine_ids) == len(medicine_numbers)\
            and len(medicine_numbers) == len(medicine_usages) \
            and all(num.isdigit() for num in medicine_numbers) \


    def create_prescription_and_detail(self, form: PrescriptionForm or Prescription, username, medicine_ids, medicine_numbers, medicine_usages):
        if form.is_valid() and self.is_prescription_detail_valid(medicine_ids, medicine_numbers, medicine_usages):
            prescription = form.save(commit=False)
            prescription.created_by = User.objects.get(username=username)
            prescription.save()
            for i in range(len(medicine_ids)):
                prescription_detail = PrescriptionDetail(medicine=Medicine.objects.get(pk=medicine_ids[i]),
                                                         prescription=prescription,
                                                         number=medicine_numbers[i],
                                                         usage=medicine_usages[i])
                prescription_detail.save()
            return True
        return False

    def edit_prescription_and_detail(self, form: PrescriptionForm or Prescription,  medicine_ids, medicine_numbers, medicine_usages):
        if form.is_valid() and self.is_prescription_detail_valid(medicine_ids, medicine_numbers, medicine_usages):

            prescription = form.save()
            prescription_details = prescription.prescriptiondetail_set.all()
            new_medicine_id_set = {id for id in medicine_ids}
            old_medicine_id_set = {str(detail.medicine.id)
                                   for detail in prescription_details}

            for i in range(len(medicine_ids)):
                # update => new medicine with id have already in old set
                if medicine_ids[i] in new_medicine_id_set & old_medicine_id_set:

                    detail = prescription_details.get(
                        medicine__id=medicine_ids[i])
                    detail.number = medicine_numbers[i]
                    detail.usage = medicine_usages[i]
                    detail.save()
                # create => new medicine with id don't have in old set
                elif medicine_ids[i] in new_medicine_id_set - old_medicine_id_set:
                    detail = PrescriptionDetail(medicine=Medicine.objects.get(pk=medicine_ids[i]),
                                                prescription=prescription,
                                                number=medicine_numbers[i],
                                                usage=medicine_usages[i])
                    detail.save()
            # delete => old medicine with id don't have in new id set
            for id in old_medicine_id_set - new_medicine_id_set:

                detail = prescription_details.get(medicine__id=id)
                detail.delete()
            return True
        return False
