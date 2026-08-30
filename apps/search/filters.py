from django_filters import rest_framework as filters
from django.db import models
from apps.products.models import Products



class ProductSearchFilter(filters.FilterSet):

    q = filters.CharFilter(
        method="product_search"
    )
    category = filters.NumberFilter(
        field_name="category_id"
    )
    min_price = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    max_price = filters.NumberFilter(
        field_name="price",
        lookup_expr="lte"
    )

    store_id = filters.NumberFilter(
        field_name="inventory__store_id"
    )
    in_stock = filters.BooleanFilter(
        method="filter_in_stock"
    )

    def product_search(self, queryset, name, value):
        value = value.strip()

        if not value:
            return queryset

        queryset=queryset.filter(
            models.Q(title__icontains=value)|
            models.Q(description__icontains=value) |
            models.Q(category__name__icontains=value)

        )

        return queryset.annotate(
            relevance=models.Case(
                models.When(
                    title__iexact=value,
                    then=models.Value(4)
                ),
                models.When(
                    title__istartswith=value,
                    then=models.Value(3)
                ),
                models.When(
                    title__icontains=value,
                    then=models.Value(2)
                ),
                models.When(
                    description__icontains=value,
                    then=models.Value(1)
                ),
                models.When(
                    category__name__icontains=value,
                    then=models.Value(1)
                ),
                default=models.Value(0),
                output_field=models.IntegerField()
            )

            )
        

    def filter_in_stock(self, queryset, name, value):
        store_id = self.data.get("store_id")

        if not store_id:
            return queryset        

        if value:
            return queryset.filter(
                inventory__store_id=store_id,
                inventory__quantity__gt=0


            )
        return queryset.filter(
            inventory__store_id=store_id,
            inventory__quantity=0
            
        )

    class Meta:

        model = Products
        fields = [
            "q", "category", "min_price",
            "max_price", "store_id", "in_stock"

        ]
