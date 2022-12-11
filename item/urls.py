from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.ItemListView.as_view(), name='item_list'),
    path('create/', views.ItemCreateView.as_view(), name='create_item'),
    path('update/<int:pk>/', views.ItemUpdateView.as_view(), name="update_item"),
    path('read/<int:pk>/', views.ItemReadView.as_view(), name="read_item"),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
    path('list/items/', views.items, name='items')
]
