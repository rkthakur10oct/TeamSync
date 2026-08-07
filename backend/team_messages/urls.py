from django.urls import path
from .views import TeamMessageListCreateView

urlpatterns = [
    path(
        "<int:team_id>/",
        TeamMessageListCreateView.as_view(),
        name="team-messages",
    ),
]