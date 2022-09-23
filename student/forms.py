from tkinter.tix import Select
from django.forms import CheckboxInput, DateInput, ModelForm, NumberInput, TextInput, Select,Form
from .models import Student
from . import utils


class StudentRegistrationForm(ModelForm):
    class Meta:
        model = Student
        exclude =['current_grade','synced','admission_number','admission_number_formatted','qb_id']
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control', 'id':'first_name','placeholder':'First Name'}),
            'middle_name': TextInput(attrs={'class':'form-control', 'id':'middle_name','placeholder':'Middle Name'}),
            'last_name': TextInput(attrs={'class':'form-control', 'id':'last_name','placeholder':'Last Name'}),
            'grade_admitted_to': Select(attrs={'class':'form-select','id':'grade_admitted_to'}),
            'date_of_admission': DateInput(attrs={'class':'form-control','id':'date_of_admission'}),
            'primary_contact_name': TextInput(attrs={'class':'form-control', 'id':'primary_contact_name','placeholder':'Primary Contact Name'}),
            'primary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'primary_contact_phone_number','placeholder':'Phone Number'}),
            'secondary_contact_name': TextInput(attrs={'class':'form-control', 'id':'secondary_contact_name','placeholder':'Secondary Contact Name'}),
            'secondary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'secondary_contact_phone_number','placeholder':'Secondary Contact Phone Number'}),
            'lunch': CheckboxInput(attrs={'class':'form-check-input', 'id':'lunch'}),
            'transport': CheckboxInput(attrs={'class':'form-check-input','id':'transport','onclick':'enable_transport_fee()'}),
            

        }

class EditStudentProfileForm(ModelForm):
    class Meta:
        model = Student
        exclude =['current_grade','synced','admission_number','qb_id','grade_admitted_to','admission_number_formatted','date_of_admission']
        widgets = {

            'first_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'First Name'}),
            'middle_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Middle Name'}),
            'last_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Last Name'}),
            'primary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Primary Contact Name'}),
            'primary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Phone Number'}),
            'secondary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Name'}),
            'secondary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Phone Number'}),
            'lunch': CheckboxInput(attrs={'class':'form-check-input', 'id':'lunch'}),
            'transport': CheckboxInput(attrs={'class':'form-check-input','id':'transport','onclick':'enable_transport_fee()'}),
        }
