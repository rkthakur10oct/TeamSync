from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from tasks.models import Task
from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    # Required for file uploads
    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_queryset(self):
        task_id = self.kwargs["task_id"]

        return Attachment.objects.filter(
            task_id=task_id
        ).order_by("-uploaded_at")

    def perform_create(self, serializer):
        task = get_object_or_404(
            Task,
            id=self.kwargs["task_id"],
        )

        serializer.save(
            task=task,
            uploaded_by=self.request.user,
        )


class AttachmentDeleteView(generics.DestroyAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    queryset = Attachment.objects.all()