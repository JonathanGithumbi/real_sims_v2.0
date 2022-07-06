from pyexpat import model
from django import forms
from .models import AcademicCalendar


class CreateAcademicCalendarForm(forms.ModelForm):
    class Meta:

        model = AcademicCalendar
        fields = ("__all__")
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'term_1_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_1_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_2_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_2_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_3_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_3_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),

        }


class UpdateAcademicCalendarForm(forms.ModelForm):
    class Meta:
        model = AcademicCalendar
        fields = ("__all__")
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'term_1_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_1_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_2_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_2_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_3_start_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),
            'term_3_end_date': forms.SelectDateWidget(attrs={'class': 'form-select'}),

        }
