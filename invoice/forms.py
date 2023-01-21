from .models import Invoice
from .models import Item as InvoiceItem
from fees_structure.models import BillingItem
from bootstrap_modal_forms.forms import BSModalModelForm


class InvoiceModelForm(BSModalModelForm):
    class Meta:
        model = Invoice
        fields = ['year', 'term', 'student']

    # this function is involved with chaining select inputs term and year
    def __init__(self, *args, **kwargs):
        self.student_obj = kwargs.pop('student')
        super(InvoiceModelForm, self).__init__(*args, **kwargs)
        from academic_calendar.models import Term
        self.fields['term'].queryset = Term.objects.none()
        self.fields['student'].initial = self.student_obj
        self.fields['student'].widget.attrs['readonly'] = True
        if 'year' in self.data:
            try:
                year_id = int(self.data.get('year'))
                self.fields['term'].queryset = Term.objects.filter(
                    year_id=year_id).order_by('term')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['term'].queryset = self.instance.year.term_set.order_by(
                'term')


class InvoiceItemModelForm(BSModalModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['billing_item', 'invoice']

    def __init__(self, *args, **kwargs):
        self.invoice_obj = kwargs.pop('invoice')
        super(InvoiceItemModelForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].initial = self.invoice_obj
        self.fields['billing_item'].queryset = BillingItem.objects.filter(
            visible=True)
