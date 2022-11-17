from django.shortcuts import redirect, render
from django.urls import reverse

from fees_structure.models import FeesStructure
from .forms import  GetFeesStructure, CreateFeesStructureForm


def fees_structure(request):
    if request.method == "GET":
        form = GetFeesStructure()
        return render(request, "fees_structure/fees_structure.html", {'form': form})
    if request.method == "POST":
        pass

def create_fees_structure(request):
    if request.method == 'GET':
        form = CreateFeesStructureForm()
        return render(request, 'fees_structure/create_fees_structure.html',{'form':form})


