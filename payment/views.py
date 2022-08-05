from django.shortcuts import render
from .forms import CreatePaymentForm
from student.models import Student


def create_payment(request,id):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        form = CreatePaymentForm()
        student = Student.objects.get(pk=id)
        return render(request, 'payment/create_payment.html',{'form':form,'student':student})