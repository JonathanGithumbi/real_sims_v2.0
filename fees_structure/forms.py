from django.forms import modelformset_factory
from .models import FeesStructure

FeesStructureFormSet = modelformset_factory(FeesStructure, fields=('__all__'))
