from .models import Year, Term
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import DateInput


class YearModelForm(BSModalModelForm):
    class Meta:
        model = Year
        fields = ('year', 'start', 'end')

        widgets = {
            'start': DateInput()
        }


class TermModelForm(BSModalModelForm):
    class Meta:
        model = Term
        fields = ['term', 'start', 'end', 'year']

    def __init__(self,*args,**kwargs):
        self.year = kwargs.pop('year')
        super(TermModelForm,self).__init__(*args,**kwargs)
        self.fields['year'].initial = self.year
