from rest_framework import serializers
from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "description",
            "join_code",
            "created_by",
            "created_at",
            "updated_at",
        ]
        
from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = TeamMember
        fields = [
            "id",
            "username",
            "role",
            "joined_at",
        ]        