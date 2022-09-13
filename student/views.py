from sre_constants import SUCCESS
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse
from regex import P
from academic_calendar.models import AcademicCalendar
from fees_structure.models import FeesStructure
import invoice
from invoice.models import Invoice, Item, BalanceTable

from payment.models import Payment
from student.models import Student
from .forms import StudentRegistrationForm, EditStudentProfileForm
from invoice import utils as invoice_utils
from django.contrib import messages
from item.models import Item as SalesItem

from quickbooks import QuickBooks
from quickbooks.objects import Customer

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Invoice as QB_Invoice
from quickbooks.objects.detailline import SalesItemLine, SalesItemLineDetail
from quickbooks.objects import Customer
from quickbooks.objects import Item as QB_Item
from quickbooks.exceptions import QuickbooksException
from datetime import date
from django.contrib import messages


def students(request):
    all_students = Student.objects.all().order_by('date_of_admission')
    return render(request, 'student/student.html', {'students': all_students})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # save the student to the database
            student = form.save()
            # save teh student as a customer in qb
            try:
                qb_customer = student.create_qb_customer()
                student.synced = True
                student.qb_id = qb_customer.Id
            except QuickbooksException as e:
                # if there is an error when trying to create the customer
                # research possible errors that might occur
                # what to do when an exception occurs
                # build a retry workflow using celery
                pass
            except ConnectionError as e:
                pass

            # charge the student the term's fees
            # create invoice for student
            invoice = Invoice.objects.create(
                student=student,
            )
            ac_cal = AcademicCalendar()
            invoice.term = ac_cal.get_term()
            invoice.year = ac_cal.get_year()
            invoice.save()  # saving the iinvoice now so that invoice items can have something to refefrence
            # Populate the lisst of items that the student is going to pay for
            # Get bare minimum items required
            items = student.get_items()
            # add Items for new students Students
            items.append("Admission")
            items.append("Diaries")
            items.append("Report Books")
            if student.student_is_upper_class():
                items.append("Upper Class Interview Fee")
            else:
                items.append("Lower Class Interview Fee")

            # Save invoice items to db these are not saved directly to qb
            for item in items:
                sales_item_obj = SalesItem.objects.get(name=item)
                calendar_obj = AcademicCalendar()
                fee_structure_obj = FeesStructure.objects.get(item=sales_item_obj, grade=student.current_grade,
                                                              term=calendar_obj.get_term())
                # Item in this case refers to invoice item
                local_item_obj = Item.objects.create(
                    invoice_item=sales_item_obj,
                    amount=fee_structure_obj.amount,
                    invoice=invoice
                )
                local_item_obj.save()
            # add amount and balance
            invoice.amount = invoice.get_amount()
            invoice.balance = invoice.get_amount()
            # calling update_fields should force an update
            invoice.save(update_fields=['amount', 'balance'])

            # record invoice in quickbooks
            try:
                qb_invoice = invoice.create_qb_invoice()
                invoice.synced = True
                invoice.qb_id = qb_invoice
                # also keep system logs
            except QuickbooksException as e:
                # log and add retry workflow
                pass

            # Create Balance record for student
            balance_obj = BalanceTable.objects.create(
                student=student,
                balance=-(invoice.get_amount())  # a negative number indicates that the student owes the school money
            )
            balance_obj.save()
            return redirect(reverse('student_profile', args=[student.id]))
        else:
            return render(request, 'student/registration.html', {'form': form})
    elif request.method == 'GET':
        # i want to register student only when the term has begun
        aca_cal = AcademicCalendar()
        today_date = date.today()
        if aca_cal.term_begun(today_date):
            form = StudentRegistrationForm()
            return render(request, 'student/registration.html', {'form': form})
        else:
            messages.error(request, "Please wait until the term begins to register new students.",
                           extra_tags='alert-warning')
            return redirect(students)


def student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    invoices = Invoice.objects.filter(student=student)
    payments = Payment.objects.filter(student=student)
    return render(request, 'student/student_profile.html',
                  {'student': student, 'invoices': invoices, 'payments': payments})


