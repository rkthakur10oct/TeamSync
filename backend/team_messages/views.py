from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from teams.models import TeamMember
from .models import TeamMessage
from .serializers import TeamMessageSerializer


class TeamMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs["team_id"]

        is_member = TeamMember.objects.filter(
            team_id=team_id,
            user=self.request.user,
        ).exists()

        if not is_member:
            raise PermissionDenied("You are not a member of this team.")

        return TeamMessage.objects.filter(team_id=team_id)

    def perform_create(self, serializer):
        team_id = self.kwargs["team_id"]

        is_member = TeamMember.objects.filter(
            team_id=team_id,
            user=self.request.user,
        ).exists()

        if not is_member:
            raise PermissionDenied("You are not a member of this team.")

        serializer.save(
            sender=self.request.user,
            team_id=team_id,
        )
