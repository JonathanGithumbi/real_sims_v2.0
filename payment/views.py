from django.shortcuts import render,redirect
from .forms import CreatePaymentForm
from student.models import Student
from invoice.models import BalanceTable

def create_payment(request,id):
    if request.method == 'POST':
        form = CreatePaymentForm(request.POST)
        student = Student.objects.get(pk=id)
        if form.is_valid():
            payment_object = form.save(commit=False)
            payment_object.student = student
            payment_object.save()
            #update the balance table
            
            bal_table = BalanceTable.objects.get(student=student)
            prev_bal = bal_table.balance
            new_bal = prev_bal - form.cleaned_data['amount']
            bal_table.balance = new_bal
            bal_table.save()
            return redirect('student_profile',id)
        else:
            return render(request, 'payment/create_payment.html',{'form':form,'student':student})
    if request.method == 'GET':
        form = CreatePaymentForm()
        student = Student.objects.get(pk=id)
        return render(request, 'payment/create_payment.html',{'form':form,'student':student})