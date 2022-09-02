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
from payment.models import Payment
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
from quickbooks.objects import Customer
from quickbooks.objects import Item as QB_Item

def students(request):
    students = Student.objects.all().order_by('date_of_admission')
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
            invoice.term = invoice.get_term()
            invoice.year = invoice.created.year
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
                    invoice_item = sales_item_obj,
                    amount = fee_structure_obj.amount,
                    invoice = invoice
                )
                local_item_obj.save()

            invoice.amount = invoice.get_amount()
            invoice.balance = invoice.get_amount()
            invoice.save()
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
    payments = Payment.objects.filter(student = student)
    return render(request, 'student/student_profile.html',{'student':student,'invoices':invoices,'payments':payments})

def edit_student_profile(request,id):
    student = Student.objects.get(pk=id)
    if request.method == 'POST':
        form = EditStudentProfileForm(request.POST, instance=student)#the instance
        if form.is_valid():
            if form.has_changed():
                if 'lunch' in form.changed_data:
                    #   a. get the lunch item
                    lunch_item = sales_item.objects.get(name='Lunch')
                    if form.cleaned_data['lunch'] == True:
                        #This is subscribing a student to lunch 
                        #1. Fetch the student's latest invoice 
                        latest_invoice = Invoice.objects.filter(student=student).order_by('-created')[0]

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

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + invoice_item.amount
                        bal_table.save()

                        #Reflect changes in the quickbooks by sparse updating the iinvoice
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
                        #Get qb_invoice
                        qb_invoice_obj = QB_Invoice.get(latest_invoice.qb_id, qb=client)
                        #Add a sales itemline for lunch
                        #create a line line detail to go into the line
                        sales_item_line_detail = SalesItemLineDetail()

                        #Populate line detail's ItemRef

                            #get qb item obj 
                        qb_item_obj =  QB_Item.get(id=lunch_item.qb_id,qb=client)
                            #assign ItemRef
                        sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
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
                        sales_item_line.Description = lunch_item.name

                        qb_invoice_obj.Line.append(sales_item_line)

                        #save the invoice
                        qb_invoice_obj.save(qb=client)

                         #update model
                        student_instance = Student.objects.filter(pk=id).update(lunch=True)

                if 'transport' in form.changed_data:
                    transport_item = sales_item.objects.get(name='Transport') 
                    if form.cleaned_data['transport'] == True:
                        #This is subscribing a student to transport 
                        #1. Fetch the student's latest invoice 
                        latest_invoice = Invoice.objects.filter(student=student).order_by('-created')[0]

                        #2 Add Lunch to that invoice
                        # get academic calendar obj
                        cal_obj = AcademicCalendar()
                        # get price of lunch item
                        fees_struc = FeesStructure.objects.get(grade=student.current_grade,term=cal_obj.get_term(),item=transport_item )
                        # a create an invoice item for that item
                        invoice_item = Item.objects.create(
                            invoice_item = transport_item,
                            amount = fees_struc.amount,
                            invoice = latest_invoice
                        )
                        # save the invoice_item
                        invoice_item.save()

                        bal_table = BalanceTable.objects.get(student=student)
                        bal_table.balance = bal_table.balance + invoice_item.amount
                        bal_table.save()

                        #Reflect changes in the quickbooks by sparse updating the iinvoice
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
                        #Get qb_invoice
                        qb_invoice_obj = QB_Invoice.get(latest_invoice.qb_id, qb=client)
                        #Add a sales itemline for lunch
                        #create a line line detail to go into the line
                        sales_item_line_detail = SalesItemLineDetail()

                        #Populate line detail's ItemRef

                            #get qb item obj 
                        qb_item_obj =  QB_Item.get(id=transport_item.qb_id,qb=client)
                            #assign ItemRef
                        sales_item_line_detail.ItemRef = qb_item_obj.to_ref()
                        #populate line detail quantity
                        sales_item_line_detail.Qty = 1
                        #populate the line detail's unit price - to be determined from the fees structure
                        calendar_obj = AcademicCalendar()
                        current_grade = student.current_grade
                        term = calendar_obj.get_term()
                        fee_structure_obj = FeesStructure.objects.get(item=transport_item, grade=current_grade,term= term)
                        sales_item_line_detail.UnitPrice = fee_structure_obj.amount

                        #create line 
                        sales_item_line = SalesItemLine()
                        sales_item_line.SalesItemLineDetail = sales_item_line_detail
                        sales_item_line.Amount = fee_structure_obj.amount
                        sales_item_line.Description = transport_item.name

                        qb_invoice_obj.Line.append(sales_item_line)

                        #save the invoice
                        qb_invoice_obj.save(qb=client)

                         #update model
                        student_instance = Student.objects.filter(pk=id).update(transport=True)

                #Name change triggers name change in quickbooks
                if 'first_name' in form.changed_data or 'middle_name' in form.changed_data or 'last_name ' in form.changed_data:
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
                    customer = Customer.get(student.qb_id, qb=client)
                    customer.DisplayName = form.cleaned_data['first_name'] +' '+form.cleaned_data['middle_name']+' '+form.cleaned_data['last_name']
                    customer.save(qb=client)
                    student_instance = Student.objects.filter(pk=id).update(first_name=form.cleaned_data['first_name'])
                    student_instance = Student.objects.filter(pk=id).update(middle_name=form.cleaned_data['middle_name'])
                    student_instance = Student.objects.filter(pk=id).update(last_name=form.cleaned_data['last_name'])
                if 'primary_contact_name' in form.changed_data:
                    student_instance = Student.objects.filter(pk=id).update(primary_contact_name=form.cleaned_data['primary_contact_name'])
                if 'primary_contact_phone_number' in form.changed_data:
                    student_instance = Student.objects.filter(pk=id).update(primary_contact_phone_number=form.cleaned_data['primary_contact_phone_number'])
                if 'secondary_contact_name' in form.changed_data:
                    student_instance = Student.objects.filter(pk=id).update(secondary_contact_name=form.cleaned_data['secondary_contact_name'])
                if 'secondary_contact_phone_number' in form.changed_data:
                    student_instance = Student.objects.filter(pk=id).update(secondary_contact_phone_number=form.cleaned_data['secondary_contact_phone_number'])

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
