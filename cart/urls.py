from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart-detail'),
]