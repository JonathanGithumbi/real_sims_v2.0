from .models import BillItem as Bill
from .PettyCashManager import PettyCashManager


class BillManager():
    def delete_bill(self, bill_obj):
        if bill_obj.category == "Deposit":
            self.delete_deposit_bill(bill_obj)
            return True
        else:
            petty_cash_manager = PettyCashManager()
            petty_cash_manager.increase_petty_cash_balance(bill_obj.total)

            bill_obj.delete()
            return True

    def delete_deposit_bill(self, bill_obj):
        petty_cash_manager = PettyCashManager()
        petty_cash_manager.decrease_petty_cash_balance(bill_obj.total)
        bill_obj.delete()
        return True

    def create_bill(self, create_bill_form):

        bill_obj = create_bill_form.save()
        petty_cash_manager = PettyCashManager()
        petty_cash_manager.decrease_petty_cash_balance(bill_obj.total)
        # Populate the balance attribute
        bill_obj.balance = petty_cash_manager.get_petty_cash_balance()
        bill_obj.save()
        return bill_obj

    def create_deposit_bill(self, topup_form):
        # By now the pety cash balance is incresedd
        topup_form.is_valid()
        amount = topup_form.cleaned_data['amount']
        petty_cash_manager = PettyCashManager()
        petty_cash_manager.increase_petty_cash_balance(amount)

        depo_transaction = Bill.objects.create(
            category="Deposit",
            description="Top Up",
            total=amount,
            quantity=1,
            price_per_quantity=amount,
            balance=petty_cash_manager.get_petty_cash_balance(),
        )
        return depo_transaction
