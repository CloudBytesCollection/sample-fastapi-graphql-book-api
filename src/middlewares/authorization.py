from strawberry.permission import BasePermission
from strawberry.types import Info
import typing


class RequestHeaderValidation(BasePermission):
    """
    Custom Request Header Validation class
    Can be expanded to check Authorization headers and
    other custom third party headers
    """

    message = "Unauthorized request attempt. Missing required request header(s)."

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        return self.has_valid_enforced_headers(info.context["request"].headers)

    def has_valid_enforced_headers(self, headers: dict):
        """Check the value of the desired headers where applicable"""
        if headers["x-bookapi-token"]:
            return (
                True if headers["x-bookapi-token"] == "fake-token-value123" else False
            )
        else:
            return False
