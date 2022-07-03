from django.contrib.auth.models import User
from django.http import HttpRequest
from rest_framework.permissions import BasePermission


class IsAdminOrStaff(BasePermission):
    """
    Allow only Admin or Staff Users
    """

    def has_permission(self, request: HttpRequest, view):
        """
        Returns True if user is admin or staff
        Args:
            request: HttpRequest
            view:

        Returns:

        """
        user: User = request.user
        return user and (user.is_superuser or user.is_staff)


class CanDeleteOrGet(BasePermission):
    """
    If authenticated User is Admin/Staff, then
    the user can perform delete, otherwise can only
    access HTTP GET Request
    """

    def has_permission(self, request, view):
        """
        Returns True if request method is get or delete only if authenticated user
        is admin
        Args:
            request: HttpRequest
            view:

        Returns:

        """
        user: User = request.user
        return request.method == "GET" or (
            request.method == "POST" and (user.is_staff or user.is_superuser)
        )
