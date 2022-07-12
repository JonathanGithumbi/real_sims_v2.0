from django.forms import ValidationError
from django.shortcuts import render,redirect
from django.urls import reverse
from regex import P
from fees_structure.models import FeesStructure
import invoice
from invoice.models import Invoice,Item
from academic_calendar import utils as academic_utils
from student.models import Student
from .forms import StudentRegistrationForm,EditStudentProfileForm
from invoice import utils as invoice_utils

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
                #created = default now,
                grade = student.grade_admitted_to,
                term = academic_utils.get_term(student.date_of_admission),
                year = student.date_of_admission.year,
                status = 'unpaid',
                
            )
            invoice.save()
            #Fees Structure object to get item price
            fees_structure_obj = FeesStructure.objects.get(grade = student.grade_admitted_to)
            #create the items to add to the invoice
            items = student.get_items()
            for item in items:
                item_obj = Item.objects.create(
                    item_description = item,
                    invoice = invoice
                )
                if item =='tuition':
                    item_obj.amount = fees_structure_obj.tuition
                if item =='transport':
                    item_obj.amount = fees_structure_obj.transport
                if item == 'lunch':
                    item_obj.amount = fees_structure_obj.lunch

                item_obj.save()
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

                if 'transport' in form.changed_data:
                    invoice = student.invoice_set.all().order_by('created').first()
                    #add the lunch to the invoice
                    transport_item = Item.objects.create(
                        item_description = 'transport',
                        amount = student.transport_fee,
                        invoice = invoice
                    )
                    transport_item.save()

                return redirect(reverse('student_profile', args=[student.id]))
            else:
                return redirect(reverse('student_profile', args=[student.id]))
        else:
            return render(request,'student/edit_student_profile.html',{'form':form,'student':student})
    if request.method =='GET':
        form = EditStudentProfileForm(instance=student)
        return render(request,'student/edit_student_profile.html',{'form':form,'student':student})
