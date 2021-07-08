from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'count'
    page_size = 4
    max_page_size = 100
    page_query_param = 'page'

