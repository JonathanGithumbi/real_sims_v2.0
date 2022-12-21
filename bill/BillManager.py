from .models import Bill, BillItem


class BillManager():
    def get_total_amount_due_bills(self):
        all_bills = Bill.objects.all()
        amount_due = 0
        for bill in all_bills:
            amount_due += bill.get_amount_due()

        return amount_due

    def get_total_amount_due_billitems(self, bill):
        all_billitems = BillItem.objects.filter(bill=bill)
        amount_due = 0
        for item in all_billitems:
            amount_due = item.get_amount_due()

        return amount_due
