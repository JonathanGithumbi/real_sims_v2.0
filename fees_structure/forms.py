from datetime import date
from django.forms import modelformset_factory
from .models import FeesStructure
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


class CreateFeesStructureForm(forms.Form):

    recurring_choices = [
        ('recurring', 'recurring'),
        ('one-time', 'one-time')
    ]
    period_choices = [
        ('year-round', 'year-round'),
        ('speecific-term', 'specific-term')
    ]
    term_choices = [
        (1, 'Term 1'),
        (2, 'Term 2'),
        (3, 'Term 3')
    ]

    description = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'description'}))

    amount = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control form-control-sm', 'id': 'amount'}))
    occurence = forms.ChoiceField(required=False, label='Fee Occurence', choices=recurring_choices, widget=forms.RadioSelect(
        attrs={'name': 'occurence'}))
    period = forms.ChoiceField(required=False, label="Period", choices=period_choices,
                               widget=forms.RadioSelect(attrs={'name': 'period', 'id': 'period'}))
    specific_terms = forms.MultipleChoiceField(required=False, choices=term_choices, widget=forms.CheckboxSelectMultiple(
        attrs={'class': '', 'id': 'specific_terms'}))
    year = forms.ChoiceField(initial="", required=False, choices=get_years, widget=forms.Select(
        attrs={'class': 'form-control form-control-sm', 'id': 'year'}))
    term = forms.ChoiceField(initial="", required=False, choices=get_terms, widget=forms.Select(
        attrs={'class': 'form-control form-control-sm', 'id': 'term'}))
    grades = forms.MultipleChoiceField(label='Apply Fee To Grades', choices=get_grades, widget=forms.CheckboxSelectMultiple(
        attrs={'class': '', 'id': 'grades'}))
