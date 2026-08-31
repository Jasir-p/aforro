from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        return f'{self.request.path}?page={page_number}'

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        return f'{self.request.path}?page={page_number}'





def paginate_queryset_with_serializer(queryset, request, serializer_class, page_size=20):
    """
    Paginate a queryset and return a paginated Response with serialized data.
    """
    paginator = StandardResultsSetPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)