from django.urls import path
from .views import (
    TeamListCreateView,
    TeamDetailView,
    JoinTeamView,
    TeamMembersView,
)

urlpatterns = [
    path("", TeamListCreateView.as_view(), name="team-list"),
    path("join/", JoinTeamView.as_view(), name="join-team"),
    path("<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path(
        "<int:team_id>/members/",
        TeamMembersView.as_view(),
        name="team-members",
    ),
]