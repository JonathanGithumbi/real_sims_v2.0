from email.policy import default
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

from academic_calendar.models import AcademicCalendar


def make_payment(request,id):
    student_obj = Student.objects.get(pk=id)
    if request.method == 'POST':
        form_obj = CreatePaymentForm(request.POST)

        if form_obj.is_valid():
            payment_obj = form_obj.save(commit=False)# Payment Object (amount, an date)
            unpaid_invoices = Invoice.objects.filter(student= student_obj,paid_status=False).order_by('created')# Student's unpaid invoices if any, with the oldest one first
            if unpaid_invoices.exists():# Are there any unapid invoices ?
                #yes
                unpaid_invoices_list = list(unpaid_invoices) # #make a list of them
                unpaid_invoices_cycle = cycle(unpaid_invoices_list)#turn list to an iterable so that i can call next()
                payment_amount = payment_obj.amount  #the amount to applied to invoices (amount paid)
                while payment_amount != 0:#Make payments until the amount is spent up
                    invoice = next(unpaid_invoices_cycle,"end") #get the first oldest unpaid invoice
                    
                    if payment_amount > invoice.balance:#if the payment amount overpays that invoice
                        #Excess amount being payed
                        excess_amount = payment_obj.amount - invoice.balance #get the amount overpaid
                        #Apply payment to invoice, for local sims
                        invoice.balance = 0
                        invoice.paid_status = True
                        invoice.save(force_update=True)
                        #Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                        #Apply the payment for accounting_sims
                        #Minus the excess amount so that it doesnt overpay the qb_invoice.
                        payment_obj.amount = payment_obj.amount - excess_amount
                        payment_obj.student = student_obj #payment was applied for this student
                        payment_obj.invoice = invoice #payment was applied to this invoice
                        payment_obj.save()#save the payment both to db and to QB

                        #Now that that invoice is paid for, update the amount paid, to the excess amount so that when the loop runs again it can apply the payment to the next unpaid invoice or create another one of that was the only invoice
                        payment_amount = excess_amount

                        #Update the Balance table
                        bal_table = BalanceTable.objects.get(student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()
                        continue
        

                    if payment_amount < invoice.balance:
                        #now the payment amount is less than the invoice_balance either from paying a previous invoice or the payment_obj.amount was that way initially
                        #apply payment to the invoice
                        invoice.balance = invoice.balance - payment_amount
                        invoice.save(force_update=True)
                        #sav the payment object
                        payment_obj.student = student_obj
                        payment_obj.invoice = invoice
                        payment_obj.save()
                        
                        #update the Balance table
                        bal_table = BalanceTable.objects.get(student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        #All the money is spent up
                        payment_amount = 0

                    if payment_amount == invoice.balance:
                        #an exact payment has been made 
                        #Apply payment to that invoice
                        invoice.balance = 0
                        invoice.paid_status = True
                        
                        #save the payment object
                        payment_obj.student = student_obj
                        payment_obj.invoice = invoice
                        payment_obj.save()

                        #update the balance table
                        bal_table = BalanceTable.objects.get(student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        #now all the money iis spent up
                        payment_amount = 0


                    if invoice == 'end' and payment_amount > 0:#if there are no incoices left to apply payments but there's still payments left, also covers if there
                        #create a new invoice and apply that invoice there.
                        #by now the balance cannot be greater than the invoice balance.
                        cal_obj = AcademicCalendar()
                        current_term = cal_obj.get_term()# the current term were in whhen the overpayment is made
                        current_year = cal_obj.get_year()# the current year were in whhen the overpayment is made
                        if current_term == 3:#if term 3 and overpayment is made, make an invoice for the next year
                            new_year = current_year + 1
                        new_term = current_term + 1 # make th invoice to be applied for the next term

                        invoice = Invoice.objects.create(
                            student = student_obj,
                            year = new_year,
                            term = new_term,
                            amount = payment_amount,
                            balance = payment_amount
                        )
                        invoice.save()
                        #make payment for that invoice with the remaining payment amount
                        new_payment = Payment.objects.create(
                            amount = payment_amount,
                            invoice = invoice,
                            student = student_obj
                        )
                        new_payment.save()
                        #alter the balance of the invoice
                        invoice.balance = payment_amount
                        invoice.save(force_update=True)
                        #set the payment_amount to 0 to exit the loop
                        payment_amount = 0
                else:
                    #When the payment amount is spent up return to the profile page
                    return redirect('student_profile',id)
            else:
                #when the student has paid all of his invoices and still makes another payment
                payment_amount = payment_obj.amount  #the amount to applied to invoices (amount paid)
                while payment_amount != 0:#Make payments until the amount is spent up
                    cal_obj = AcademicCalendar()
                    current_term = cal_obj.get_term()# the current term were in whhen the overpayment is made
                    current_year = cal_obj.get_year()# the current year were in whhen the overpayment is made
                    if current_term == 3:#if term 3 and overpayment is made, make an invoice for the next year
                        new_year = current_year + 1
                    new_term = current_term + 1 # make th invoice to be applied for the next term


                    #create a new invoice until all the money is spent up
                    invoice = Invoice.objects.create(
                        student = student_obj,
                        year = new_year,
                        term = new_term,
                        amount = payment_amount,
                        balance = payment_amount
                    )
                    
                    if payment_amount > invoice.balance:#if the payment amount overpays that invoice
                        #Excess amount being payed
                        excess_amount = payment_obj.amount - invoice.balance #get the amount overpaid
                        #Apply payment to invoice, for local sims
                        invoice.balance = 0
                        invoice.paid_status = True
                        invoice.save(force_update=True)
                        #Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                        #Apply the payment for accounting_sims
                        #Minus the excess amount so that it doesnt overpay the qb_invoice.
                        payment_obj.amount = payment_obj.amount - excess_amount
                        payment_obj.student = student_obj #payment was applied for this student
                        payment_obj.invoice = invoice #payment was applied to this invoice
                        payment_obj.save()#save the payment both to db and to QB

                        #Now that that invoice is paid for, update the amount paid, to the excess amount so that when the loop runs again it can apply the payment to the next unpaid invoice or create another one of that was the only invoice
                        payment_amount = excess_amount

        

                    if payment_amount < invoice.balance:
                        #now the payment amount is less than the invoice_balance either from paying a previous invoice or the payment_obj.amount was that way initially
                        #apply payment to the invoice
                        invoice.balance = invoice.balance - payment_amount
                        invoice.save(force_update=True)
                        #sav the payment object
                        payment_obj.student = student_obj
                        payment_obj.invoice = invoice
                        payment_obj.save()

                        #All the money is spent up
                        payment_amount = 0

                    if payment_amount == invoice.balance:
                        #an exact payment has been made 
                        #Apply payment to that invoice
                        invoice.balance = 0
                        invoice.paid_status = True
                        
                        #save the payment object
                        payment_obj.student = student_obj
                        payment_obj.invoice = invoice
                        payment_obj.save()

                        #now all the money iis spent up
                        payment_amount = 0


                    if invoice == 'end' and payment_amount>0:#if there are no incoices left to apply payments but there's still payments left, also covers if there
                        #create a new invoice and apply that invoice there.
                        #by now the balance cannot be greater than the invoice balance.
                        cal_obj = AcademicCalendar()
                        current_term = cal_obj.get_term()# the current term were in whhen the overpayment is made
                        current_year = cal_obj.get_year()# the current year were in whhen the overpayment is made
                        if current_term == 3:#if term 3 and overpayment is made, make an invoice for the next year
                            new_year = current_year + 1
                        new_term = current_term + 1 # make th invoice to be applied for the next term

                        invoice = Invoice.objects.create(
                            student = student_obj,
                            year = new_year,
                            term = new_term,
                            amount = payment_amount,
                            balance = payment_amount
                        )
                        invoice.save()
                        #make payment for that invoice with the remaining payment amount
                        new_payment = Payment.objects.create(
                            amount = payment_amount,
                            invoice = invoice,
                            student = student_obj
                        )
                        new_payment.save()
                        #alter the balance of the invoice
                        invoice.balance = payment_amount
                        invoice.save(force_update=True)
                        #set the payment_amount to 0 to exit the loop
                        payment_amount = 0
                
                #After everything return to student profile
                return redirect('student_profile',id)
                
        else:
            #form != valid
            form = CreatePaymentForm(request.POST)
            return render(request,'payments/create_payment.html',{'form':form})
    else:
        #request method GET
        form = CreatePaymentForm()
        return render(request, 'payment/create_payment.html',{'form':form,'student':student_obj})