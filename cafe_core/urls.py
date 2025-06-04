# cafe_core/urls.py
from django.urls import path
from . import views

app_name = 'cafe_core' # Define an app namespace

urlpatterns = [
    path('', views.index_view, name='index'),
    path('menu/', views.menu_view, name='menu'),
    path('contact/', views.contact_view, name='contact'),
]
