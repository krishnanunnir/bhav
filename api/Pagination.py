from django.conf import settings
from rest_framework import pagination
from rest_framework.response import Response


class PageNumberCountPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_numer': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
