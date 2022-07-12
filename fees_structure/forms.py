from django import forms
from .models import FeesStructure


class FeesStructureForm(forms.ModelForm):
    class Meta:
        
        model = FeesStructure
        fields = '__all__'
        widgets={
            'grade':forms.Select(attrs={'class':'form-select', 'readonly':True}),
            'term': forms.Select(attrs={'readonly':True,'class':'form-select'}),
            'tuition':forms.NumberInput({'class':'form-control', 'id':'tuition','placeholder':'Tuition'}),
            'lunch':forms.NumberInput({'class':'form-control','placeholder':'Lunch'}),
            'transport': forms.NumberInput({'class':'form-control','placeholder':'Transport'}),
            'admission':forms.NumberInput({'class':'form-control','placeholder':'Admission'}),
            'diary_and_report_book':forms.NumberInput({'class':'form-control','placeholder':'Diary and Report Book'}),
            'interview':forms.NumberInput({'class':'form-control','placeholder':'Interview'}),
            'computer':forms.NumberInput({'class':'form-control','placeholder':'Computer '}),
        }

class UpdateFeesStructureForm(forms.ModelForm):
    class Meta:
        
        model = FeesStructure
        fields = '__all__'
        widgets={
            'grade':forms.Select(attrs={'class':'form-select',}),
            'term': forms.Select(attrs={'readonly':True,'class':'form-select'}),
            'year':forms.Select(attrs={'readonly':True,'class':'form-select'}),
            'tuition':forms.NumberInput({'class':'form-control', 'id':'tuition','placeholder':'Tuition'}),
            'lunch':forms.NumberInput({'class':'form-control','placeholder':'Lunch'}),
            'transport': forms.NumberInput({'class':'form-control','placeholder':'Transport'}),
            'admission':forms.NumberInput({'class':'form-control','placeholder':'Admission'}),
            'diary_and_report_book':forms.NumberInput({'class':'form-control','placeholder':'Diary and Report Book'}),
            'interview':forms.NumberInput({'class':'form-control','placeholder':'Interview'}),
            'computer':forms.NumberInput({'class':'form-control','placeholder':'Computer '}),
        }

