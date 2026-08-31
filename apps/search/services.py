from django.db.models import When, Case, Value, IntegerField
from apps.products.models import Products


def product_with_priority(query):

    return (Products.objects.filter(
            title__icontains=query
        ).annotate(
            match_priority=Case(
                When(
                    title__istartswith=query,
                    then=Value(0)
                ),
                default=Value(1),
                output_field=IntegerField()
            
            )
        ).order_by("match_priority", "title")[:10]
            
        )
