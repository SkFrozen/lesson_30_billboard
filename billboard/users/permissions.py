from rest_framework.permissions import SAFE_METHODS, BasePermission


class CreateOnlyOrSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_superuser
