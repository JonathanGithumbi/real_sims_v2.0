from .models import Vendor
from django.template.loader import render_to_string
from .forms import VendorModelForm
from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView)
from django.urls import reverse_lazy
from django.views import generic


class VendorListView(generic.ListView):
    model = Vendor
    template_name = 'vendor_list.html'
    context_object_name = 'vendor_list'


class VendorCreateView(BSModalCreateView):
    template_name = 'vendor/create_vendor.html'
    form_class = VendorModelForm
    success_message = 'Success: Vendor was created.'
    success_url = reverse_lazy('vendor_list')


class VendorUpdateView(BSModalUpdateView):
    model = Vendor
    template_name = "vendor/update_vendor.html"
    form_class = VendorModelForm
    success_message = 'Success: Vendor was updated.'
    success_url = reverse_lazy('vendor_list')


class VendorReadView(BSModalReadView):
    model = Vendor
    template_name = "vendor/read_vendor.html"


class VendorDeleteView(BSModalDeleteView):
    model = Vendor
    template_name = "vendor/delete_vendor.html"
    success_message = "Success: Vendor was deleted"
    success_url = reverse_lazy('vendor_list')


def vendors(request):
    data = dict()
    if request.method == 'GET':
        vendor_list = Vendor.objects.all()
        data['table'] = render_to_string(
            '_vendors_table.html',
            {'vendor_list': vendor_list},
            request=request
        )
        return JsonResponse(data)
