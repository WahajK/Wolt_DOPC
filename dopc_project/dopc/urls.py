from django.urls import path
from . import views

urlpatterns = [
    path('delivery-order-price', views.calculate_price, name='delivery-order-price'),
]
