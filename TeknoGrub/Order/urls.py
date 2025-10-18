
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_history_view, name='order-history'),
]