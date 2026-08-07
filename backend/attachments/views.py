from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Attachment
from .serializers import AttachmentSerializer


class AttachmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return Attachment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class AttachmentDeleteView(generics.DestroyAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    queryset = Attachment.objects.all()