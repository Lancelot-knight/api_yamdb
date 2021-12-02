from rest_framework.permissions import SAFE_METHODS, BasePermission

from reviews.enums import Roles


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.role == Roles.ADMIN
        return False


class AdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == Roles.ADMIN

    # def has_object_permission(self, request, view, obj):
    #     return obj == request.user
