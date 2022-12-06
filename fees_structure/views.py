from django.shortcuts import redirect, render
from django.urls import reverse
from item.models import Item
from fees_structure.models import FeesStructure, FeesStructureBatch
from .forms import GetFeesStructure, CreateFeesStructureForm, EditFeesStructureForm
from grade.models import Grade
from django.contrib import messages
from user_account.models import User
from academic_calendar.models import Year
from item.forms import CreateSalesItemForm
from fees_structure.FeesStructureManager import FeesStructureManager


def create_fees_structure(request):
    create_feesstructure_form = CreateFeesStructureForm(request.POST)
    feesstructure_manager = FeesStructureManager()
    fees_obj = feesstructure_manager.create_feesstructure(
        create_feesstructure_form)
    messages.success(
        request, "Billing Item: {0} Created Successfully".format(fees_obj.item), extra_tags='alert-success')
    return redirect('view_fees_structure', permanent=True)


def view_fees_structure(request):
    add_billing_item_form = CreateFeesStructureForm()
    fees_structures = FeesStructureBatch.objects.all()
    add_salesitem_form = CreateSalesItemForm()
    return render(request, 'fees_structure/view_fees_structure.html', {'fees_structures': fees_structures, 'add_billing_item_form': add_billing_item_form, 'add_salesitem_form': add_salesitem_form})


def edit_fees_structure(request, id):
    if request.method == 'POST':
        fees_structure = FeesStructureBatch.objects.get(pk=id)
        prev_data = {
            'item': fees_structure.item,
            'grades': fees_structure.grades,
            'amount': fees_structure.amount,
            'ocurrence': fees_structure.ocurrence,
            'period': fees_structure.period,
            'terms': fees_structure.terms,
            'year': fees_structure.year,
            'term': fees_structure.term,
            'charge_on_registration': fees_structure.charge_on_registration,
        }
        form = EditFeesStructureForm(request.POST, initial=prev_data)
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(
                    request, "Changes made successfully", extra_tags='alert-success')
                return redirect(reverse('view_fees_structure'))
            else:
                messages.info(
                    request, "No changes made to the structure", extra_tags='alert-info')
                return redirect(reverse('view_fees_structure'))
        else:
            messages.error(
                request, "Error!", extra_tags='alert-danger')
            return render(request, 'fees_structure/edit_fees_structure.html', {'form': form})

    if request.method == 'GET':
        fees_structure = FeesStructureBatch.objects.get(pk=id)
        form = EditFeesStructureForm(instance=fees_structure)
        return render(request, 'fees_structure/edit_fees_structure.html', {'form': form})


def delete_fees_structure(request, id):
    fees_structure = FeesStructureBatch.objects.get(pk=id)
    feesstructure_manager = FeesStructureManager()
    feesstructure_manager.delete_feesstructure(fees_structure)
    messages.success(
        request, "Billing Item:{} Deleted Successfullly".format(fees_structure.item), extra_tags='alert-success')
    return redirect('view_fees_structure')
