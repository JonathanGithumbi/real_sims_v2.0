from django.shortcuts import redirect, render

from user_account.models import User
from .models import Bill, BillItem, PettyCash
from .forms import CreateBillItemForm
from django.urls import reverse
from bill_payment.models import BillPayment
from .forms import EditBillItemForm, TopUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.views import APIView
from rest_framework.response import Response

login_required()
# @permission_required("can_view_bill")


def bills(request):
    #!use some kind of limiter to reduce the load on the db server
    bills = BillItem.objects.all().order_by('-created')
    petty_cash = PettyCash.objects.get(pk=1)
    petty_cash_balance = petty_cash.balance
    return render(request, 'bill/bills.html', {'bills': bills, 'petty_cash_balance': petty_cash_balance})


login_required()
# @permission_required("can_create_bill")


def create_bill(request):
    # decreases the petty cash balance by the total,that is also the transaction's balance snapshot
    if request.method == 'GET':
        form = CreateBillItemForm()
        return render(request, 'bill/create_bill.html', {'form': form})
    if request.method == 'POST':
        form = CreateBillItemForm(request.POST)
        if form.is_valid():
            bill_item_obj = form.save()
            petty_cash_obj = PettyCash.objects.get(pk=1)

            bill_item_obj.balance = petty_cash_obj.balance - bill_item_obj.total
            user_id = request.user.id
            user = User.objects.get(pk=user_id)
            bill_item_obj.user = user
            bill_item_obj.save(update_fields=['balance', 'user'])

            petty_cash_obj.balance = petty_cash_obj.balance - bill_item_obj.total
            petty_cash_obj.save(update_fields=['balance', 'modified'])
            # also save the  bill to quickbooks
            try:
                qb_bill_item = bill_item_obj.create_qb_bill()
            except:
                pass
            else:
                bill_item_obj.qb_id = qb_bill_item.Id
                bill_item_obj.synced = True
                bill_item_obj.save(update_fields=['qb_id', 'synced'])
            messages.success(request, "{0} Bill recorded successfully".format(
                bill_item_obj.description), extra_tags='alert-success')
            return redirect(reverse('bills'))
        else:
            return render(request, 'bill/create_bill.html', {'form': form})


login_required()
# @permission_required("can_pay_bill")


def pay_bill(request, id):
    bill_obj = BillItem.objects.get(pk=id)

    # create a bill payment object.
    # bill pay
    bill_payment_obj = BillPayment.objects.create(

        amount=bill_obj.total,
        bill=bill_obj,
    )
    bill_payment_obj.save()
    bill_obj.fully_paid = True
    bill_obj.save(update_fields=['fully_paid'])

    #qb_payment = bill_payment_obj.create_qb_bill_payment_obj()
    #bill_payment_obj.qb_id = qb_payment.Id
    #bill_payment_obj.synced = True
    #bill_payment_obj.save(update_fields=['qb_id', 'synced'])

    messages.success(request, "{0} Bill Payment recorded Successfully".format(
        bill_obj.description), extra_tags='alert-success')
    return redirect('bills')


login_required()
# @permission_required("can_edit_bill")


def edit_bill(request, id):
    bill_obj = BillItem.objects.get(pk=id)

    if request.method == 'GET':
        bill_edit_form = EditBillItemForm(instance=bill_obj)
        return render(request, 'bill/edit_bill.html', {'form': bill_edit_form, 'bill': bill_obj})
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
def delete_bill(request, id):
    bill_obj = BillItem.objects.get(pk=id)
    petty_cash = PettyCash.objects.get(pk=1)
    if bill_obj.category == "Deposit":
        petty_cash.balance = petty_cash.balance - bill_obj.total
        petty_cash.save(update_fields=['balance', 'modified'])
        bill_obj.delete()
        messages.success(request, "Top Up Discarded Successfully")
        return redirect(reverse('bills'))
        # return the total amount back to the petty_cash

    petty_cash.balance = petty_cash.balance + bill_obj.total
    petty_cash.save(update_fields=['balance', 'modified'])
    bill_obj.delete()
    messages.success(request, "Bill Discarded Successfully")
    return redirect(reverse('bills'))


@login_required()
def view_summaries(request):
    return render(request, 'bill/bill_summaries.html')


@login_required()
def topup(request):
    if request.method == 'GET':
        topupform = TopUpForm()
        return render(request, 'bill/topup.html', {'form': topupform})

    if request.method == "POST":
        topup_form = TopUpForm(request.POST)
        if topup_form.is_valid():
            amount = topup_form.cleaned_data['amount']
            petty_cash_object = PettyCash.objects.get(pk=1)
            user_id = request.user.id
            user = User.objects.get(pk=user_id)

            # topup algorithm
            # topup means increasing the petty cash balance and creating a billitem and also reflecting it to qb
            depo_transaction = BillItem.objects.create(
                category="Deposit",
                description="Petty Cash Top Up",
                total=int(amount),
                quantity=1,
                price_per_quantity=int(amount),
                balance=petty_cash_object.balance + int(amount),
                recipient=user.username,

            )
            petty_cash_object.balance = int(
                petty_cash_object.balance) + int(amount)
            petty_cash_object.save(update_fields=['balance', 'modified'])

            #
            # record to qb
            #

            messages.info(request, "Petty Cash Top Up Successfull",
                          extra_tags='alert-success')
            return redirect(reverse('bills'))
        else:
            return render(request, 'bill/topup.html', {'form': topup_form
                                                       })


# One class view per chart
class BillDistributionChart(APIView):
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
