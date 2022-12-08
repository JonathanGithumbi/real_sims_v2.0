from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vendor
from .forms import CreateVendorForm, EditVendorForm
from .VendorManager import VendorManager
from django.http import HttpResponse


def view_vendors(request):
    vendors = Vendor.objects.all()
    add_vendor_form = CreateVendorForm()
    return render(request, 'vendor/vendors.html', {'vendors': vendors, 'add_vendor_form': add_vendor_form})


def add_vendor(request):
    add_vendor_form = CreateVendorForm(request.POST)
    vendor_manager = VendorManager()
    vendor_obj = vendor_manager.create_vendor(add_vendor_form)
    messages.success(request, "Successfully Created Vendor :{0}".format(vendor_obj.name),
                     extra_tags="alert-success")
    return redirect('view_vendors')


def get_vendor_editform(request):
    vendor_id = request.GET['vendor_id']
    vendor = Vendor.objects.get(pk=vendor_id)
    vendor_form = EditVendorForm(instance=vendor)
    return HttpResponse(vendor_form.as_p())


def delete_vendor(request, id):
    vendor = Vendor.objects.get(pk=id)
    vendor_manager = VendorManager()
    vendor_manager.delete_vendor(vendor)
    messages.success(request, "Successfully Deleted Vendor:{0}".format(vendor.name),
                     extra_tags="alert-success")
    return redirect('view_vendors')


def edit_vendor(request, id):
    post_data = request.POST
    vendor = Vendor.objects.get(pk=id)
    data = {
        'name': vendor.name
    }
    edit_vendor_form = EditVendorForm(request.POST, initial=data)
    if edit_vendor_form.has_changed():
        vendor_manager = VendorManager()
        vendor_manager.edit_vendor(edit_vendor_form)
        messages.success(request, "Successfully Edited Vendor :{0}".format(vendor.name),
                         extra_tags="alert-success")
        return redirect('view_vendors')
    else:
        messages.success(request, "No Data Changed in :{0}".format(vendor.name),
                         extra_tags="alert-success")
        return redirect('view_vendors')
