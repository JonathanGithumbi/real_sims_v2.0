from django.shortcuts import redirect, render
from .models import BillItem
from .forms import CreateBillItemForm
from django.urls import reverse
from bill_payment.models import BillPayment
from .forms import EditBillItemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.views import APIView
from rest_framework.response import Response

login_required()
# @permission_required("can_view_bill")


def bills(request):
    bills = BillItem.objects.all().order_by('-created')

    return render(request, 'bill/bills.html', {'bills': bills})


login_required()
# @permission_required("can_create_bill")


def create_bill(request):

    if request.method == 'GET':
        form = CreateBillItemForm()
        return render(request, 'bill/create_bill.html', {'form': form})
    if request.method == 'POST':
        form = CreateBillItemForm(request.POST)
        if form.is_valid():
            bill_item_obj = form.save()

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
        vendor=bill_obj.vendor,
        amount=bill_obj.total,
        bill=bill_obj,
    )
    bill_payment_obj.save()
    bill_obj.fully_paid = True
    bill_obj.save(update_fields=['fully_paid'])

    try:
        qb_bill_payment_obj = bill_payment_obj.create_qb_bill_payment_obj()
    except:
        pass
    else:
        bill_payment_obj.qb_id = qb_bill_payment_obj.Id
        bill_payment_obj.synced = True
        bill_payment_obj.save(update_fields=['qb_id', 'synced'])
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
            'vendor': bill_obj.vendor,
            'description': bill_obj.description,
            'quantity': bill_obj.quantity,
            'price_per_quantity': bill_obj.price_per_quantity,
            'total': bill_obj.total
        }
        bill_edit_form = EditBillItemForm(request.POST, initial=initial_data)
        if bill_edit_form.is_valid():
            if bill_edit_form.has_changed():
                bill_obj.vendor = bill_edit_form.cleaned_data['vendor']
                bill_obj.description = bill_edit_form.cleaned_data['description']
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


def view_summaries(request):
    return render(request, 'bill/bill_summaries.html')


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
