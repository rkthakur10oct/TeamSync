from rest_framework import serializers

from .models import Task
from teams.models import TeamMember


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    assigned_to_name = serializers.ReadOnlyField(source="assigned_to.username")

    class Meta:
        model = Task
        fields = "__all__"

    def validate(self, data):
        team = data.get("team", getattr(self.instance, "team", None))
        assigned_to = data.get(
            "assigned_to",
            getattr(self.instance, "assigned_to", None),
        )

        if assigned_to and not TeamMember.objects.filter(
            team=team,
            user=assigned_to,
        ).exists():
            raise serializers.ValidationError(
                {
                    "assigned_to": "This user is not a member of the selected team."
                }
            )

        return data