def edit_student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, instance=student)  # the instance
        if form.is_valid():
            if form.has_changed():
                if 'lunch' in form.changed_data:
                    #   a. get the lunch item
                    lunch_item = SalesItem.objects.get(name='Lunch')
                    if form.cleaned_data['lunch'] == True:
                        # This is subscribing a student to lunch 
                        # 1. Fetch the student's latest invoice 
                        latest_invoice = Invoice.objects.filter(student=student).order_by('-created')[0]

                        # 2 Add Lunch to that invoice
                        # get academic calendar obj
                        cal_obj = AcademicCalendar()
                        # get price of lunch item
                        fees_struc = FeesStructure.objects.get(grade=student.current_grade, term=cal_obj.get_term(),
                                                               item=lunch_item)
                        # add the item to the invoice
                        invoice_item = Item.objects.create(
                            invoice_item=lunch_item,
                            amount=fees_struc.amount,
                            invoice=latest_invoice
                        )
                        # save the invoice_item
                        invoice_item.save()

                        #save the transaction to quickbooks
                        try:
                            latest_invoice.update_qb_invoice(lunch_item)
                        except QuickbooksException as e:
                            #what do i do when the update fails to add the item to the invoice ?
                            pass

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + -(invoice_item.amount)
                        bal_table.save()


                        # update the student subscripiton to lunnch
                        Student.objects.filter(pk=student_id).update(lunch=True)

                if 'transport' in form.changed_data:
                    transport_item = SalesItem.objects.get(name='Transport')
                    if form.cleaned_data['transport'] == True:
                        # This is subscribing a student to transport 
                        # 1. Fetch the student's latest invoice 
                        latest_invoice = Invoice.objects.filter(student=student).order_by('-created')[0]

                        # 2 Add Lunch to that invoice
                        # get academic calendar obj
                        cal_obj = AcademicCalendar()
                        # get price of lunch item
                        fees_struc = FeesStructure.objects.get(grade=student.current_grade, term=cal_obj.get_term(),
                                                               item=transport_item)
                        # a create an invoice item for that item
                        invoice_item = Item.objects.create(
                            invoice_item=transport_item,
                            amount=fees_struc.amount,
                            invoice=latest_invoice
                        )
                        # save the invoice_item
                        invoice_item.save()

                        try:
                            latest_invoice.update_qb_invoice(transport_item)
                        except QuickbooksException as e:
                            pass

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + -(invoice_item.amount)
                        bal_table.save()


                        # update model
                        Student.objects.filter(pk=student_id).update(transport=True)

                # Name change triggers name change in quickbooks
                if 'first_name' in form.changed_data or 'middle_name' in form.changed_data or 'last_name ' in form.changed_data:
                    access_token_obj = Token.objects.get(name='access_token')
                    refresh_token_obj = Token.objects.get(name='refresh_token')
                    realm_id_obj = Token.objects.get(name='realm_id')
                    # create an auth_client
                    auth_client = AuthClient(
                        client_id=settings.CLIENT_ID,
                        client_secret=settings.CLIENT_SECRET,
                        access_token=access_token_obj.key,
                        environment=settings.ENVIRONMENT,
                        redirect_uri=settings.REDIRECT_URI
                    )
                    # create a quickboooks client
                    client = QuickBooks(
                        auth_client=auth_client,
                        refresh_token=refresh_token_obj.key,
                        company_id=realm_id_obj.key
                    )
                    customer = Customer.get(student.qb_id, qb=client)
                    customer.DisplayName = form.cleaned_data['first_name'] + ' ' + form.cleaned_data[
                        'middle_name'] + ' ' + form.cleaned_data['last_name']
                    try:
                        customer.save(qb=client)
                    except QuickbooksException as e:
                        pass


                    Student.objects.filter(pk=student_id).update(
                        first_name=form.cleaned_data['first_name'])
                    Student.objects.filter(pk=student_id).update(
                        middle_name=form.cleaned_data['middle_name'])
                    Student.objects.filter(pk=student_id).update(
                        last_name=form.cleaned_data['last_name'])
                if 'primary_contact_name' in form.changed_data:
                    student_instance = Student.objects.filter(pk=student_id).update(
                        primary_contact_name=form.cleaned_data['primary_contact_name'])
                if 'primary_contact_phone_number' in form.changed_data:
                    student_instance = Student.objects.filter(pk=student_id).update(
                        primary_contact_phone_number=form.cleaned_data['primary_contact_phone_number'])
                if 'secondary_contact_name' in form.changed_data:
                    student_instance = Student.objects.filter(pk=student_id).update(
                        secondary_contact_name=form.cleaned_data['secondary_contact_name'])
                if 'secondary_contact_phone_number' in form.changed_data:
                    student_instance = Student.objects.filter(pk=student_id).update(
                        secondary_contact_phone_number=form.cleaned_data['secondary_contact_phone_number'])

            return redirect('student_profile', student.id)
        else:
            # form is not valid
            pass
    if request.method == 'GET':
        form = EditStudentProfileForm(instance=student)
        return render(request, 'student/edit_student_profile.html', {'form': form, 'student': student})


def delete_student(request, id):
    student = Student.objects.get(pk=id)
    student.delete()
    messages.add_message(request, messages.SUCCESS, "Student Deleted Successfully")
    return redirect(reverse('students'))
