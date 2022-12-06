from django.forms import modelformset_factory
from django.shortcuts import render
from .models import Year, Term
from .forms import YearForm, TermForm
from django.contrib import messages
from django.shortcuts import redirect
from .CalendarManager import CalendarManager


def create_term(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            term_instace = form.save()
            messages.success(request, "Term added successfully.",
                             extra_tags='alert-success')
            return redirect('view_ac_cal')
        else:
            messages.error(request, "Error creating term",
                           extra_tags='alert-error')
            return render(request, 'academic_calendar/create_term.html', {'form': form})
    else:
        form = TermForm()
        return render(request, 'academic_calendar/create_term.html', {'form': form})


def create_year(request):
    if request.method == 'POST':
        form = YearForm(request.POST)
        if form.is_valid():
            term_instance = form.save()
            messages.success(request, "Year added successfully.",
                             extra_tags='alert-success')
            return redirect('view_year', term_instance.id)
        else:
            messages.error(request, "Error creating year",
                           extra_tags='alert-error')
            return render(request, 'academic_calendar/create_year.html', {'form': form})
    else:
        form = YearForm()
        return render(request, 'academic_calendar/create_year.html', {'form': form})


def view_ac_cal(request):
    all_years = Year.objects.all()
    return render(request, 'academic_calendar/view_ac_cal.html', {'years': all_years})


def edit_ac_cal(request):
    pass


def delete_year(request, id):
    year = Year.objects.get(pk=id)
    calendar_manager = CalendarManager()
    calendar_manager.delete_year(year)
    messages.success(request, "Successfuy deleted the year {0}".format(
        year.year), extra_tags="alert-success")
    return redirect('academic_calendars')


def create_year(request):
    create_year_form = YearForm(request.POST)
    calendar_manager = CalendarManager()
    year = calendar_manager.create_year(create_year_form)
    messages.success(
        request, "Successfully created academic calendar for : {0}".format(year.year), extra_tags="alert-success")
    return redirect('academic_calendars')


def academic_calendars(request):
    years = Year.objects.all()
    create_year_form = YearForm()
    return render(request, 'academic_calendar/academic_calendars.html',
                  {'years': years, 'create_year_form': create_year_form, 'edit_year_form': YearForm})


def academic_calendar(request, id):
    year = Year.objects.get(pk=id)
    create_term_form = TermForm()
    create_term_form.year = year
    return render(request, 'academic_calendar/academic_calendar.html', {'year': year, 'create_term_form': create_term_form})


def create_term(request, year_id):
    create_term_form = TermForm(request.POST)
    year = Year.objects.get(pk=year_id)
    calendar_manager = CalendarManager()
    term_obj = calendar_manager.create_term(year, create_term_form)
    messages.success(
        request, "Term created successfully", extra_tags="alert-success")
    return redirect('academic_calendar', year_id)


def edit_term(request, id):
    pass


def delete_term(request, id):
    term = Term.objects.get(pk=id)
    calendar_manager = CalendarManager()
    calendar_manager.delete_term(term)
    messages.success(
        request, "Term deleted successfully", extra_tags="alert-success")
    return redirect('academic_calendar', term.year.id)


def edit_year(request, id):
    year = Year.objects.get(pk=id)
    year_form = YearForm(instance)
    pass
