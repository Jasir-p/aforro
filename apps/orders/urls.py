from django.urls import path
from .views import (
    OrderCreateView,
    OrdersListView
)


urlpatterns = [
    path("orders/", OrderCreateView.as_view(), name='order-create'),
    path("stores/<int:store_id>/orders/", OrdersListView.as_view(), name='orders-list')
]
