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
            "created_by",
            "created_at",
            "updated_at",
        ]