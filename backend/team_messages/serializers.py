from rest_framework import serializers
from .models import TeamMessage


class TeamMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = TeamMessage
        fields = [
            "id",
            "team",
            "sender",
            "sender_name",
            "message",
            "created_at",
        ]
        read_only_fields = [
            "sender",
            "created_at",
        ]