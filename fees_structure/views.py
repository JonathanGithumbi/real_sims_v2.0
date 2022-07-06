from django.shortcuts import render,redirect
from . models import FeesStructure
from django.forms import modelformset_factory
from .forms import FeesStructureForm,UpdateFeesStructureForm
from django.urls import reverse

def fees_structure(request):
    fees_structure = FeesStructure.objects.all()
    return render(request,'fees_structure/fees_structure.html',{'fees_structure':fees_structure})

def update_fees_structure(request,id):
    fees_structure = FeesStructure.objects.get(pk=id)
    if request.method == 'POST':
        form = UpdateFeesStructureForm(request.POST,instance=fees_structure)
        if form.is_valid():
            form.save()
            return redirect(reverse('fees_structure'))
        else:
            return render(request,'fees_structure/update_fees_structure.html',{'form':form,'fees_structure':fees_structure})
    if request.method == 'GET':
        form = UpdateFeesStructureForm(instance=fees_structure)
        return render(request,'fees_structure/update_fees_structure.html',{'form':form,'fees_structure':fees_structure})

    
    



    
