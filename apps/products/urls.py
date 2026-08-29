from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import(
    CategoryViews,
    ProductView
)


router = DefaultRouter()

router.register(r'category', CategoryViews, basename='category')
router.register(r'products', ProductView, basename='products')


urlpatterns = [
    path("", include(router.urls)),
]


