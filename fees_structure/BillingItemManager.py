from item.ItemManager import ItemManager
from .models import BillingItem


class BillingItemManager():
    def get_lunch_bill(self):
        item_man = ItemManager()
        lunch_item = item_man.get_lunch_item()
        try:
            lunch_bill = BillingItem.objects.get(item=lunch_item)
        except:
            print("error fetching lunch bill item")

        return lunch_bill

    def get_trans_bill(self):
        item_man = ItemManager()
        trans_item = item_man.get_transport_item()
        try:
            trans_bill = BillingItem.objects.get(item=trans_item)
        except:
            print("error fetching lunch bill item")

        return trans_bill
