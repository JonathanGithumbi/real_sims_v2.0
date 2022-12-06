from .models import Year, Term
from django import forms


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ('year', 'start', 'end')
        widgets = {
            'year': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'year'}),
            'start': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'start', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'end', 'type': 'date'}),
        }


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ('term', 'start', 'end')
        widgets = {
            'term': forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'year'}),
            'start': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'start', 'type': 'date'}),
            'end': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id': 'end', 'type': 'date'}),

        }
