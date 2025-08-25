from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard_view, name='user-dashboard'),
]
