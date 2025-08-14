from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/<str:product_id>/', views.AddToCartView.as_view(), name='cart-add')
]