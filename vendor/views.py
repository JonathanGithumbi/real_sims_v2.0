from django import forms
from django.shortcuts import redirect, render
from .models import Vendor
from django.forms import modelformset_factory
from .forms import CreateVendorForm
from django.urls import reverse



def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html',{'vendors':vendors})


def create_vendor(request):
    form = CreateVendorForm()
    if request.method == 'GET':
        return render(request, 'vendor/create_vendor.html',{'form':form})
    if request.method == 'POST':
        form=CreateVendorForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect(reverse('vendors'))
        else:
            return render(request, 'vendor/create_vendor.html',{'form':form})

def delete_vendor(request ,id):
    vendor = Vendor.objects.get(pk=id)
    vendor.delete()
    return redirect('vendors')



