from rest_framework import serializers
from .models import Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source="uploaded_by.username")

    class Meta:
        model = Attachment
        fields = [
            "id",
            "task",
            "uploaded_by",
            "file",
            "uploaded_at",
        ]

        read_only_fields = [
            "task",
            "uploaded_by",
            "uploaded_at",
        ]