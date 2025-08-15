from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('comment/add/<int:product_id>/', views.CommentCreateView.as_view(), name='comment-add'),
]
