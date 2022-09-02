from django.shortcuts import render,redirect

from payment.models import Payment
from .forms import CreatePaymentForm
from student.models import Student
from invoice.models import BalanceTable, Invoice

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException
from quickbooks.client import QuickBooks

from itertools import cycle

def create_payment(request,id):
    if request.method == 'POST':
        form = CreatePaymentForm(request.POST)
        student = Student.objects.get(pk=id)
        if form.is_valid():
            payment_object = form.save(commit=False)
                     
            #get the oldest unpaid invoice
            oldest_unpaid_invoice = Invoice.objects.filter(student=student).filter(paid = False).order_by('created').first()
            
            #check whether if you pay the invoice gets overpaid
            if payment_object.amount + oldest_unpaid_invoice.balance > oldest_unpaid_invoice.amount or payment_object.amount > oldest_unpaid_invoice.balance: 
                #payment overpays the invoice
                pass
            else:
                #then just pay the invoice normally
                #update the balance on the invoice
                #this updates the balance of just the invoice
                new_balance = oldest_unpaid_invoice.balance - payment_object.amount
                Invoice.objects.filter(pk = oldest_unpaid_invoice.id).update(balance=new_balance)


            payment_object.invoice = oldest_unpaid_invoice
            payment_object.student = student
            # change the balance of the invoice
            
            payment_object.save()
            #update the balance table
            
            #this updates the total amount of alll the invoices
            bal_table = BalanceTable.objects.get(student=student)
            prev_bal = bal_table.balance
            new_bal = prev_bal - form.cleaned_data['amount']
            bal_table.balance = new_bal
            bal_table.save()

  
            return redirect('student_profile',id)

            #first check if student has any unpaid invoices and if so, collect a list of them
            
        else:
            return render(request, 'payment/create_payment.html',{'form':form,'student':student})
    if request.method == 'GET':

        form = CreatePaymentForm()
        student = Student.objects.get(pk=id)
        return render(request, 'payment/create_payment.html',{'form':form,'student':student})

def make_payment(request,id):
    if request.method == 'POST':
        student_obj = Student.objects.get(pk=1)
        form_obj = CreatePaymentForm(request.POST)

        if form_obj.is_valid():
            payment_obj = form_obj.save(commit=False)
            unpaid_invoices = Invoice.objects.filter(student= student_obj,paid_status=False).order_by('created')
            if unpaid_invoices.exists():
                unpaid_invoices_list = list(unpaid_invoices)
                unpaid_invoices_cycle = cycle(unpaid_invoices_list)
                payment_amount = payment_obj.amount
                while payment_amount is not 0:#Make payments until the amount is spent up
                    invoice = next(unpaid_invoices_cycle)
                    if payment_amount > invoice.balance:
                        #Excess amount being payed
                        excess_amount = payment_obj.amount - invoice.balance
                        #Apply payment to invoice
                        invoice.balance = 0
                        invoice.paid_status = True
                        invoice.save(force_update=True)
                        #Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                        payment_obj.amount = payment_obj.amount - excess_amount
                        payment_obj.save()
                        #Modify the payment amount 
                        payment_amount = excess_amount
                        continue 
                    if payment_amount
                    


                    

            else:
                #queryset is empty
                pass
        else:
            #for is not valid
            pass
    else:
        pass