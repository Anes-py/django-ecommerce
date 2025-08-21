from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.OrderCreateView.as_view(), name='checkout-cart'),
]