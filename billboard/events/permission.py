from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.username

    def has_object_permission(self, request, view, obj):
        return request.user in obj.users
