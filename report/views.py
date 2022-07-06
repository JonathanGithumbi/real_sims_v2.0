from django.shortcuts import render

def reports(request):
    return render(request, 'report/reports.html')