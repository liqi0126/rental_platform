from rest_framework import permissions


class IsAdminOrCannotUpdateAndDestroy(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if bool(request.user and request.user.is_staff):
            return True

        if request.method in ['update', 'partial_update', 'destroy']:
            return False

        return True
