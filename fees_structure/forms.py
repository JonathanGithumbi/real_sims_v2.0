from datetime import date
from django.forms import modelformset_factory
from .models import FeesStructureBatch
from grade.models import Grade
from django import forms
from grade.models import Grade
from academic_calendar.models import AcademicCalendar


class GetFeesStructure(forms.Form):
    TERMS = (
        (1, 1),
        (2, 2),
        (3, 3)
    )
    grade = forms.ModelChoiceField(queryset=Grade.objects.all(
    ), widget=forms.Select(attrs={'class': 'form-control'}))
    term = forms.ChoiceField(choices=TERMS, widget=forms.Select(
        attrs={'class': 'form-control'}))


def get_grades():
    grades = Grade.objects.all()
    grade_iterable = []

    for grade in grades:
        tup = (str(grade), str(grade))
        grade_iterable.append(tup)

    return grade_iterable


def get_terms():
    cal = AcademicCalendar()
    this_term = cal.get_term()
    terms_iterable = []
    terms_iterable.append(("", ""))
    while this_term < 4:
        terms_iterable.append((str(this_term), str(this_term)))
        this_term = this_term+1

    return terms_iterable


def get_years():
    years_iterable = []
    today = date.today()
    years_iterable.append(("", ""))
    i = 0
    while i < 6:
        new_year = today.year + i
        years_iterable.append((str(new_year), str(new_year)))
        i = i + 1

    return years_iterable


class CreateFeesStructureForm(forms.ModelForm):

    class Meta:
        model = FeesStructureBatch
        fields = ('item', 'grades', 'amount', 'ocurrence', 'period',
                'terms', 'year', 'term', 'charge_on_registration')

        widgets = {
            'item': forms.Select(
                attrs={'class': 'form-control form-control-sm', 'id': 'description'}),
            'grades': forms.CheckboxSelectMultiple(
                attrs={'name': 'grades', 'id': 'grades'}),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control form-control-sm', 'id': 'amount'}),
            'ocurrence': forms.RadioSelect(
                attrs={'name': 'ocurrence'}),
            'period': forms.RadioSelect(attrs={'name': 'period', 'id': 'period'}),
            'terms': forms.CheckboxSelectMultiple(
                attrs={'class': '', 'id': 'specific_terms'}),
            'year': forms.Select(
                attrs={'class': 'form-control form-control-sm', 'id': 'year'}),
            'term': forms.Select(
                attrs={'class': 'form-control form-control-sm', 'id': 'term'}),
            'charge_on_registration': forms.CheckboxInput(
                attrs={'name': 'cor', 'id': 'cor'})

        }
