from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # Allow client to set size
    max_page_size = 100  # Maximum allowed