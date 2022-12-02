from django.shortcuts import render, redirect
from django.urls import reverse
from fees_structure.models import FeesStructure
from invoice.models import Invoice, Item, BalanceTable
from payment.models import Payment
from student.models import Student
from student.StudentManager import StudentManager
from .forms import StudentRegistrationForm, EditStudentProfileForm
from django.contrib import messages
from item.models import Item as SalesItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from payment.forms import PaymentCreationForm


@login_required()
def students(request):
    all_students = Student.objects.all().order_by('date_of_admission')
    return render(request, 'student/student.html', {'students': all_students})


@login_required()
def register_student(request):
    if request.method == 'POST':

        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Get student object
            student = form.save(commit=False)
            student_manager = StudentManager()
            student_manager.register_student(student=student)
            messages.success(request, "{0} {1} {2} registered successfully.".format(
                student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")
            return redirect(reverse('student_profile', args=[student.id]))
        else:
            messages.error(
                request, "Error Registering Student", extra_tags='alert-error')
            return render(request, 'student/registration.html', {'form': form})
    elif request.method == 'GET':
        form = StudentRegistrationForm()
        return render(request, 'student/registration.html', {'form': form})
        return redirect(students)


@login_required()
def student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    invoices = Invoice.objects.filter(student=student)
    payments = Payment.objects.filter(student=student)
    make_payment_form = PaymentCreationForm()
    make_payment_form.student = student
    return render(request, 'student/student_profile.html',
                  {'student': student, 'invoices': invoices, 'payments': payments, 'make_payment_form': make_payment_form})


@login_required()
def edit_student_profile(request, student_id):
    student = Student.objects.get(pk=student_id)
    if request.method == 'POST':
        prev_data = {
            'first_name': student.first_name,
            'middle_name': student.middle_name,
            'last_name': student.last_name,
            'grade_admitted_to': student.grade_admitted_to,
            'date_of_admission': student.date_of_admission,
            'primary_contact_name': student.primary_contact_name,
            'primary_contact_phone_number': student.primary_contact_phone_number,
            'secondary_contact_name': student.secondary_contact_name,
            'secondary_contact_phone_number': student.secondary_contact_phone_number,
            'lunch': student.lunch,
            'transport': student.transport
        }
        form = EditStudentProfileForm(
            request.POST, initial=prev_data)  # the initial data
        if form.is_valid():
            if form.has_changed():
                if 'lunch' in form.changed_data:
                    #   a. get the lunch item
                    lunch_item = SalesItem.objects.get(name='Lunch')
                    if form.cleaned_data['lunch'] == True:
                        # This is subscribing a student to lunch
                        # fetch the student's invoice for the current term
                        ac_cal = AcademicCalendar()
                        current_invoice = Invoice.objects.get(
                            year=ac_cal.get_year(), term=ac_cal.get_term(), student=student)

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
                            invoice=current_invoice)
                        # save the invoice_item, i.e increase the invoice item to the invoice.
                        invoice_item.save()
                        # increase the amount on the invoice by the amount of this item
                        current_invoice.amount = current_invoice.amount + invoice_item.amount
                        # increae the balance on the invoice by the amount of this item
                        current_invoice.balance = current_invoice.balance + invoice_item.amount
                        current_invoice.save(
                            update_fields=['amount', 'balance'])

                        # save the transaction to quickbooks
                        try:
                            current_invoice.update_qb_invoice(lunch_item)
                        except:
                            # what do i do when the update fails to add the item to the invoice ?
                            pass

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + -invoice_item.amount
                        bal_table.save()

                        # update the student subscripiton to lunnch
                        Student.objects.filter(
                            pk=student_id).update(lunch=True)
                        messages.success(request, "{0} {1} {2} subscribed to lunch successfully.".format(
                            student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")

                if 'transport' in form.changed_data:
                    transport_item = SalesItem.objects.get(name='Transport')
                    if form.cleaned_data['transport'] == True:
                        # This is subscribing a student to transport
                        # fetch the student's invoice for the current term
                        ac_cal = AcademicCalendar()
                        current_invoice = Invoice.objects.get(
                            year=ac_cal.get_year(), term=ac_cal.get_term(), student=student)
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
                            invoice=current_invoice
                        )
                        # save the invoice_item
                        invoice_item.save()
                        # increase the amount on the invoice by the amount of this item
                        current_invoice.amount = current_invoice.amount + invoice_item.amount
                        # increae the balance on the invoice by the amount of this item
                        current_invoice.balance = current_invoice.balance + invoice_item.amount
                        current_invoice.save(
                            update_fields=['amount', 'balance'])

                        try:
                            current_invoice.update_qb_invoice(transport_item)
                        except:
                            pass

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + - \
                            (invoice_item.amount)
                        bal_table.save()

                        # update model
                        Student.objects.filter(
                            pk=student_id).update(transport=True)
                        messages.success(request, "{0} {1} {2} subscribed to transport successfully.".format(
                            student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")

                # Name change triggers name change in quickbooks
                if 'first_name' in form.changed_data or 'middle_name' in form.changed_data or 'last_name ' in form.changed_data:

                    student.first_name = form.cleaned_data['first_name']
                    student.middle_name = form.cleaned_data['middle_name']
                    student.last_name = form.cleaned_data['last_name']
                    student.save(update_fields=[
                                 'first_name', 'middle_name', 'last_name'])

                    # reflect changes to quickbooks
                    try:
                        student.update_qb_customer(student)
                    except:
                        pass
                    messages.success(request, "Name Changed to {0} {1} {2}.".format(
                        student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")

                if 'primary_contact_name' in form.changed_data:
                    Student.objects.filter(pk=student_id).update(
                        primary_contact_name=form.cleaned_data['primary_contact_name'])
                    messages.success(request, "Primary Contact Changed to :  {0}".format(
                        form.cleaned_data['primary_contact_name']), extra_tags="alert-success")
                if 'primary_contact_phone_number' in form.changed_data:
                    Student.objects.filter(pk=student_id).update(
                        primary_contact_phone_number=form.cleaned_data['primary_contact_phone_number'])
                    messages.success(request, "Primary Contact Phone Number Changed to :  {0}".format(
                        form.cleaned_data['primary_contact_phone_number']), extra_tags="alert-success")
                if 'secondary_contact_name' in form.changed_data:
                    Student.objects.filter(pk=student_id).update(
                        secondary_contact_name=form.cleaned_data['secondary_contact_name'])
                    messages.success(request, "Secondary Contact Changed to :  {0}".format(
                        form.cleaned_data['secondary_contact_name']), extra_tags="alert-success")
                if 'secondary_contact_phone_number' in form.changed_data:
                    Student.objects.filter(pk=student_id).update(
                        secondary_contact_phone_number=form.cleaned_data['secondary_contact_phone_number'])
                    messages.success(request, "Secondary Contact Phone Number Changed to :  {0}".format(
                        form.cleaned_data['secondary_contact_phone_number']), extra_tags="alert-success")
                # after everything redirect back to the stuudent profile
                return redirect(student_profile, student.id)
            else:
                # form has not changed
                messages.info(
                    request, "No changes made to the student's profile", extra_tags='alert-info')
                return redirect(student_profile, student.id)
        else:
            #form is not valid
            return render(request, 'student/edit_student_profile.html', {'form': form, 'student': student})
    if request.method == 'GET':
        form = EditStudentProfileForm(instance=student)
        return render(request, 'student/edit_student_profile.html', {'form': form, 'student': student})


@login_required()
def delete_student(request, id):
    student = Student.objects.get(pk=id)
    balance = BalanceTable.objects.get(student=student)
    if balance.balance < 0:
        # student has balance sp dont delete
        messages.info(
            request, "Cannot Unregister Student Until Fees Arrears Cleared.", extra_tags="alert-danger")
        return redirect(reverse('students'))
    else:
        student.delete()
        messages.add_message(request, messages.SUCCESS, "{0} {1} {2} Unregistered Successfully".format(
            student.first_name, student.middle_name, student.last_name))
        return redirect(reverse('students'))


@login_required()
def inactivate_student(request, id):
    student = Student.objects.get(pk=id)
    student.active = False
    student.save(update_fields=['active'])
    messages.success(request, "Student Inactivated Successfully ")
    return redirect(reverse('students'))
