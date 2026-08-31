from django.urls import path
from .views import ProductSearchView, ProductsuggestView



urlpatterns = [
    path('search/products/', ProductSearchView.as_view()),
    path('search/suggest/', ProductsuggestView.as_view())
]
