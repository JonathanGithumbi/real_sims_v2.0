
from .models import Student
from bootstrap_modal_forms.forms import BSModalModelForm



class StudentModelForm(BSModalModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'grade_admitted_to',
            'primary_contact_name', 'primary_contact_phone_number', 'secondary_contact_name', 'secondary_contact_phone_number', 'lunch', 'transport'
        ]

    


