from django.urls import path
from .views import (
    TeamListCreateView,
    TeamDetailView,
    JoinTeamView,
)

urlpatterns = [
    path("", TeamListCreateView.as_view(), name="team-list"),
    path("join/", JoinTeamView.as_view(), name="join-team"),   # <-- join pehle
    path("<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    
]