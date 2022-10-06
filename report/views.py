from django.shortcuts import render
from .utils import render_to_pdf
from student.models import Student
from django.http import HttpResponse
from invoice.models import BalanceTable, Invoice
from django.contrib.auth.decorators import login_required

@login_required()
def fees_arrears_report(request):
    students = BalanceTable.objects.filter(balance__lt=0).order_by('balance')
    return render(request, 'report/fees_arrears_report.html', {'students': students})

@login_required()
def lunch_subscribers_report(request):
    students = Student.objects.filter(lunch=True)
    return render(request, 'report/lunch_subscribers.html', {'students': students})

@login_required()
def transport_subscribers_report(request):
    students = Student.objects.filter(transport=True)
    return render(request, 'report/transport_subscribers.html', {'students': students})


@login_required()
def generate_fees_arrears_report(request):
    students = BalanceTable.objects.filter(balance__lt=0).order_by('balance')
    context = {'students': students}
    template_name = 'report/fees_arrears_report.html'
    pdf = render_to_pdf(template_name, context)
    return HttpResponse(pdf, content_type='application/pdf')

@login_required()
def generate_lunch_subscribers_report(request):
    students = Student.objects.filter(lunch=True)
    context = {'students': students}
    template_name = 'report/lunch_subscribers.html'
    pdf = render_to_pdf(template_name, context)
    return HttpResponse(pdf, content_type='application/pdf')


@login_required()
def generate_transport_subscribers_report(request):
    students = Student.objects.filter(transport=True)
    context = {'students': students}
    template_name = 'report/transport_subscribers.html'
    pdf = render_to_pdf(template_name, context)
    return HttpResponse(pdf, content_type='application/pdf')
