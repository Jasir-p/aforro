from django.shortcuts import render
from rest_framework import views,permissions,response
from .pagination import paginate_queryset_with_serializer
from apps.products.models import Products
from .filters import ProductSearchFilter
from .serializers import ProductSearchSerializer

# Create your views here.



class ProductSearchView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Products.objects.select_related('category')
        queryset = ProductSearchFilter(
            request.GET,
            queryset=products
        ).qs

        sort = request.query_params.get("sort")

        if sort == 'price':
            queryset = queryset.order_by("price")

        elif sort == "newest":
            queryset = queryset.order_by("-created_at")

        elif sort == "relevance":
            if request.query_params.get("q"):
                queryset = queryset.order_by("-relevance")

        else:
            queryset = queryset.order_by("id")

        return paginate_queryset_with_serializer(queryset, request, ProductSearchSerializer)


