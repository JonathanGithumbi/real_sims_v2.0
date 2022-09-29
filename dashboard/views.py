from django.shortcuts import redirect, render
from django.urls import reverse
from user_account.views import refresh
from user_account.models import Token
from django.core.exceptions import ObjectDoesNotExist
from intuitlib.client import AuthClient
from django.conf import settings
from student.models import Student


def dashboard(request):
    total_no_students = Student.objects.count()
    total_amount_in_unpaid_bills = 0
    total_amount_in_unpaid_fees_arrears =0
    total_no_transport_subscribers = 0
    total_no_lunch_subscribers = 0
    students_in_each_grade = 0
    fees_arrears_distributed_across_each_class = 0
    return render(request, 'dashboard/dashboard.html', {
                  'total_no_students': total_no_students,
                  'total_amount_in_unpaid_bills':total_amount_in_unpaid_bills,
                  'total_amount_in_unpaid_fees_arrears':total_amount_in_unpaid_fees_arrears,
                  'total_no_transport_subscribers':total_no_transport_subscribers,
                  'total_no_lunch_subscribers':total_no_lunch_subscribers,
                  'students_in_each_grade':students_in_each_grade,
                  'fees_arrears_distributed_across_each_class':fees_arrears_distributed_across_each_class,
    })
