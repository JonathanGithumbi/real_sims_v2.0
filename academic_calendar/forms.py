from .models import Year, Term
from bootstrap_modal_forms.forms import BSModalModelForm


class YearModelForm(BSModalModelForm):
    class Meta:
        model = Year
        fields = ('year', 'start', 'end')


class TermModelForm(BSModalModelForm):
    class Meta:
        model = Term
        fields = ('term', 'start', 'end')
        
