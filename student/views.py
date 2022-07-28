from sre_constants import SUCCESS
from django.forms import ValidationError
from django.shortcuts import render,redirect
from django.urls import reverse
from regex import P
from academic_calendar.models import AcademicCalendar
from fees_structure.models import FeesStructure
import invoice
from invoice.models import Invoice,Item,BalanceTable
from academic_calendar import utils as academic_utils
from student.models import Student
from .forms import StudentRegistrationForm,EditStudentProfileForm
from invoice import utils as invoice_utils
from django.contrib import messages
from item.models import Item as sales_item

def students(request):
    students = Student.objects.all()
    return render(request, 'student/student.html',{'students':students})

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            #create invoice for student
            invoice = Invoice.objects.create(
                student = student,
            )
            invoice.save()

            #Save invoice items to db
            for item in student.get_items():
                sales_item_obj = sales_item.objects.get(name=item)
                calendar_obj = AcademicCalendar()
                fee_structure_obj = FeesStructure.objects.get(item=sales_item_obj,grade=student.current_grade, term=calendar_obj.get_term())
                local_item_obj = Item.objects.create(
                    item_description = item,
                    amount = fee_structure_obj.amount,
                    invoice = invoice
                )
                local_item_obj.save()


            #Create Balance Object for student
            balance_obj = BalanceTable.objects.create(
                student=student,
                balance = invoice.get_amount()            
            )
            balance_obj.save()

            return redirect(reverse('student_profile',args=[student.id]))
        else:
            return render(request, 'student/registration.html',{'form':form})
    elif request.method == 'GET':
        form = StudentRegistrationForm()
        return render(request, 'student/registration.html',{'form':form})
    
def student_profile(request,id):
    student = Student.objects.get(pk=id)
    invoices = Invoice.objects.filter(student=student)
    return render(request, 'student/student_profile.html',{'student':student,'invoices':invoices})

def edit_student_profile(request,id):
    student = Student.objects.get(pk=id)
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()
            fees_structure_obj = FeesStructure.objects.get(grade = student.current_grade)
            if form.has_changed():
                if 'lunch' in form.changed_data:
                    invoice = student.invoice_set.all().order_by('created').first()
                    #add the lunch to the invoice
                    lunch_item = Item.objects.create(
                        item_description = 'lunch',
                        amount = fees_structure_obj.lunch,
                        invoice = invoice
                    )
                    lunch_item.save()
                    #Student and balance to BalanceTable
                    balance_obj = BalanceTable.objects.get(student=student)
                    balance = balance_obj.balance
                    new_balance = balance + lunch_item.amount
                    balance_obj.balance = new_balance
                    balance_obj.save()

                if 'transport' in form.changed_data:
                    invoice = student.invoice_set.all().order_by('created').first()
                    #add the lunch to the invoice
                    transport_item = Item.objects.create(
                        item_description = 'transport',
                        amount = student.transport_fee,
                        invoice = invoice
                    )
                    transport_item.save()
                    balance_obj = BalanceTable.objects.get(student=student)
                    balance = balance_obj.balance
                    new_balance = balance + transport_item.amount
                    balance_obj.balance = new_balance
                    balance_obj.save()
                return redirect(reverse('student_profile', args=[student.id]))
            else:
                return redirect(reverse('student_profile', args=[student.id]))
        else:
            return render(request,'student/edit_student_profile.html',{'form':form,'student':student})
    if request.method =='GET':
        form = EditStudentProfileForm(instance=student)
        return render(request,'student/edit_student_profile.html',{'form':form,'student':student})

def delete_student(request,id):
    student = Student.objects.get(pk=id)
    student.delete()
    messages.add_message(request, messages.SUCCESS,"Student Deleted Successfully")
    return redirect(reverse('students'))
