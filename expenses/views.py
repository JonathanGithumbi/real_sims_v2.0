from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import CreateExpenseForm, EditExpenseForm
from django.urls import reverse
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response


@login_required()
def expenses(request):
    #!use some kind of limiter to reduce the load on the db server
    expenses = Expense.objects.all().order_by('-created')
    return render(request, 'expenses/expenses.html', {'expenses': expenses})


@login_required()
def add_expense(request):
    # decreases the petty cash balance by the total,that is also the transaction's balance snapshot
    if request.method == 'GET':
        form = CreateExpenseForm()
        return render(request, 'expenses/create_expense.html', {'form': form})
    if request.method == 'POST':
        form = CreateExpenseForm(request.POST)
        if form.is_valid():
            expense_obj = form.save()
            # also save the  expenses to quickbooks
            return redirect(reverse('expenses'))
        else:
            return render(request, 'expenses/create_expense.html', {'form': form})


@login_required()
def confirm_add_expense(request, id):
    expense_obj = Expense.objects.get(pk=id)

    expense_obj.fully_paid = True
    expense_obj.save(update_fields=['fully_paid'])

    #qb_payment = bill_payment_obj.create_qb_bill_payment_obj()
    #bill_payment_obj.qb_id = qb_payment.Id
    #bill_payment_obj.synced = True
    #bill_payment_obj.save(update_fields=['qb_id', 'synced'])

    messages.success(request, "{0} Recorded Successfully".format(
        expense_obj.description), extra_tags='alert-success')
    return redirect('expenses')


@login_required()
def edit_expense(request, id):
    expense_obj = Expense.objects.get(pk=id)

    if request.method == 'GET':
        edit_expense_form = EditExpenseForm(instance=expense_obj)
        return render(request, 'expenses/edit_expense.html', {'form': edit_expense_form, 'expense': expense_obj})
    if request.method == 'POST':
        initial_data = {
            'recipient': expense_obj.recipient,
            'description': expense_obj.description,
            'category': expense_obj.category,
            'quantity': expense_obj.quantity,
            'price_per_quantity': expense_obj.price_per_quantity,
            'total': expense_obj.total,
        }
        edit_expense_form = EditExpenseForm(request.POST, initial=initial_data)
        if edit_expense_form.is_valid():
            edit_expense_form.save(update_fields=None)
            try:
                qb_bill = expense_obj.edit_qb_bill()
            except:
                pass
            if edit_expense_form.has_changed():
                messages.info(request, "{0} Expense Details changed successfully".format(
                    expense_obj.description), extra_tags='alert-success')
                return redirect('expenses')
            else:
                messages.info(request, "No Data Changed on {0} Expense".format(
                    expense_obj.description), extra_tags='alert-info')
                return redirect('expenses')
        else:
            edit_expense_form = EditExpenseForm(request.POST)
            return render(request, 'expenses/edit_expense.html', {'form': edit_expense_form})


@login_required()
def discard_expense(request, id):
    expense_obj = Expense.objects.get(pk=id)

    expense_obj.delete()
    messages.success(request, "{0} Expense Discarded Successfully.".format(
        expense_obj.description))
    return redirect(reverse('expenses'))


@login_required()
def summaries(request):
    return render(request, 'expenses/expense_summary.html')


class ExpenseDistributionChart(APIView):
    """This class view builds the bill distribution pie chart"""
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = [
            'January', 'February', 'March', 'April', 'May', 'June', 'July'
        ]
        chartLabel = "my data"
        chartdata = [0, 10, 5, 2, 20, 30, 45]
        data = {
            "labels": labels,
            'chartLabel': chartLabel,
            "chartdata": chartdata, }
        return Response(data)
