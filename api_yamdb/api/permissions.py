from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_superuser


class AdminOrAuthOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
<<<<<<< HEAD
        return request.user.is_authenticated and obj == request.user
=======
        return request.user.is_authenticated and obj == request.user
>>>>>>> feature_3
