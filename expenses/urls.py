from django.urls import path
from . import views
urlpatterns = [
    path('', views.expenses, name='expenses'),
    path('add-expense', views.add_expense, name='add_expense'),
    path('confrm-add/<int:id>/', views.confirm_add_expense,
         name='confirm_add_expense'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit_expense'),
    path('discard-expense/<int:id>', views.discard_expense, name='discard_expense'),
    path('summaries/', views.summaries, name='expense_summaries'),
    path('summaries/expense-distribution-api',
         views.chart_data, name='chart_data')
]
