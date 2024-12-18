from rest_framework.pagination import PageNumberPagination

class EnlacePagination(PageNumberPagination):
    page_size = 10

class InternetPagination(PageNumberPagination):
    page_size = 10