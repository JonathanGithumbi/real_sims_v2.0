from .models import PettyCash


class PettyCashManager():
 
    def get_petty_cash_object(self):
        petty_cash_obj = PettyCash.objects.get(pk=1)
        return petty_cash_obj

    def increase_petty_cash_balance(self, amount):
        petty_cash_obj = self.get_petty_cash_object()
        petty_cash_obj.balance = petty_cash_obj.balance + amount
        petty_cash_obj.save()
        return True

    def decrease_petty_cash_balance(self, amount):
        petty_cash_obj = self.get_petty_cash_object()
        petty_cash_obj.balance = petty_cash_obj.balance - amount
        petty_cash_obj.save()
        return True

    def get_petty_cash_balance(self):
        obj = self.get_petty_cash_object()
        return obj.balance
