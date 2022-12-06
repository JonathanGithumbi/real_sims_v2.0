from django.urls import path
from . import views
urlpatterns = [
    path('new-item/', views.create_salesitem, name='add_salesitem'),
    path('view-sales-items/', views.view_sales_item, name='view_sales_items'),
    path('edit-sales-item/<int:id>', views.edit_salesitem, name='edit_salesitem'),
    path('delete-sales-item/<int:id>/',
         views.delete_salesitem, name="delete_salesitem"),
    path('salesitem-editform/<int:id>', views.get_salesitem_editform,
         name='get_salesitem_editform')
]
