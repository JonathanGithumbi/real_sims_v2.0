from .models import Vendor

from bootstrap_modal_forms.forms import BSModalModelForm


class VendorModelForm(BSModalModelForm):
    class Meta:
        model = Vendor
        fields = ['name','phone_number']

    def clean(self):
        super(VendorModelForm,self).clean()

        name = self.cleaned_data.get('name')
        phone_number = self.cleaned_data.get('phone_number')

        if not name.replace(' ','').isalpha():
            self._errors['name'] = self.error_class(['Name cannot contain numbers'])
        
        return self.cleaned_data

