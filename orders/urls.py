from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('order-create/', views.OrderCreateView.as_view(), name='checkout-cart'),
]
