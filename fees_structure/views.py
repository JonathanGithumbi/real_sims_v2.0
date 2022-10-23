from django.shortcuts import redirect, render
from django.urls import reverse

from fees_structure.models import FeesStructure
from .forms import FeesStructureFormSet


def fees_structure(request):

    fees_structure_objects = FeesStructure.objects.all()
    return render(request, 'fees_structure/fees_structure.html', {'fees_structure_objects': fees_structure_objects})


def edit_fees_structure(request):
    if request.method == 'GET':
        fees_structure_objects = FeesStructure.objects.all()
        formset = FeesStructureFormSet(initial=fees_structure_objects)
        return render(request, 'fees_structure/edit_fees_structure.html', {'formset': formset})
    if request.method == 'POST':
        formset = FeesStructureFormSet(request.POST)
        if formset.is_valid():
            # instances is all the instance sthat have bee changed and saved
            instances = formset.save()
            return redirect(reverse('fees_structure'))
        else:
            return render(request, 'fees_structure/edit_fees_structure.html', {'formset': formset})
