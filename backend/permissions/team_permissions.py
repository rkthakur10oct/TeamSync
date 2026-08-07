from rest_framework.permissions import BasePermission


class IsTeamOwner(BasePermission):
    """
    Allow access only to the Team Owner.
    """

    message = "Only the team owner can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class IsTeamMember(BasePermission):
    """
    Allow access only to members of the team.
    """

    message = "You are not a member of this team."

    def has_object_permission(self, request, view, obj):
        return obj.members.filter(id=request.user.id).exists()


class IsOwnerOrReadOnly(BasePermission):
    """
    Everyone can read.
    Only owner can modify.
    """

    message = "Only the owner can modify this team."

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        return obj.created_by == request.user