
from .models import Student
from bootstrap_modal_forms.forms import BSModalModelForm


class StudentModelForm(BSModalModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'grade_admitted_to',
            'contact1_name', 'contact1_number', 'contact2_name', 'contact2_number', 'active'
        ]
