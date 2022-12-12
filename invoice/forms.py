from .models import Invoice
from .models import Item as InvoiceItem

from bootstrap_modal_forms.forms import BSModalModelForm


class InvoiceModelForm(BSModalModelForm):
    class Meta:
        model = Invoice
        fields = ['student', 'grade', 'year', 'term', ]


class InvoiceItemModelForm(BSModalModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['sales_item', 'amount', 'invoice']
