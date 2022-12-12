#from django.shortcuts import render, redirect
#from django.urls import reverse
#from fees_structure.models import FeesStructure
#from invoice.models import Invoice, Item, BalanceTable
#from payment.models import Payment
#from student.models import Student
#from student.StudentManager import StudentManager
#from .forms import StudentRegistrationForm, EditStudentProfileForm
#from django.contrib import messages
#from item.models import Item as SalesItem
#from django.contrib import messages
#from django.contrib.auth.decorators import login_required
#from payment.forms import PaymentCreationForm
#
#
#@login_required()
#def students(request):
#    all_students = Student.objects.filter(
#        visible=True).order_by('date_of_admission')
#    active_students = Student.objects.filter(active=True).count()
#    # Send Along the student registration form
#    student_registration_form = StudentRegistrationForm()
#    return render(request, 'student/student.html', {'students': all_students, 'active_students': active_students, 'student_registration_form': student_registration_form})
#
#
#@login_required()
#def register_student(request):
#    registration_form = StudentRegistrationForm(request.POST)
#    student_manager = StudentManager()
#    try:
#        registered_student = student_manager.register_student(
#            registration_form)
#    except:  # An Expressionless exception matches any exception
#        raise Exception("Error in Student Manager registering students ")
#    messages.success(request, "{0} {1} {2} registered successfully.".format(
#        registered_student.first_name, registered_student.middle_name, registered_student.last_name), extra_tags="alert-success")
#    return redirect('student_profile', registered_student.id, permanent=True)
#
#
#@login_required()
#def student_profile(request, student_id):
#    student = Student.objects.get(pk=student_id)
#    invoices = Invoice.objects.filter(student=student)
#    payments = Payment.objects.filter(student=student)
#    make_payment_form = PaymentCreationForm()
#    make_payment_form.student = student
#    student_edit_form = EditStudentProfileForm(instance=student)
#    return render(request, 'student/student_profile.html',
#                  {'student': student, 'invoices': invoices, 'payments': payments, 'make_payment_form': make_payment_form, 'student_edit_form': student_edit_form})
#
#
#@login_required()
#def edit_student_details(request, id):
#    student = Student.objects.get(pk=id)
#    prev_data = {
#        'first_name': student.first_name,
#        'middle_name': student.middle_name,
#        'last_name': student.last_name,
#        'grade_admitted_to': student.grade_admitted_to,
#        'date_of_admission': student.date_of_admission,
#        'primary_contact_name': student.primary_contact_name,
#        'primary_contact_phone_number': student.primary_contact_phone_number,
#        'secondary_contact_name': student.secondary_contact_name,
#        'secondary_contact_phone_number': student.secondary_contact_phone_number,
#        'lunch': student.lunch,
#        'transport': student.transport
#    }
#    edit_form = EditStudentProfileForm(
#        request.POST, initial=prev_data, instance=student)  # the initial data
#
#    student_manager = StudentManager()
#    if (student_manager.edit_student(edit_form)):
#        messages.success(request, "Details changed successfully.",
#                         extra_tags='alert-success')
#        return redirect('student_profile', student.id)
#    else:
#        messages.info(request, "No changes made.",
#                      extra_tags='alert-success')
#        return redirect('student_profile', student.id)
#
#
#@login_required()
#def delete_student(request, id):
#    student = Student.objects.get(pk=id)
#    student_manager = StudentManager()
#    student_manager.delete_student(student)
#    messages.success(request, "{0} {1} {2} unregistered successfully.".format(
#        student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")
#    return redirect(reverse('students'))
#
#
#@login_required()
#def inactivate_student(request, id):
#    student = Student.objects.get(pk=id)
#    student_manager = StudentManager()
#    student_manager.inactivate_student(student)
#    messages.success(request, "{0} {1} {2} inactivated successfully.".format(
#        student.first_name, student.middle_name, student.last_name), extra_tags="alert-success")
#    return redirect(reverse('students'))
#