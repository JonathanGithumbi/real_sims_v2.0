from django.shortcuts import redirect, render

from user_account.models import User
from .models import Bill, BillItem, PettyCash
from .forms import CreateBillItemForm
from django.urls import reverse
from bill_payment.models import BillPayment
from .forms import EditBillItemForm, TopUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .BillManager import BillManager
from .PettyCashManager import PettyCashManager
from django.http import HttpResponse


@login_required()
# @permission_required("can_view_bill")
def bills(request):
    #!use some kind of limiter to reduce the load on the db server
    create_bill_form = CreateBillItemForm()
    edit_bill_form = EditBillItemForm()
    topup_form = TopUpForm()
    bills = BillItem.objects.all().order_by('-created')
    petty_cash = PettyCash.objects.get(pk=1)
    petty_cash_balance = petty_cash.balance
    return render(request, 'bill/bills.html', {'bills': bills, 'petty_cash_balance': petty_cash_balance, 'edit_bill_form': edit_bill_form, 'create_bill_form': create_bill_form, 'topup_form': topup_form})


login_required()
# @permission_required("can_create_bill")


def create_bill(request):
    form = CreateBillItemForm(request.POST)
    bill_manager = BillManager()
    bill_item_obj = bill_manager.create_bill(form)
    messages.success(request, "{0} Bill recorded successfully".format(
        bill_item_obj.description), extra_tags='alert-success')
    return redirect('bills')


@login_required()
def topup(request):
    topup_form = TopUpForm(request.POST)
    bill_manager = BillManager()
    bill_manager.create_deposit_bill(topup_form)
    messages.success(request, "Top Up Successfull",
                     extra_tags='alert-success')
    return redirect(reverse('bills'))


@login_required()
def delete_bill(request, id):
    bill_obj = BillItem.objects.get(pk=id)
    bill_manager = BillManager()
    bill_manager.delete_bill(bill_obj)
    messages.success(request, "Bill Deleted Successfully")
    return redirect(reverse('bills'))


login_required()
# @permission_required("can_edit_bill")


def edit_bill(request, id):
    bill_obj = BillItem.objects.get(pk=id)

    if request.method == 'GET':
        bill_edit_form = EditBillItemForm(instance=bill_obj)
        return HttpResponse(bill_edit_form.as_p())
    if request.method == 'POST':
        initial_data = {
            'recipient': bill_obj.recipient,
            'description': bill_obj.description,
            'category': bill_obj.category,
            'quantity': bill_obj.quantity,
            'price_per_quantity': bill_obj.price_per_quantity,
            'total': bill_obj.total,
            'balance': bill_obj.balance
        }
        bill_edit_form = EditBillItemForm(request.POST, initial=initial_data)
        if bill_edit_form.is_valid():
            if bill_edit_form.has_changed():
                bill_obj.recipient = bill_edit_form.cleaned_data['recipient']
                bill_obj.description = bill_edit_form.cleaned_data['description']
                bill_obj.category = bill_edit_form.cleaned_data['category']
                if 'amount' in bill_edit_form.changed_data or 'price_per_quantity' in bill_edit_form.changed_data or 'total' in bill_edit_form.changed_data:
                    petty_cash = PettyCash.objects.get(pk=1)
                    petty_cash.balance = (petty_cash.balance +
                                          initial_data['total']) - bill_edit_form.cleaned_data['total']
                    petty_cash.save(update_fields=['balance', 'modified'])
                    bill_obj.balance = (initial_data['balance'] +
                                        initial_data['total']) - bill_edit_form.cleaned_data['total']
                    bill_obj.quantity = bill_edit_form.cleaned_data['quantity']
                    bill_obj.price_per_quantity = bill_edit_form.cleaned_data['price_per_quantity']
                    bill_obj.total = bill_edit_form.cleaned_data['total']

                bill_obj.save(update_fields=None)
                try:
                    qb_bill = bill_obj.edit_qb_bill()
                except:
                    pass
                messages.info(request, "{0} Bill Details changed successfully".format(
                    bill_obj.description), extra_tags='alert-success')
                return redirect('bills')
            else:
                messages.info(request, "No Data Changed on {0} Bill".format(
                    bill_obj.description), extra_tags='alert-info')
                return redirect('bills')
        else:
            bill_edit_form = EditBillItemForm(request.POST)
            return render(request, 'bill/edit_bill.html', {'form': bill_edit_form})


@login_required()
def view_summaries(request):
    return render(request, 'bill/bill_summaries.html')


# One class view per chart
def chart_data(request):
    pass
