from django.shortcuts import render
from .utils import render_to_pdf


def reports(request):
    return render(request, 'report/reports.html')

def generate_fees_arrears_report(request):
    students = Student.objects.filter(hot_lunch=True)
    context = {'students':students}
    template_name = 'administrator/lunch_report.html'
    pdf = render_to_pdf(template_name,context)
    return HttpResponse(pdf, content_type='application/pdf')

def generate_lunch_subscribers_report(report):
    pass

def generate_transport_subscribers_report(request):
    pass



