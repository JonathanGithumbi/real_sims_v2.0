from .models import BillItem
from .models import Bill
from django.template.loader import render_to_string
from .forms import BillItemModelForm, BillModelForm, BillPaymentModelForm
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
from .CashManager import CashManager
from .models import BillPayment
from .BillManager import BillManager
# lists of bills are visible on a per student basis


class BillListView(generic.ListView):
    model = Bill
    template_name = 'bill_list.html'
    context_object_name = 'bill_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill_man = BillManager()
        context['total_amount_due_bills'] = bill_man.get_total_amount_due_bills()
        return context


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
        bill = get_object_or_404(Bill, pk=self.kwargs['bill_pk'])
        context['bill'] = get_object_or_404(Bill, pk=self.kwargs['bill_pk'])

        bill_man = BillManager()
        context['total_amount_due_billitems'] = bill_man.get_total_amount_due_billitems(
            bill)
        return context


class BillItemCreateView(BSModalCreateView):
    template_name = 'bill/create_billitem.html'
    form_class = BillItemModelForm
    success_message = 'Success: Bill Item was created.'

    # overriding the get_form_kwargs to add kwargs to the form before instantiation
    def get_form_kwargs(self):
        kwargs = super(BillItemCreateView, self).get_form_kwargs()
        bill_obj = Bill.objects.get(pk=self.kwargs['bill_pk'])
        kwargs.update({'bill_obj': bill_obj})
        return kwargs

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
        billitem_list = BillItem.objects.filter(bill=bill)
        data['table'] = render_to_string(
            '_billitems_table.html',
            {'billitem_list': billitem_list, 'bill': bill},
            request=request
        )
        return JsonResponse(data)


# lists of bill payments are visible on a per billitem basis

class BillPaymentListView(generic.ListView):
    template_name = 'billpayment_list.html'
    context_object_name = 'billpayment_list'

    def get_queryset(self):
        self.billitem = get_object_or_404(
            BillItem, pk=self.kwargs['billitem_pk'])
        return BillPayment.objects.filter(billitem=self.billitem)

    # Add the  to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['billitem'] = get_object_or_404(
            BillItem, pk=self.kwargs['billitem_pk'])
        context['bill'] = get_object_or_404(Bill, pk=self.kwargs['bill_pk'])
        return context


class BillPaymentCreateView(BSModalCreateView):
    template_name = 'bill/create_billpayment.html'
    form_class = BillPaymentModelForm
    success_message = 'Success: Billpayment was created.'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(BillPaymentCreateView, self).get_form_kwargs()
        billitem = BillItem.objects.get(pk=self.kwargs['billitem_pk'])
        kwargs.update({'billitem': billitem})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('billpayment_list', kwargs={'billitem_pk': self.kwargs['billitem_pk'], 'bill_pk': self.kwargs['bill_pk']})


class BillPaymentUpdateView(BSModalUpdateView):
    model = BillPayment
    template_name = "bill/update_billpayment.html"
    form_class = BillPaymentModelForm
    success_message = 'Success: Bill payment was updated.'

    def get_form_kwargs(self, **kwargs):
        kwargs = super(BillPaymentUpdateView, self).get_form_kwargs()
        billitem = BillItem.objects.get(pk=self.kwargs['billitem_pk'])
        kwargs.update({'billitem': billitem})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill'] = get_object_or_404(
            Bill, pk=self.kwargs['bill_pk'])

        return context

    def get_success_url(self):
        return reverse_lazy('billpayment_list', kwargs={'billitem_pk': self.kwargs['billitem_pk'], 'bill_pk': self.kwargs['bill_pk']})


class BillPaymentReadView(BSModalReadView):
    model = BillPayment
    template_name = "bill/read_billpayment.html"


class BillPaymentDeleteView(BSModalDeleteView):
    model = BillPayment
    template_name = "bill/delete_billpayment.html"
    success_message = "Success: Billpayment was deleted"

    def get_success_url(self):
        return reverse_lazy('billpayment_list', kwargs={'billitem_pk': self.kwargs['billitem_pk'], 'bill_pk': self.kwargs['bill_pk']})


def billpayments(request, billitem_pk):
    billitem = get_object_or_404(BillItem, pk=billitem_pk)
    bill = billitem.bill
    data = dict()
    if request.method == 'GET':
        billpayment_list = BillPayment.objects.filter(billitem=billitem)
        data['table'] = render_to_string(
            '_billpayments_table.html',
            {'billpayment_list': billpayment_list,
                'billitem': billitem, 'bill': bill},
            request=request
        )
        return JsonResponse(data)
