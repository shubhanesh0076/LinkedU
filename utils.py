import constants as const
import re
from typing import Any
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class Settings:

    @staticmethod
    def email_validate(email):
        email_pattern = const.email_validator_pattern
        if re.match(email_pattern, email):
            return True
        return False

    @staticmethod
    def get_payload(
        detail: Any,
        message: str = None,
        is_authenticated: bool = False,
        extra_information: dict = {},
    ):
        return {
            "is_authenticated": is_authenticated,
            "message": message,
            "detail": detail,
            "extra_information": extra_information,
        }

    def is_authenticated_status(self, request):
        """
        check the authentication status...
        """
        try:
            if request.user.is_authenticated:
                return True
            return False

        except Exception as e:
            return False

    def custome_message(self, error):
        if "to_user" in error.detail:
            return str(error.detail.get("to_user")[0])
        elif "non_field_errors" in error.detail:
            return str(error.detail.get("non_field_errors")[0])
        else:
            return "Invalid request."


st = Settings()


class CustomPageNumberPagination(PageNumberPagination):
    page_size = const.page_size
    page_size_query_param = const.page_size_query_param
    max_page_size = const.max_page_size

    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "count": self.page.paginator.count,
                "results": data,
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        self.request = request  # Set the request object here
        page_number = request.query_params.get(self.page_query_param, 1)
        try:
            self.page = super().paginate_queryset(queryset, request, view)
            if self.page is None:
                raise NotFound()
        except NotFound:
            return None
        return list(self.page)

    def get_custom_error_response(self):
        return Response(
            {"detail": "Invalid page. Please select a valid page number."}, status=404
        )


class StandardResultsSetPagination(CustomPageNumberPagination): ...
