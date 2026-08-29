from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StoreViews,
    InventoryCreateViews,
    InventoryListView
)


router = DefaultRouter()
router.register(r'stores', StoreViews, basename='stores')

urlpatterns = [

  path("", include(router.urls)), 
  path("inventory/add/", InventoryCreateViews.as_view(),name='inventory-create'),
  path("stores/<int:store_id>/inventory/", InventoryListView.as_view(), name="store-inventory")
]
