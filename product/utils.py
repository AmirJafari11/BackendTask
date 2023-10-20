from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request


class CustomPagination(PageNumberPagination):
    """
        The custom pagination.
    """

    # page_size = 2  # Number of items per page (default)
    page_size_query_param = 'page_size'  # Custom query parameter to override page size
    max_page_size = 100  # Maximum page size allowed

    def get_page_size(self, request: Request):

        if request.user.is_superuser:
            self.max_page_size = 1000

        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is None:
            return self.max_page_size

        return min(int(page_size), self.max_page_size)
