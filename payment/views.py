from dal import autocomplete
from email.policy import default
from django.shortcuts import render, redirect

from .models import Payment
from .forms import PaymentCreationForm
from student.models import Student
from invoice.models import BalanceTable, Invoice
from item.models import Item as SalesItem
from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException
from quickbooks.client import QuickBooks

from itertools import cycle
from fees_structure.models import FeesStructure

from academic_calendar.models import AcademicCalendar
from django.contrib import messages
from invoice.models import Item as Invoice_Item
from grade.models import Grade
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response


@login_required()
def payments(request):
    all_payments = Payment.objects.all()
    return render(request, 'payment/payments.html', {'payments': all_payments})


@login_required()
def make_payment(request):
    # Make a payment for student
    # Get the student the payment is being made for
    # make_paymnt_POST
    if request.method == 'POST':
        form_obj = PaymentCreationForm(request.POST)

        if form_obj.is_valid():

            # if you do have a valid  PaymentCreation form you create a payment object that holds the amount of money
            # paid and the date it was paid
            # payment_obj = form_obj.save()  # Payment Object (amount, an date)

            # Check if there are any unpaid invoices , because it does not make sense making a payment for a new \
            # invoice while you stilll have previously unpaid ones
            student_obj = form_obj.cleaned_data['student']
            unpaid_invoices = Invoice.objects.filter(student=student_obj, paid=False).order_by(
                'created')  # Student's unpaid invoices if any, with the oldest one first

            # there are unpaid invoices
            if unpaid_invoices.exists() is True:  # Are there any unapid invoices ?
                # yes
                unpaid_invoices_list = list(
                    unpaid_invoices)  # #make a list of them
                unpaid_invoices_iterator = iter(
                    unpaid_invoices_list)  # turn list to an iterator so that i can call next()

                # the amount to be applied to invoices (amount paid)
                payment_amount = form_obj.cleaned_data['amount']

                while payment_amount != 0:  # Make payments until the amount is spent up

                    invoice = next(unpaid_invoices_iterator, "end")

                    if invoice != "end" and payment_amount > invoice.balance:  # if the payment amount overpays that invoice
                        # Excess amount being payed
                        excess_amount = payment_amount - invoice.balance  # get the amount overpaid

                        # Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                        # Apply the payment for accounting_sims
                        # Minus the excess amount so that it doesnt overpay the qb_invoice.
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount - excess_amount,
                            student=student_obj,  # payment was applied for this student
                            invoice=invoice,  # payment was applied to this invoice
                            note="Payment Split. Overflow to next invoice"
                        )
                        payment_obj.save()  # save the payment both to db and to QB

                        # Apply payment to invoice, for local sims
                        invoice.balance = 0
                        invoice.paid = True
                        invoice.save(update_fields=['balance', 'paid'])

                        # record payment in quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # Now that that invoice is paid for, update the amount paid, to the excess amount so that when the loop runs again it can apply the payment to the next unpaid invoice or create another one of that was the only invoice
                        payment_amount = excess_amount

                        # Update the Balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save(update_fields=['balance'])

                    if invoice != "end" and payment_amount < invoice.balance:
                        # now the payment amount is less than the invoice_balance either from paying a previous invoice or the payment_obj.amount was that way initially
                        # sav the payment object
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount,
                            student=student_obj,
                            invoice=invoice
                        )
                        payment_obj.save()

                        # apply payment to the invoice
                        invoice.balance = invoice.balance - payment_amount
                        invoice.save(update_fields=['balance'])

                        # record transaction to quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # update the Balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        # All the money is spent up
                        payment_amount = 0

                    if invoice != "end" and payment_amount == invoice.balance:
                        # an exact payment has been made
                        # Apply payment to that invoice

                        # save the payment object
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount,
                            student=student_obj,
                            invoice=invoice
                        )
                        payment_obj.save(update_fields=['student', 'invoice'])

                        invoice.balance = 0
                        invoice.paid = True
                        invoice.save(update_fields=['balance', 'paid'])

                        # record transaction to quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # update the balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        # now all the money iis spent up
                        payment_amount = 0
                        break

                    if invoice == 'end' and payment_amount > 0:
                        # if there are no unpaid invoices left to apply payments but there's still payment amount
                        # left.
                        # create a new invoice and apply that invoice there.
                        # by now the balance cannot be greater than the invoice balance.
                        # all the unpaid invoices are now paid for and there's still money left
                        # create an invoice for the next term

                        while payment_amount != 0:
                            # maybe its best t0 fetch the term, grade and year from the previous invoice
                            previous_invoice = Invoice.objects.filter(student=student_obj).order_by(
                                '-created').first()
                            prev_year = previous_invoice.year
                            prev_term = previous_invoice.term
                            prev_grade = previous_invoice.grade

                            # if the kids are still in the current year
                            next_grade = prev_grade
                            next_year = prev_year
                            next_term = prev_term + 1
                            # get the next term year
                            if prev_term + 1 > 3:  # if term 3 and overpayment is made, make an invoice for the next year
                                # Children graduating to a new year, term 1 , next grade
                                if prev_grade.number == 6:
                                    # student goes off to junior secondary.ie extra pay
                                    # deposit that amount to the student's overpay
                                    # i.e if you have overpaid for term 3 and you are in grade 6... where do we put that money ?
                                    # create an empty invoice
                                    # return
                                    pass
                                if prev_grade.number == 8:
                                    # this is a edge case, to facilitate the transitioning of
                                    # class 8 is being phased out
                                    # if youre in grade 8 and you over pay 3rd term's fees, where do we put the money
                                    #  return
                                    pass

                                if prev_grade.number == 101:  # 101 is code for PP1
                                    next_grade = Grade.objects.get(number=102)
                                    next_year = prev_year + 1
                                    next_term = 1

                                if prev_grade.number == 102:  # 102 is code for PP2
                                    next_grade = Grade.objects.get(number=1)
                                    next_year = prev_year + 1
                                    next_term = 1
                                if prev_grade.number == 0:  # 0 is code for play group
                                    next_grade = Grade.objects.get(number=1)
                                    next_year = prev_year + 1
                                    next_term = 1
                                else:
                                    next_grade = Grade.objects.get(
                                        number=prev_grade.number + 1)
                                    next_year = prev_year + 1
                                    next_term = 1

                            # get the amount to be paid for that term
                            # add an invoice for the coming term
                            invoice = Invoice.objects.create(

                                student=student_obj,
                                year=next_year,
                                term=next_term,
                                grade=next_grade
                            )
                            invoice.save()
                            # add items to that invoice
                            items = student_obj.get_items()
                            total_amount = 0
                            for item in items:
                                sales_item = SalesItem.objects.get(name=item)
                                fees_struc = FeesStructure.objects.get(
                                    grade=next_grade,
                                    term=next_term,
                                    item=sales_item
                                )
                                inv_item = Invoice_Item.objects.create(
                                    invoice_item=sales_item,
                                    amount=fees_struc.amount,
                                    invoice=invoice

                                )
                                inv_item.save()
                                total_amount = total_amount + inv_item.amount
                            invoice.amount = total_amount
                            invoice.balance = total_amount
                            invoice.save(update_fields=['balance', 'amount'])

                            # balance table
                            bal_table = BalanceTable.objects.get(
                                student=student_obj)
                            bal_table.balance = bal_table.balance + -total_amount
                            bal_table.save(update_fields=['balance'])

                            if payment_amount > invoice.balance:  # if the payment amount overpays that invoice
                                # Excess amount being payed
                                excess_amount = payment_amount - invoice.balance  # get the amount overpaid

                                # Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                                # Apply the payment for accounting_sims
                                # Minus the excess amount so that it doesnt overpay the qb_invoice.
                                payment_obj = Payment.objects.create(
                                    date_paid=form_obj.cleaned_data['date_paid'],
                                    amount=payment_obj.amount - excess_amount,
                                    student=student_obj,  # payment was applied for this student
                                    invoice=invoice,  # payment was applied to this invoice
                                    note="Payment Split. Overflow to next invoice"
                                )
                                payment_obj.save()  # save the payment both to db and to QB

                                # Apply payment to invoice, for local sims
                                invoice.balance = 0
                                invoice.paid = True
                                invoice.save(update_fields=['balance', 'paid'])

                                # record payment in quickbooks
                                try:
                                    payment_obj.create_qb_payment()
                                except:
                                    pass

                                # Now that that invoice is paid for, update the amount paid, to the excess amount so that when the loop runs again it can apply the payment to the next unpaid invoice or create another one of that was the only invoice
                                payment_amount = excess_amount

                                # Update the Balance table
                                bal_table = BalanceTable.objects.get(
                                    student=student_obj)
                                bal_table.balance = bal_table.balance + payment_obj.amount
                                bal_table.save(update_fields=['balance'])

                            if payment_amount < invoice.balance:
                                # now the payment amount is less than the invoice_balance either from paying a previous invoice or the payment_obj.amount was that way initially
                                # sav the payment
                                payment_obj = Payment.objects.create(
                                    date_paid=form_obj.cleaned_data['date_paid'],
                                    amount=payment_amount,
                                    student=student_obj,
                                    invoice=invoice
                                )
                                payment_obj.save()

                                # apply payment to the invoice
                                invoice.balance = invoice.balance - payment_amount
                                invoice.save(update_fields=['balance'])

                                # record transaction to quickbooks
                                try:
                                    payment_obj.create_qb_payment()
                                except:
                                    pass

                                # update the Balance table
                                bal_table = BalanceTable.objects.get(
                                    student=student_obj)
                                bal_table.balance = bal_table.balance + payment_obj.amount
                                bal_table.save()

                                # All the money is spent up
                                payment_amount = 0

                            if payment_amount == invoice.balance:
                                # an exact payment has been made
                                # Apply payment to that invoice

                                # save the payment object
                                payment_obj = Payment.objects.create(
                                    date_paid=form_obj.cleaned_data['date_paid'],
                                    amount=payment_amount,
                                    student=student_obj,
                                    invoice=invoice
                                )
                                payment_obj.save()

                                invoice.balance = 0
                                invoice.paid = True
                                invoice.save(update_fields=['balance', 'paid'])

                                # record transaction to quickbooks
                                try:
                                    payment_obj.create_qb_payment()
                                except:
                                    pass

                                # update the balance table
                                bal_table = BalanceTable.objects.get(
                                    student=student_obj)
                                bal_table.balance = bal_table.balance + payment_obj.amount
                                bal_table.save()

                                # now all the money iis spent up
                                payment_amount = 0

                # When payment amount is spent up, means the payment was made successfully
                messages.success(
                    request, "Payment made successfully", extra_tags="alert-success")
                return redirect('payments')

            # there are no unpaid invoices
            else:
                # when there are no unpaid invoices and the student makes another payment
                # the amount to applied to invoices (amount paid)
                payment_amount = form_obj.cleaned_data['amount']
                while payment_amount != 0:
                    # maybe its best t0 fetch the term, grade and year from the previous invoice
                    previous_invoice = Invoice.objects.filter(student=student_obj).order_by(
                        '-created').first()
                    prev_year = previous_invoice.year
                    prev_term = previous_invoice.term
                    prev_grade = previous_invoice.grade

                    # if the kids are still in the current year
                    next_grade = prev_grade
                    next_year = prev_year
                    next_term = prev_term + 1
                    # get the next term year
                    if prev_term + 1 > 3:  # if term 3 and overpayment is made, make an invoice for the next year
                        # Children graduating to a new year, term 1 , next grade
                        if prev_grade.number == 6:
                            # student goes off to junior secondary.ie extra pay
                            # deposit that amount to the student's overpay
                            # i.e if you have overpaid for term 3 and you are in grade 6... where do we put that money ?
                            # create an empty invoice
                            # return
                            pass
                        if prev_grade.number == 8:
                            # this is a edge case, to facilitate the transitioning of
                            # class 8 is being phased out
                            # if youre in grade 8 and you over pay 3rd term's fees, where do we put the money
                            # return
                            pass

                        if prev_grade.number == 101:  # 101 is code for PP1
                            next_grade = Grade.objects.get(number=102)
                            next_year = prev_year + 1
                            next_term = 1

                        if prev_grade.number == 102:  # 102 is code for PP2
                            next_grade = Grade.objects.get(number=1)
                            next_year = prev_year + 1
                            next_term = 1
                        if prev_grade.number == 0:  # 0 is code for play group
                            next_grade = Grade.objects.get(number=1)
                            next_year = prev_year + 1
                            next_term = 1
                        else:
                            next_grade = Grade.objects.get(
                                number=prev_grade.number + 1)
                            next_year = prev_year + 1
                            next_term = 1

                    # get the amount to be paid for that term
                    # add an invoice for the coming term
                    invoice = Invoice.objects.create(
                        student=student_obj,
                        year=next_year,
                        term=next_term,
                        grade=next_grade
                    )
                    invoice.save()
                    # add items to that invoice
                    items = student_obj.get_items()
                    total_amount = 0
                    for item in items:
                        sales_item = SalesItem.objects.get(name=item)
                        fees_struc = FeesStructure.objects.get(
                            grade=next_grade,
                            term=next_term,
                            item=sales_item
                        )
                        inv_item = Invoice_Item.objects.create(
                            invoice_item=sales_item,
                            amount=fees_struc.amount,
                            invoice=invoice

                        )
                        inv_item.save()
                        total_amount = total_amount + inv_item.amount
                    invoice.amount = total_amount
                    invoice.balance = total_amount
                    invoice.save(update_fields=['balance', 'amount'])

                    # balance table
                    bal_table = BalanceTable.objects.get(student=student_obj)
                    bal_table.balance = bal_table.balance + -total_amount
                    bal_table.save(update_fields=['balance'])

                    if payment_amount > invoice.balance:  # if the payment amount overpays that invoice
                        # Excess amount being payed
                        excess_amount = payment_amount - invoice.balance  # get the amount overpaid

                        # Modify the payment object so that it pays the invoice exactly(to 0) in Quickbooks
                        # Apply the payment for accounting_sims
                        # Minus the excess amount so that it doesnt overpay the qb_invoice.
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount - excess_amount,
                            student=student_obj,  # payment was applied for this student
                            invoice=invoice,  # payment was applied to this invoice
                            note="Payment Split. Overflow to next invoice"
                        )
                        payment_obj.save()  # save the payment both to db and to QB

                        # Apply payment to invoice, for local sims
                        invoice.balance = 0
                        invoice.paid = True
                        invoice.save(update_fields=['balance', 'paid'])

                        # record payment in quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # Now that that invoice is paid for, update the amount paid, to the excess amount so that when the loop runs again it can apply the payment to the next unpaid invoice or create another one of that was the only invoice
                        payment_amount = excess_amount

                        # Update the Balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save(update_fields=['balance'])

                    if payment_amount < invoice.balance:
                        # now the payment amount is less than the invoice_balance either from paying a previous invoice or the payment_obj.amount was that way initially
                        # sav the payment object
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount,
                            student=student_obj,
                            invoice=invoice
                        )
                        payment_obj.save()

                        # apply payment to the invoice
                        invoice.balance = invoice.balance - payment_amount
                        invoice.save(update_fields=['balance'])

                        # record transaction to quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # update the Balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        # All the money is spent up
                        payment_amount = 0

                    if payment_amount == invoice.balance:
                        # an exact payment has been made
                        # Apply payment to that invoice

                        # save the payment object
                        payment_obj = Payment.objects.create(
                            date_paid=form_obj.cleaned_data['date_paid'],
                            amount=payment_amount,
                            student=student_obj,
                            invoice=invoice
                        )
                        payment_obj.save(update_fields=['student', 'invoice'])

                        invoice.balance = 0
                        invoice.paid = True
                        invoice.save(update_fields=['balance', 'paid'])

                        # record transaction to quickbooks
                        try:
                            payment_obj.create_qb_payment()
                        except:
                            pass

                        # update the balance table
                        bal_table = BalanceTable.objects.get(
                            student=student_obj)
                        bal_table.balance = bal_table.balance + payment_obj.amount
                        bal_table.save()

                        # now all the money iis spent up
                        payment_amount = 0
                        break
                # After everything return to student profile
                messages.success(
                    request, "Payment applied successfully", extra_tags="alert-success")
                return redirect('payments')
            # there are no unpaid invoices
            # now you start the process of applying payments
        else:
            # form != valid
            return render(request, 'payments/create_payment.html', {'form': form_obj})
    if request.method == 'GET':
        # request method
        # make a new payment creation form
        form = PaymentCreationForm()
        return render(request, 'payment/create_payment.html', {'form': form})


@login_required()
def payment_summaries(request):
    return render(request, 'payment/payment_summaries.html')


class StudentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Student.objects.none()

        qs = Student.objects.all()

        if self.q:
            qs = qs.filter(first_name__istartswith=self.q)

        return qs


class PaymentTrendChart(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July'
        ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data = {
            "labels": labels,
            'chartLabel': chartLabel,
            "chartdata": chartdata, }
        return Response(data)
