
from .models import Student
from bootstrap_modal_forms.forms import BSModalModelForm


class StudentModelForm(BSModalModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'grade_admitted_to',
            'contact1_name', 'contact1_number', 'contact2_name', 'contact2_number', 'active'
        ]

    def clean(self):
        #The super function gets data from the form
        super(StudentModelForm,self).clean()

        #extract the fields you want to do validation on 
        first_name = self.cleaned_data.get('first_name')
        middle_name = self.cleaned_data.get('middle_name')
        last_name = self.cleaned_data.get('last_name')
        contact1_name = self.cleaned_data.get('contact1_name')
        contact2_name = self.cleaned_data.get('contact2_name')
        contact1_number = self.cleaned_data.get('contact1_number')
        contact2_number = self.cleaned_data.get('contact2_number')

        #add conditions to be met for the fields
        #names should not have numeric characters.
        if not first_name.isalpha():
            self._errors['first_name'] = self.error_class(['Name cannot contain numbers.'])
        if not middle_name.isalpha():
            self._errors['middle_name'] = self.error_class(['Name cannot contain numbers.'])
        if not last_name.isalpha():
            self._errors['last_name'] = self.error_class(['Name cannot contain numbers.'])
        if not contact1_name.replace(' ','').isalpha():
            self._errors['contact1_name'] = self.error_class(['Name cannot contain numbers.'])
        if not contact2_name.replace(' ','').isalpha():
            self._errors['contact2_name'] = self.error_class(['Name cannot contain numbers.'])
        #Phone numbers should not contain alphabets
        if not contact1_number.isnumeric():
            self._errors['contact1_number'] = self.error_class(['Number cannot contain letters.'])
        if not contact2_number.isnumeric():
            self._errors['contact2_number'] = self.error_class(['Number cannot contain letters.'])

        #return any errors if found
        return self.cleaned_data
    