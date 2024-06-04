from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Add this line for the root URL
    path('vyrobci/', views.vyrobce_list, name='vyrobce_list'),
    path('zavody/', views.zavod_list, name='zavod_list'),
    path('auta/', views.auto_list, name='auto_list'),
    path('auto/<int:id>/', views.auto_detail, name='auto_detail'),
]
