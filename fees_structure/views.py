from .models import BillingItem
from django.template.loader import render_to_string
from .forms import BillingItemModelForm

from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views import generic


class BillingItemListView(generic.ListView):
    model = BillingItem
    template_name = 'billingitem_list.html'
    context_object_name = 'billingitem_list'


class BillingItemCreateView(BSModalCreateView):
    template_name = 'fees_structure/create_billingitem.html'
    form_class = BillingItemModelForm
    success_message = 'Success: Billing Item was created'
    success_url = reverse_lazy('billingitem_list')


class BillingItemUpdateView(BSModalUpdateView):
    model = BillingItem
    template_name = 'fees_structure/update_billingitem.html'
    form_class = BillingItemModelForm
    success_message = 'Success: Billing Item was updated'
    success_url = reverse_lazy('billingitem_list')


class BillingItemReadView(BSModalReadView):
    model = BillingItem
    template_name = 'fees_structure/read_billingitem.html'


class BillingItemDeleteView(BSModalDeleteView):
    model = BillingItem
    template_name = 'fees_structure/delete_billingitem.html'
    success_message = 'Success: Billing Item was created'
    success_url = reverse_lazy('billingitem_list')


def billingitems(request):
    data = dict()
    if request.method == 'GET':
        billingitem_list = BillingItem.objects.all()
        data['table'] = render_to_string(
            '_billingitems_table.html',
            {'billingitem_list': billingitem_list},
            request=request
        )
        return JsonResponse(data)
