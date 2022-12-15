from .models import Item as InvoiceItem
from .models import Invoice
from django.template.loader import render_to_string
from .forms import InvoiceItemModelForm, InvoiceModelForm
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

# lists of invoices are visible on a per student basis


class InvoiceListView(generic.ListView):
    template_name = 'invoice_list.html'
    context_object_name = 'invoice_list'

    def get_queryset(self):
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return Invoice.objects.filter(student=self.student)

    # Add the student to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student
        return context


class InvoiceCreateView(BSModalCreateView):
    template_name = 'invoice/create_invoice.html'
    form_class = InvoiceModelForm
    success_message = 'Success: Invoice was created.'

    def get_success_url(self):
        return reverse_lazy('invoice_list', kwargs={'student_pk': self.kwargs['student_pk']})


class InvoiceUpdateView(BSModalUpdateView):
    model = Invoice
    template_name = "invoice/update_invoice.html"
    form_class = InvoiceModelForm
    success_message = 'Success: Invoice was updated.'

    def get_success_url(self):
        return reverse_lazy('invoice_list', kwargs={'student_pk': self.kwargs['student_pk']})


class InvoiceReadView(BSModalReadView):
    model = Invoice
    template_name = "invoice/read_invoice.html"


class InvoiceDeleteView(BSModalDeleteView):
    model = Invoice
    template_name = "invoice/delete_invoice.html"
    success_message = "Success: Invoice was deleted"

    def get_success_url(self):
        return reverse_lazy('invoice_list', kwargs={'student_pk': self.kwargs['student_pk']})


def invoices(request):
    data = dict()
    if request.method == 'GET':
        invoice_list = Invoice.objects.all()
        data['table'] = render_to_string(
            '_invoices_table.html',
            {'invoice_list': invoice_list},
            request=request
        )
        return JsonResponse(data)


# lists of invoiceitems are visible on a per invoice

class InvoiceItemListView(generic.ListView):
    template_name = 'invoiceitem_list.html'
    context_object_name = 'invoiceitem_list'

    def get_queryset(self):
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return InvoiceItem.objects.filter(invoice=self.invoice)

    # Add the student to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['student'] = self.student
        return context


class InvoiceItemCreateView(BSModalCreateView):
    template_name = 'invoice/create_invoiceitem.html'
    form_class = InvoiceItemModelForm
    success_message = 'Success: InvoiceItem was created.'

    def get_queryset(self):
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return InvoiceItem.objects.filter(invoice=self.invoice)

    # Add the student to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['student'] = self.student
        return context

    def get_success_url(self):
        return reverse_lazy('invoiceitem_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


class InvoiceItemUpdateView(BSModalUpdateView):
    model = InvoiceItem
    template_name = "invoice/update_invoiceitem.html"
    form_class = InvoiceItemModelForm
    success_message = 'Success: InvoiceItem was updated.'

    def get_queryset(self):
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return InvoiceItem.objects.filter(invoice=self.invoice)

    # Add the student to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['student'] = self.student
        return context

    def get_success_url(self):
        return reverse_lazy('invoiceitem_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


class InvoiceItemReadView(BSModalReadView):
    model = InvoiceItem
    template_name = "invoice/read_invoiceitem.html"


class InvoiceItemDeleteView(BSModalDeleteView):
    model = InvoiceItem
    template_name = "invoice/delete_invoiceitem.html"
    success_message = "Success: InvoiceItem was deleted"

    def get_success_url(self):
        return reverse_lazy('invoiceitem_list', kwargs={'invoice_pk': self.kwargs['invoice_pk']})


def invoiceitems(request):
    data = dict()
    if request.method == 'GET':
        invoiceitem_list = InvoiceItem.objects.all()
        data['table'] = render_to_string(
            '_invoiceitems_table.html',
            {'invoiceitem_list': invoiceitem_list},
            request=request
        )
        return JsonResponse(data)
