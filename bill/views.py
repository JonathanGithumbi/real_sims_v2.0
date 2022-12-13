from .models import BillItem
from .models import Bill
from django.template.loader import render_to_string
from .forms import BillItemModelForm, BillModelForm
from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView)
from django.urls import reverse_lazy
from django.views import generic
from student.models import Student
from django.shortcuts import get_object_or_404

# lists of bills are visible on a per student basis


class BillListView(generic.ListView):
    model = Bill
    template_name = 'bill_list.html'
    context_object_name = 'bill_list'


class BillCreateView(BSModalCreateView):
    template_name = 'bill/create_bill.html'
    form_class = BillModelForm
    success_message = 'Success: Bill was created.'
    success_url = reverse_lazy('bill_list')


class BillUpdateView(BSModalUpdateView):
    model = Bill
    template_name = "bill/update_bill.html"
    form_class = BillModelForm
    success_message = 'Success: Bill was updated.'
    success_url = reverse_lazy('bill_list')


class BillReadView(BSModalReadView):
    model = Bill
    template_name = "bill/read_bill.html"


class BillDeleteView(BSModalDeleteView):
    model = Bill
    template_name = "bill/delete_bill.html"
    success_message = "Success: Bill was deleted"
    success_url = reverse_lazy('bill_list')


def bills(request):
    data = dict()
    if request.method == 'GET':
        bill_list = Bill.objects.all()
        data['table'] = render_to_string(
            '_bills_table.html',
            {'bill_list': bill_list},
            request=request
        )
        return JsonResponse(data)


# lists of billitems are visible on a per bill basis

class BillItemListView(generic.ListView):
    template_name = 'billitem_list.html'
    context_object_name = 'billitem_list'

    def get_queryset(self):
        self.bill = get_object_or_404(Bill, pk=self.kwargs['bill_pk'])
        return BillItem.objects.filter(bill=self.bill)

    # Add the  to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill'] = self.bill
        return context


class BillItemCreateView(BSModalCreateView):
    template_name = 'bill/create_billitem.html'
    form_class = BillItemModelForm
    success_message = 'Success: BillItem was created.'

    def get_success_url(self):
        return reverse_lazy('billitem_list', kwargs={'bill_pk': self.kwargs['bill_pk']})


class BillItemUpdateView(BSModalUpdateView):
    model = BillItem
    template_name = "bill/update_billitem.html"
    form_class = BillItemModelForm
    success_message = 'Success: BillItem was updated.'

    def get_success_url(self):
        return reverse_lazy('billitem_list', kwargs={'bill_pk': self.kwargs['bill_pk']})


class BillItemReadView(BSModalReadView):
    model = BillItem
    template_name = "bill/read_billitem.html"


class BillItemDeleteView(BSModalDeleteView):
    model = BillItem
    template_name = "bill/delete_billitem.html"
    success_message = "Success: BillItem was deleted"

    def get_success_url(self):
        return reverse_lazy('billitem_list', kwargs={'bill_pk': self.kwargs['bill_pk']})


def billitems(request, bill_pk):
    bill = get_object_or_404(Bill, pk=bill_pk)
    data = dict()
    if request.method == 'GET':
        billitem_list = BillItem.objects.all()
        data['table'] = render_to_string(
            '_billitems_table.html',
            {'billitem_list': billitem_list, 'bill': bill},
            request=request
        )
        return JsonResponse(data)
