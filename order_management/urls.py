# order_management/urls.py
from django.urls import path
from .views import OrderCreateView, OrderDetailView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('order/<int:order_id>/', OrderDetailView.as_view(), name='order-detail'),
]
