from .models import Invoice
from .models import Item as InvoiceItem

from bootstrap_modal_forms.forms import BSModalModelForm


class InvoiceModelForm(BSModalModelForm):
    class Meta:
        model = Invoice
        fields = ['year', 'term']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        from academic_calendar.models import Term
        self.fields['term'].queryset = Term.objects.none()

        if 'year' in self.data:
            try:
                year_id = int(self.data.get('year'))
                self.fields['term'].queryset = Term.objects.filter(year_id=year_id).order_by('term')
            except(ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['term'].queryset = self.instance.year.term_set.order_by('term')

    
class InvoiceItemModelForm(BSModalModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['sales_item', 'amount', 'invoice']
