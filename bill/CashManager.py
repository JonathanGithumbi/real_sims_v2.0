from .models import PettyCash as Cash


class CashManager():

    def get_cash_object(self):
        cash_obj = Cash.objects.get(pk=1)
        return cash_obj

    def increase_cash_balance(self, amount):
        cash_obj = self.get_cash_object()
        cash_obj.balance = cash_obj.balance + amount
        cash_obj.save()
        return True

    def decrease_petty_cash_balance(self, amount):
        cash_obj = self.get_cash_object()
        cash_obj.balance = cash_obj.balance - amount
        cash_obj.save()
        return True

    def get_cash_balance(self):
        obj = self.get_cash_object()
        return obj.balance
