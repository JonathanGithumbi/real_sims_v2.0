from django.urls import path
from . import views
urlpatterns = [
    path('list/years/', views.YearListView.as_view(), name='year_list'),
    path('list/terms/<int:pk>/',
         views.TermListView.as_view(), name='term_list'),
    path('create/year/', views.YearCreateView.as_view(),
         name='create_year'),
    path('create/term/<int:year_pk>', views.TermCreateView.as_view(),
         name='create_term'),
    path('update/year/<int:pk>/', views.YearUpdateView.as_view(),
         name="update_year"),
    path('update/term/<int:pk>/<int:pk2>', views.TermUpdateView.as_view(),
         name="update_term"),
    path('read/year/<int:pk>/', views.YearReadView.as_view(),
         name="read_year"),
    path('read/term/<int:pk>/', views.TermReadView.as_view(),
         name="read_term"),
    path('delete/year/<int:pk>/', views.YearDeleteView.as_view(),
         name='delete_year'),
    path('delete/term/<int:pk>/<int:pk2>', views.TermDeleteView.as_view(),
         name='delete_term'),
    path('list/years/years/', views.years, name='years'),
    path('list/terms/terms/', views.terms, name='terms')
]
