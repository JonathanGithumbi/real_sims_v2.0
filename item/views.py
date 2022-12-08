from django.shortcuts import render
from .forms import CreateSalesItemForm, EditSalesItemForm
from .ItemManager import ItemManager
from django.contrib import messages
from django.shortcuts import redirect
from .models import Item
from django.http import HttpResponse


def create_salesitem(request):
    add_salesitem_form = CreateSalesItemForm(request.POST)
    item_manager = ItemManager()
    item_obj = item_manager.create_salesitem(add_salesitem_form)
    messages.success(request, "Successfully Created Sales Item :{0}".format(item_obj.name),
                     extra_tags="alert-success")
    return redirect('view_sales_items')


def view_sales_item(request):
    items = Item.objects.all()
    add_salesitem_form = CreateSalesItemForm()
    return render(request, 'item/view_sales_items.html', {'items': items, 'add_salesitem_form': add_salesitem_form})


def edit_salesitem(request, id):
    pass


def get_salesitem_editform(request):
    """Gets a sales item form populated with insytance data for the edit modal"""
    item_id = request.GET['item_id']

    item = Item.objects.get(pk=item_id)
    item_form = EditSalesItemForm(instance=item)
    return HttpResponse(item_form.as_p())


def delete_salesitem(request, id):
    item = Item.objects.get(pk=id)
    item_manager = ItemManager()
    item_manager.delete_salesitem(item)
    messages.success(request, "Successfully Deleted Sales Item :{0}".format(item.name),
                     extra_tags="alert-success")
    return redirect('view_sales_items')
