from .models import Item


class ItemManager():
    def get_lunch_item(self):
        return Item.objects.get(name='Lunch')

    def get_transport_item(self):
        return Item.objects.get(name='Transport')
