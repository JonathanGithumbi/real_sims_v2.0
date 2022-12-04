from invoice.models import BalanceTable
from invoice.InvoiceManager import InvoiceManager

class PaymentManager():

    def make_payment(self, payment_form, invoice):
        # get payment_object
        payment_object = payment_form.save(commit=False)

        """Apply Payment to this invoice"""
        payment_object.invoice = invoice
        payment_object.save()

        #update the invoice balance 
        invoice_manager = InvoiceManager()
        invoice_manager.receive_payment(payment_object.amount, invoice)

        # decrease the balance table
        bal_record = BalanceTable.objects.get(student=invoice.student)
        bal_record.decrease_balance(payment_object.amount)
        return payment_object
