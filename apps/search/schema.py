from drf_spectacular.utils import extend_schema, OpenApiParameter


search_schema = extend_schema(
    summary="Search Products",
    parameters=[
        OpenApiParameter("q", str, description="Search keyword"),
        OpenApiParameter("category", int, description="Category ID"),
        OpenApiParameter("min_price", float, description="Minimum price"),
        OpenApiParameter("max_price", float, description="Maximum price"),
        OpenApiParameter("store_id", int, description="Store ID"),
        OpenApiParameter("in_stock", bool, description="Filter by stock"),
        OpenApiParameter(
            "sort",
            str,
            description="Sort by: price, newest, relevance"
        ),
        OpenApiParameter(
            "page",
            int,
            description="Page number"
        ),
        OpenApiParameter(
            "page_size",
            int,
            description="Number of results per page"
        ),
    ],
)

suggest_schema = extend_schema(
    summary="Product Suggestions",
    parameters=[
        OpenApiParameter(
            "q",
            str,
            description="Search query (minimum 3 characters)",
            required=True,
        ),
    ],
)
