from django.shortcuts import render
from .forms import CreateSalesItemForm
from .ItemManager import ItemManager
from django.contrib import messages
from django.shortcuts import redirect
from .models import Item


def create_salesitem(request):
    add_salesitem_form = CreateSalesItemForm(request.POST)
    item_manager = ItemManager()
    item_obj = item_manager.create_salesitem(add_salesitem_form)
    messages.success(request, "Successfully Created Sales Item :{0}".format(item_obj.name),
                     extra_tags="alert-success")
    return redirect('view_fees_structure')


def view_sales_item(request):
    items = Item.objects.all()
    add_salesitem_form = CreateSalesItemForm()
    return render(request, 'item/view_sales_items.html', {'items': items, 'add_sales_tems_form': add_salesitem_form})


def edit_salesitem(request, id):
    pass


def delete_salesitem(request, id):
    pass
