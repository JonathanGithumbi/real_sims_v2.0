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

