from .models import Item


class ItemManager():
    def get_lunch_item(self):
        lunch_item = Item.objects.get(name='Lunch')
        return lunch_item

    def get_transport_item(self):
        transport_item = Item.objects.get(name='Transport')
        return transport_item
