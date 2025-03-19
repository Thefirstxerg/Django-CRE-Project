from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_name, name='add_name'),
    path('delete_selected/', views.delete_selected_names, name='delete_selected_names'),
    path('clear/', views.clear_names, name='clear_names'),
    path('names/', views.get_names, name='get_names'),
]