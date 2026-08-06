from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Team, TeamMember
from .serializers import TeamSerializer


class TeamListCreateView(generics.ListCreateAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        team = serializer.save(created_by=self.request.user)

        TeamMember.objects.create(
            team=team,
            user=self.request.user,
            role=TeamMember.Role.OWNER,
        )


class TeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user)