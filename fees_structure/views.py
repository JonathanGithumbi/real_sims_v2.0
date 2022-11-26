from django.shortcuts import redirect, render
from django.urls import reverse
from item.models import Item
from fees_structure.models import FeesStructure, FeesStructureBatch
from .forms import GetFeesStructure, CreateFeesStructureForm
from grade.models import Grade
from django.contrib import messages
from user_account.models import User


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
            return redirect('view_fees_structure')
        else:
            messages.error(
                request, "Error!", extra_tags='alert-danger')
            return render(request, 'fees_structure/create_fees_structure.html', {'form': form})


def view_fees_structure(request):
    fees_structures = FeesStructureBatch.objects.all()
    return render(request, 'fees_structure/view_fees_structure.html', {'fees_structures': fees_structures})


def delete_fees_structure(request):
    pass
