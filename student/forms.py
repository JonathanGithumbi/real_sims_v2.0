
from django.forms import CheckboxInput, DateInput, ModelForm, NumberInput, TextInput, Select, Form
from .models import Student
from . import utils


class StudentRegistrationForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'grade_admitted_to',
            'primary_contact_name', 'primary_contact_phone_number', 'secondary_contact_name', 'secondary_contact_phone_number', 'lunch', 'transport'
        ]
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'first_name'}),
            'middle_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'middle_name'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'last_name'}),
            'grade_admitted_to': Select(attrs={'class': 'form-control form-control-sm', 'id': 'grade_admitted_to'}),
            'date_of_admission': DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'date_of_admission'}),
            'primary_contact_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'primary_contact_name'}),
            'primary_contact_phone_number': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'primary_contact_phone_number'}),
            'secondary_contact_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'secondary_contact_name'}),
            'secondary_contact_phone_number': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'secondary_contact_phone_number'}),
            'lunch': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'lunch', 'type': 'checkbox'}),
            'transport': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'transport', 'type': 'checkbox'}),


        }


class EditStudentProfileForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name',
            'primary_contact_name', 'primary_contact_phone_number', 'secondary_contact_name', 'secondary_contact_phone_number', 'lunch', 'transport'
        ]
        widgets = {

            'first_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'middle_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'last_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'primary_contact_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'primary_contact_phone_number': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'secondary_contact_name': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'secondary_contact_phone_number': TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'floatingInput'}),
            'lunch': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'lunch'}),
            'transport': CheckboxInput(attrs={'class': 'form-check-input', 'id': 'transport', 'onclick': 'enable_transport_fee()'}),
        }
