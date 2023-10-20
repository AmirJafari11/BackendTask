from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsSuperUserOrStaff(BasePermission):
    """
        The custom permission for granting access to users who are either superusers or the author (product registrator)
        of the object being accessed.
    """

    def has_object_permission(self, request: Request, view, obj) -> bool:

        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user == obj.u_id:
            return True

        return False
