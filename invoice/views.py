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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = Student.objects.get(pk=self.kwargs['student_pk'])
        return context

    # overriding the get_form_kwargs to add kwargs to the form before instantiation
    def get_form_kwargs(self):
        """returns the kwargs for instantiating the form"""
        kwargs = super(InvoiceCreateView, self).get_form_kwargs()
        student = Student.objects.get(pk=self.kwargs['student_pk'])
        kwargs.update({'student': student})
        return kwargs

    def get_success_url(self):
        # how to get the invoice that was just created ?
        # why is my self.object not populated?
        # answer: bcause i overrided the create form and never returned the object after i was finished with it
        # reverse to invoice list instead
        print(self.object)
        return reverse_lazy('invoice_list', kwargs={'student_pk': self.kwargs['student_pk']})


class InvoiceUpdateView(BSModalUpdateView):
    model = Invoice
    template_name = "invoice/update_invoice.html"
    form_class = InvoiceModelForm
    success_message = 'Success: Invoice was updated.'

    # i need to add the student to the form's kwargs so i can prepopulate the student field
    def get_form_kwargs(self):
        kwargs = super(InvoiceUpdateView, self).get_form_kwargs()
        student = Student.objects.get(pk=self.kwargs['student_pk'])
        kwargs.update({'student': student})
        return kwargs

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


def invoices(request, student_pk):
    data = dict()
    if request.method == 'GET':
        invoice_list = Invoice.objects.filter(
            student=Student.objects.get(pk=student_pk))
        data['table'] = render_to_string(
            '_invoices_table.html',
            {'invoice_list': invoice_list,
                'student': Student.objects.get(pk=student_pk)},
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
        context['invoice'] = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        context['student'] = Student.objects.get(pk=self.kwargs['student_pk'])
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
        context['invoice'] = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        context['student'] = Student.objects.get(pk=self.kwargs['student_pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(InvoiceItemCreateView, self).get_form_kwargs()
        invoice = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        kwargs.update({'invoice': invoice})
        return kwargs

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
        return reverse_lazy('invoiceitem_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


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
