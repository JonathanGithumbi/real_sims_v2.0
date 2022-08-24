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

from quickbooks import QuickBooks
from quickbooks.objects import Customer

from user_account.models import Token
from intuitlib.client import AuthClient
from django.conf import ENVIRONMENT_VARIABLE, settings

from quickbooks.exceptions import QuickbooksException
from quickbooks.objects import Invoice as QB_Invoice
from quickbooks.objects.detailline import SalesItemLine,SalesItemLineDetail
from quickbooks.objects import Customers
from quickbooks.objects import Item as QB_Item

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

            items = student.get_items()
            #Items for Registering Students 
            items.append("Admission")
            items.append("Diaries")
            items.append("Report Books")
            if student.student_is_upper_class():
                items.append("Upper Class Interview Fee")
            else:
                items.append("Lower Class Interview Fee")

            #Save invoice items to db
            for item in items:
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
            if form.has_changed():
                if 'lunch' in form.changed_data:
                    #   a. get the lunch item
                    lunch_item = sales_item.objects.get(name='Lunch')
                    if form.lunch == True:
                        #This is subscribing a student to lunch 
                        #1. Fetch the student's latest invoice 
                        latest_invoice = Invoice.objects.filter(student=student).order_by('-created')

                        #2 Add Lunch to that invoice
                        # get academic calendar obj
                        cal_obj = AcademicCalendar()
                        # get price of lunch item
                        fees_struc = FeesStructure.objects.get(grade=student.current_grade,term=cal_obj.get_term(),item=lunch_item )
                        # a create an invoice item for that item
                        invoice_item = Item.objects.create(
                            invoice_item = lunch_item,
                            amount = fees_struc.amount,
                            invoice = latest_invoice
                        )
                        # save the invoice_item
                        invoice_item.save()

                        #3. Modify the Invoice in quickbooks
                        #   a. setup for API calls
                        access_token_obj = Token.objects.get(name='access_token')
                        refresh_token_obj = Token.objects.get(name='refresh_token')
                        realm_id_obj = Token.objects.get(name='realm_id')
                        #create an auth_client
                        auth_client = AuthClient(
                            client_id = settings.CLIENT_ID,
                            client_secret = settings.CLIENT_SECRET,
                            access_token = access_token_obj.key,
                            environment=settings.ENVIRONMENT,
                            redirect_uri = settings.REDIRECT_URI
                        )
                        #create a quickboooks client
                        client = QuickBooks(
                            auth_client = auth_client,
                            refresh_token = refresh_token_obj.key,
                            company_id = realm_id_obj.key
                        )

                        #get invoice by id and update
                        invoice = QB_Invoice.get(latest_invoice.qb_id)
                                    #create a line line detail to go into the line
                        sales_item_line_detail = SalesItemLineDetail()

                        #Populate line detail's ItemRef
                            #get local item obj
                        lunch_item = sales_item.objects.get(name = 'Lunch')
                            #get qb item obj 
                        qb_lunch_item_obj =  QB_Item.get(id=lunch_item.qb_id,qb=client)
                            #assign ItemRef
                        sales_item_line_detail.ItemRef = qb_lunch_item_obj.to_ref()
                        #populate line detail quantity
                        sales_item_line_detail.Qty = 1
                        #populate the line detail's unit price - to be determined from the fees structure
                        calendar_obj = AcademicCalendar()
                        current_grade = student.current_grade
                        term = calendar_obj.get_term()
                        fee_structure_obj = FeesStructure.objects.get(item=lunch_item, grade=current_grade,term= term)
                        sales_item_line_detail.UnitPrice = fee_structure_obj.amount

                        #create line 
                        sales_item_line = SalesItemLine()
                        sales_item_line.SalesItemLineDetail = sales_item_line_detail
                        sales_item_line.Amount = fee_structure_obj.amount
                        sales_item_line.Description = lunch_item

                        invoice.Line.append(sales_item_line)
                        invoice.save(qb=client)

                        #update the balance table
                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + fee_structure_obj.amount
                        bal_table.save()

                    if form.lunch == False:
                        pass 
                if 'transport' in form.changed_data:
                    if form.transport == True:
                        pass
                    if form.transport == False:
                        pass
                if 'first_name' in form.changed_data:
                    pass
                if 'middle_name' in form.changed_data:
                    pass
                if 'last_name' in form.changed_data:
                    pass

                if 'primary_contact_name' in form.changed_data:
                    pass
                if 'primary_contact_phone_number' in form.changed_data:
                    pass
                if 'secondary_contact_name' in form.changed_data:
                    pass
                if 'primary_contact_phone_number' in form.changed_data:
                    pass
                
                form.save()
                return redirect('student_profile',student.id)
        else: 
            #form is valid 
            pass
    if request.method =='GET':
        form = EditStudentProfileForm(instance=student)
        return render(request,'student/edit_student_profile.html',{'form':form,'student':student})

def delete_student(request,id):
    student = Student.objects.get(pk=id)
    student.delete()
    messages.add_message(request, messages.SUCCESS,"Student Deleted Successfully")
    return redirect(reverse('students'))
