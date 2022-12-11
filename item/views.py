from .models import Item
from django.template.loader import render_to_string
from .forms import ItemModelForm

from django.http import JsonResponse
from bootstrap_modal_forms.generic import (
    BSModalCreateView,
    BSModalUpdateView,
    BSModalReadView,
    BSModalDeleteView
)
from django.urls import reverse_lazy
from django.views import generic

class ItemListView(generic.ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'item_list'

class ItemCreateView(BSModalCreateView):
    template_name = 'item/create_item.html'
    form_class = ItemModelForm
    success_message = 'Success: Item was created'
    success_url = reverse_lazy('item_list')

class ItemUpdateView(BSModalUpdateView):
    model = Item
    template_name = 'item/update_item.html'
    form_class = ItemModelForm
    success_message = 'Success: Item was updated'
    success_url = reverse_lazy('item_list')


class ItemReadView(BSModalReadView):
    model = Item
    template_name = 'item/read_item.html'

class ItemDeleteView(BSModalDeleteView):
    model = Item
    template_name = 'item/delete_item.html'
    success_message = 'Success: Item was created'
    success_url = reverse_lazy('item_list')


def items(request):
    data = dict()
    if request.method == 'GET':
        item_list = Item.objects.all()
        data['table'] = render_to_string(
            '_items_table.html',
            {'item_list': item_list},
            request=request
        )
        return JsonResponse(data)
