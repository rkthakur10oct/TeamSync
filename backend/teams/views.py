from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from permissions.team_permissions import IsOwnerOrReadOnly


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
    permission_classes = [
    IsAuthenticated,
    IsOwnerOrReadOnly,
]

    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user)
    

class JoinTeamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        join_code = request.data.get("join_code")

        if not join_code:
            return Response(
                {"error": "join_code is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            team = Team.objects.get(join_code=join_code)
        except (Team.DoesNotExist, ValidationError, ValueError):
            return Response(
                {"error": "Invalid join code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        member, created = TeamMember.objects.get_or_create(
            team=team,
            user=request.user,
            defaults={"role": TeamMember.Role.MEMBER},
        )

        if not created:
            return Response(
                {"message": "You are already a member"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "message": "Successfully joined the team",
                "team": team.name,
            },
            status=status.HTTP_201_CREATED,
        )
        
        
class TeamMembersView(generics.ListAPIView):
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        team_id = self.kwargs["team_id"]

        return TeamMember.objects.filter(
            team_id=team_id
        ).select_related("user")        