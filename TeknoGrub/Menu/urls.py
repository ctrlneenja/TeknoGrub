from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.favorites_view, name='favorites'),
    path('', views.menu_view, name='menu'),
]

