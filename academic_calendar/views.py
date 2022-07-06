from django.urls import reverse
from django.shortcuts import redirect, render
from datetime import date
from academic_calendar.models import AcademicCalendar
from .forms import UpdateAcademicCalendarForm,CreateAcademicCalendarForm

def academic_calendar(request):
    academic_calendars = AcademicCalendar.objects.all()
    return render(request,'academic_calendar/academic_calendar.html',{'academic_calendars':academic_calendars})


def create_academic_calendar(request):
    if request.method == 'POST':
        form = CreateAcademicCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('academic_calendar'))
        else:
            return render(request,'academic_calendar/create_academic_calendar.html',{'form':form})
    if request.method == 'GET':
        form = CreateAcademicCalendarForm()
        return render(request,'academic_calendar/create_academic_calendar.html',{'form':form})
    
def update_academic_calendar(request, id):
    academic_calendar = AcademicCalendar.objects.get(pk=id)
    if request.method =='POST':
        form = UpdateAcademicCalendarForm(request.POST,instance=academic_calendar)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('academic_calendar'))
    if request.method =='GET':
        form = UpdateAcademicCalendarForm(instance=academic_calendar)
        return render(request, 'academic_calendar/edit_academic_calendar.html',{'form':form,'academic_calendar':academic_calendar})


def delete_academic_calendar(request,id):
    obj = AcademicCalendar.objects.get(pk=id)
    obj.delete()
    return redirect(reverse('academic_calendar'))

