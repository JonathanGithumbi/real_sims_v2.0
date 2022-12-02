from django.shortcuts import redirect, render
from django.urls import reverse
from item.models import Item
from fees_structure.models import FeesStructure, FeesStructureBatch
from .forms import GetFeesStructure, CreateFeesStructureForm, EditFeesStructureForm
from grade.models import Grade
from django.contrib import messages
from user_account.models import User
from academic_calendar.models import Year


def create_fees_structure(request):
    """This method creates a separate fees structure for each grade."""
    if request.method == 'GET':
        form = CreateFeesStructureForm()
        return render(request, 'fees_structure/create_fees_structure.html', {'form': form})
    if request.method == 'POST':

        form = CreateFeesStructureForm(request.POST)
        if form.is_valid():
            fees_structure_batch = form.save()

            fees_structure_batch.created_by = request.user
            fees_structure_batch.last_modified_by = request.user
            fees_structure_batch.save(
                update_fields=['last_modified_by', 'last_modified', 'created_by'])
            messages.success(
                request, "Billing Items Created Successfully", extra_tags='alert-success')
            return redirect('view_fees_structure', permanent=True)
        else:
            messages.error(
                request, "Error!", extra_tags='alert-danger')
            return render(request, 'fees_structure/create_fees_structure.html', {'form': form})


def view_fees_structure(request):
    fees_structures = FeesStructureBatch.objects.all()
    return render(request, 'fees_structure/view_fees_structure.html', {'fees_structures': fees_structures})


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
    fees_structure = fees_structure.delete()
    messages.info(
        request, "Fees Structure Deleted Successfullly", extra_tags='alert-success')
    return redirect('view_fees_structure')
