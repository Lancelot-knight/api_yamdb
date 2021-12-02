from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.enums import Roles


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == Roles.ADMIN
        return False


class AdminOrSuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                (
                        request.user.role == Roles.ADMIN or
                        request.user.is_superuser
                )
        )
