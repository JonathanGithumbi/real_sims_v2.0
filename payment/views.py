from django.shortcuts import render
from .models import Payment
from django.template.loader import render_to_string
from .forms import PaymentModelForm
from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView)
from django.urls import reverse_lazy
from django.views import generic
from invoice.models import Invoice
from student.models import Student
from django.shortcuts import get_object_or_404
# lists of payments are visible on a per invoice basis


class PaymentListView(generic.ListView):
    template_name = 'payment_list.html'
    context_object_name = 'payment_list'

    def get_queryset(self):
        self.invoice = get_object_or_404(Invoice, pk=self.kwargs['invoice_pk'])
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return Payment.objects.filter(invoice=self.invoice)

    # Add the invoice to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = self.invoice
        context['student'] = self.student
        return context


class PaymentCreateView(BSModalCreateView):
    template_name = 'payment/create_payment.html'
    form_class = PaymentModelForm
    success_message = 'Success: Payment was created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        context['student'] = Student.objects.get(pk=self.kwargs['student_pk'])

        return context

    # add invoice and student to modelform  **kwargs
    def get_form_kwargs(self):
        kwargs = super(PaymentCreateView, self).get_form_kwargs()
        invoice = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        student = Student.objects.get(pk=self.kwargs['student_pk'])
        kwargs.update({'invoice': invoice, 'student': student})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


class PaymentUpdateView(BSModalUpdateView):
    model = Payment
    template_name = "payment/update_payment.html"
    form_class = PaymentModelForm
    success_message = 'Success: Payment was updated.'

    # add invoice and student to modelform  **kwargs
    def get_form_kwargs(self):
        kwargs = super(PaymentUpdateView, self).get_form_kwargs()
        invoice = Invoice.objects.get(pk=self.kwargs['invoice_pk'])
        student = Student.objects.get(pk=self.kwargs['student_pk'])
        kwargs.update({'invoice': invoice, 'student': student})
        return kwargs

    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


class PaymentReadView(BSModalReadView):
    model = Payment
    template_name = "payment/read_payment.html"


class PaymentDeleteView(BSModalDeleteView):
    model = Payment
    template_name = "payment/delete_payment.html"
    success_message = "Success: Payment was deleted"

    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'invoice_pk': self.kwargs['invoice_pk'], 'student_pk': self.kwargs['student_pk']})


def payments(request, invoice_pk, student_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    student = get_object_or_404(Student, pk=student_pk)
    data = dict()
    if request.method == 'GET':
        payment_list = Payment.objects.filter(invoice=invoice)
        data['table'] = render_to_string(
            '_payments_table.html',
            {'payment_list': payment_list, 'invoice': invoice, 'student': student},
            request=request
        )
        return JsonResponse(data)
