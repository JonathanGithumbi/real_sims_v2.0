from django.apps import apps

AdmissionNumber = apps.get_model('student','AdmissionNumber')
class AdmissionNumberGenerator():
    """This class handles the generation of admission numbers"""

    def retrieve_latest_adm_no(self):
        self.adm_no = AdmissionNumber.objects.all().order_by('-created').first()

        return self.adm_no

    def generate_admission_number(self,adm_no):
        self.adm_no = self.retrieve_latest_adm_no(adm_no)
        self.formated_adm_no = 's'+str(self.adm_no.id).zfill(4)
        return self.formated_adm_no