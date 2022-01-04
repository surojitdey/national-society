from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# from loguru import logger


class LargeResultsSetPagination(PageNumberPagination):
  page_size = 20
  page_size_query_param = 'page_size'
  max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
  page_size = 2
  page_size_query_param = 'page_size'
  max_page_size = 1000


class CommentPagination(PageNumberPagination):
  page_size = 10
  page_size_query_param = 'page_size'
  max_page_size = 1000

  # @logger.catch
  def get_paginated_response(self, data):
    return Response({
        'next': self.get_next_link(),
        'previous': self.get_previous_link(),
        'count': self.page.paginator.count,
        'data': data
    })
