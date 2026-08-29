from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer, ProductsListSerializer
from .models import Category, Products

# Create your views here.


class CategoryViews(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductView(viewsets.ModelViewSet):
    queryset = Products.objects.select_related('category')

    def get_serializer_class(self):

        if self.action in ["list","retrieve"]:
            return ProductsListSerializer

        return ProductSerializer

