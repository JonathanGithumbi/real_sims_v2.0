
from payment.PaymentManager import PaymentManager
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from invoice.models import BalanceTable, Invoice
from .forms import PaymentCreationForm
from django.shortcuts import render, redirect
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
from student.models import Student
from django.shortcuts import get_object_or_404
# lists of payments are visible on a per student basis


class PaymentListView(generic.ListView):
    template_name = 'payment_list.html'
    context_object_name = 'payment_list'

    def get_queryset(self):
        self.student = get_object_or_404(Student, pk=self.kwargs['student_pk'])
        return Payment.objects.filter(student=self.student)

    # Add the student to the context so that the templates can use it
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.student


class PaymentCreateView(BSModalCreateView):
    template_name = 'payment/create_payment.html'
    form_class = PaymentModelForm
    success_message = 'Success: Payment was created.'

    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'student_pk': self.kwargs['student_pk']})


class PaymentUpdateView(BSModalUpdateView):
    model = Payment
    template_name = "payment/update_payment.html"
    form_class = PaymentModelForm
    success_message = 'Success: Payment was updated.'

    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'student_pk': self.kwargs['student_pk']})


class PaymentReadView(BSModalReadView):
    model = Payment
    template_name = "payment/read_payment.html"


class PaymentDeleteView(BSModalDeleteView):
    model = Payment
    template_name = "payment/delete_payment.html"
    success_message = "Success: Payment was deleted"
    
    def get_success_url(self):
        return reverse_lazy('payment_list', kwargs={'student_pk': self.kwargs['student_pk']})


def payments(request):
    data = dict()
    if request.method == 'GET':
        payment_list = Payment.objects.all()
        data['table'] = render_to_string(
            '_payments_table.html',
            {'payment_list': payment_list},
            request=request
        )
        return JsonResponse(data)


@login_required()
def payments(request):
    all_payments = Payment.objects.all()
    return render(request, 'payment/payments.html', {'payments': all_payments})

