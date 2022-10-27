from django.shortcuts import redirect, render
from django.urls import reverse
from user_account.views import refresh
from user_account.models import Token
from django.core.exceptions import ObjectDoesNotExist
from intuitlib.client import AuthClient
from django.conf import settings
from student.models import Student
from bill.models import BillItem
from django.db.models import Sum
from invoice.models import Invoice
from academic_calendar.models import AcademicCalendar
from payment.models import Payment
from django.contrib.auth.decorators import login_required



@login_required()
def dashboard(request):
    total_no_students = get_tot_no_students(request)
    total_amount_in_unpaid_bills = get_tot_amt_unpaid_bills(request)
    total_amount_in_unpaid_fees_arrears_term = get_tot_amt_unpaid_fees_term(request)
    total_amount_in_paid_fees_arrears_term = get_tot_amt_paid_fees_term(request)
    total_no_transport_subscribers = get_tot_no_transport_subs(request)
    total_no_lunch_subscribers = get_tot_no_lunch_subs(request)
    students_in_each_grade = 0
    fees_arrears_distributed_across_each_class = 0
    return render(request, 'dashboard/dashboard.html', {
        'total_no_students': total_no_students,
        'total_amount_in_unpaid_bills': total_amount_in_unpaid_bills,
        'total_amount_in_unpaid_fees_arrears_term': total_amount_in_unpaid_fees_arrears_term,
        'total_amount_in_paid_fees_arrears_term': total_amount_in_paid_fees_arrears_term,
        'total_no_transport_subscribers': total_no_transport_subscribers,
        'total_no_lunch_subscribers': total_no_lunch_subscribers,
        'students_in_each_grade': students_in_each_grade,
        'fees_arrears_distributed_across_each_class': fees_arrears_distributed_across_each_class,
    })


@login_required()
def get_tot_no_students(request):
    """Gets the total number of registered students"""
    tot_no_stu = Student.objects.filter(active=True).count()
    return tot_no_stu


@login_required()
def get_tot_amt_unpaid_bills(reqeust):
    unpaid_bills = BillItem.objects.filter(fully_paid=False).aggregate(total=Sum('total'))
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