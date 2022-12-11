from .models import Item
from bootstrap_modal_forms.forms import BSModalModelForm

class  ItemModelForm(BSModalModelForm):
    class Meta:
        model = Item
        fields = ['name']
        

