from tkinter.tix import Select
from django.forms import CheckboxInput, DateInput, ModelForm, NumberInput, TextInput, Select
from .models import Student
from . import utils


class StudentRegistrationForm(ModelForm):
    class Meta:
        model = Student
        exclude =['current_grade','synced','admission_number','admission_number_formatted']
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'First Name'}),
            'middle_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Middle Name'}),
            'last_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Last Name'}),
            'grade_admitted_to': Select(attrs={'class':'form-select'}),
            'date_of_admission': DateInput(attrs={'class':'form-control'}),
            'primary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Primary Contact Name'}),
            'primary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Phone Number'}),
            'secondary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Name'}),
            'secondary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Phone Number'}),
            'hot_lunch': CheckboxInput(attrs={'class':'form-check-input', 'id':'floatingInput'}),
            'transport': CheckboxInput(attrs={'class':'form-check-input','id':'transport','onclick':'enable_transport_fee()'}),
            'transport_fee': NumberInput(attrs={'class':'form-control', 'id':'transport_fee','placeholder':'Transport Fee','value':0}),

        }

class EditStudentProfileForm(ModelForm):
    class Meta:
        model = Student
        exclude =['current_grade','synced','admission_number',]
        widgets = {
            'admission_number_formatted': TextInput(attrs={'class':'form-control', 'id':'floatingInput','readonly':'readonly'}),
            'first_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'First Name'}),
            'middle_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Middle Name'}),
            'last_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Last Name'}),
            'grade_admitted_to': Select(attrs={'class':'form-select'}),
            'date_of_admission': DateInput(attrs={'class':'form-control'}),
            'primary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Primary Contact Name'}),
            'primary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Phone Number'}),
            'secondary_contact_name': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Name'}),
            'secondary_contact_phone_number': TextInput(attrs={'class':'form-control', 'id':'floatingInput','placeholder':'Secondary Contact Phone Number'}),
            'hot_lunch': CheckboxInput(attrs={'class':'form-check-input', 'id':'floatingInput'}),
            'transport': CheckboxInput(attrs={'class':'form-check-input','id':'transport','onclick':'enable_transport_fee()'}),
            'transport_fee': NumberInput(attrs={'class':'form-control', 'id':'transport_fee','placeholder':'Transport Fee','value':0}),

        }
