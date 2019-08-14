from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class ResultLimitOffsetPagination(LimitOffsetPagination):
    default_limit=5
    max_limit=1

class ResultSetPagination(PageNumberPagination):
    page_size=10