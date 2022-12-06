from django.shortcuts import redirect, render

from student.models import Student
from bill.models import BillItem
from django.db.models import Sum
from invoice.models import Invoice
from academic_calendar.models import AcademicCalendar
from payment.models import Payment
from django.contrib.auth.decorators import login_required


@login_required()
def dashboard(request):
    
    return render(request, 'dashboard/dashboard.html')


@login_required()
def get_tot_no_students(request):
    """Gets the total number of registered students"""
    tot_no_stu = Student.objects.filter(active=True).count()
    return tot_no_stu


@login_required()
def get_tot_amt_unpaid_bills(reqeust):
    unpaid_bills = BillItem.objects.filter(
        fully_paid=False).aggregate(total=Sum('total'))
    if unpaid_bills['total'] == None:
        return 0
    else:
        return unpaid_bills['total']


@login_required()
def get_tot_amt_unpaid_fees_term(request):
    cal_obj = AcademicCalendar()
    current_year = cal_obj.get_year()
    current_term = cal_obj.get_term()
    unpaid_invoices_for_this_term = Invoice.objects.filter(year=current_year, term=current_term,
                                                           balance__gt=0).aggregate(total=Sum('balance'))
    if unpaid_invoices_for_this_term['total'] == None:
        return 0
    else:
        return unpaid_invoices_for_this_term['total']


@login_required()
def get_tot_amt_paid_fees_term(request):
    cal_obj = AcademicCalendar()
    current_year = cal_obj.get_year()
    current_term = cal_obj.get_term()
    payments_made = Payment.objects.filter(invoice__year=current_year, invoice__term=current_term).aggregate(
        total=Sum('amount'))
    if payments_made['total'] == None:
        return 0
    else:
        return payments_made['total']


@login_required()
def get_tot_no_transport_subs(request):
    total_trans_sub = Student.objects.filter(transport=True).count()
    return total_trans_sub


@login_required()
def get_tot_no_lunch_subs(request):
    total_lunch_sub = Student.objects.filter(lunch=True).count()
    return total_lunch_sub


@login_required()
def get_arrears_distribution(request):
    pass


@login_required()
def get_no_students_per_grade(request):
    pass


@login_required()
def chart_data(request):
    pass
