from django.shortcuts import render
from .forms import CreatePaymentForm


def payments(request,student_id):
    return render(request, 'payment/payments.html')

def create_payment(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        form = CreatePaymentForm()
        return render(request, 'payment/create_payment.html',{'form':form})