from django.urls import path
from . import views

app_name = 'randomizer'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_name, name='add_name'),
    path('delete_selected/', views.delete_selected_names, name='delete_selected_names'),
    path('clear/', views.clear_names, name='clear_names'),
    path('names/', views.get_names, name='get_names'),
    path('randomize/', views.randomize_cohort, name='randomize_cohort'),
    path('updates/', views.updates_view, name='updates'),
]