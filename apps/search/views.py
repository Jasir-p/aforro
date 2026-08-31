from django.shortcuts import render
from rest_framework import views, permissions, response, status
from .pagination import paginate_queryset_with_serializer
from apps.products.models import Products
from .filters import ProductSearchFilter
from .serializers import ProductSearchSerializer
from django.core.cache import cache
from .services import product_with_priority
from .schema import search_schema,suggest_schema

# Create your views here.


@search_schema
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


@suggest_schema
class ProductsuggestView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):

        query = request.query_params.get("q", "").strip().lower()

        if len(query)<3:
            return response.Response(
                {
                    "detail": "Search query must contain at least 3 characters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        cache_key = f"product_suggest:{query}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return response.Response({
                "results": cached_data
            })

        products = product_with_priority(query)

        results = list(products.values_list('title',flat=True))
        cache.set(
            cache_key,
            results,
            timeout=300
        )
        return response.Response({
            'results':results
        })


