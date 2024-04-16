from rest_framework import pagination

class CoursePaginator(pagination.PageNumberPagination):
    page_size = 5
    # page_size_query_param = 'page_size'
    # max_page_size = 10

class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'
    # max_page_size = 10