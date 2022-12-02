class PaymentManager():

    def make_payment(self, payment, invoice):
        """Apply Payment to this invoice"""
        payment.invoice = invoice
        payment.save()
        return payment
