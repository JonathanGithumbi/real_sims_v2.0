from django.forms import modelformset_factory
from django.shortcuts import render
from .models import Year, Term
from .forms import YearForm, TermForm
from django.contrib import messages
from django.shortcuts import redirect


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
    pass


def create_year(request):
    if request.method == 'POST':
        create_year_form = YearForm(request.POST)
        if create_year_form.is_valid():
            create_year_form.save()
            return redirect('academic_calendars')
        else:
            messages.error(
                request, "error creating academic calendar", extra_tags="alert-danger")
            return render(request, 'academic_calendar.html', {'create_year_form': create_year_form})
    else:
        pass


def academic_calendars(request):
    years = Year.objects.all()
    create_year_form = YearForm()
    return render(request, 'academic_calendar/academic_calendars.html', {'years': years, 'create_year_form': create_year_form})


def academic_calendar(request, id):
    year = Year.objects.get(pk=id)
    create_term_form = TermForm()
    return render(request, 'academic_calendar/academic_calendar.html', {'year': year, 'create_term_form': create_term_form})


def create_term(request):
    if request.method == 'POST':
        create_term_form = TermForm(request.POST)
        if create_term_form.is_valid():
            term_obj = create_term_form.save()
            return redirect('academic_calendar', term_obj.id)
        else:
            pass


def edit_term(request, id):
    pass


def delete_term(request, id):
    term = Term.objects.get(pk=id)
    year = Year.objects.get(pk=term.id)
    term.delete()
    messages.success(
        request, "Term deleted successfully", extra_tags="alert-success")
    return redirect('academic_calendar', year)
