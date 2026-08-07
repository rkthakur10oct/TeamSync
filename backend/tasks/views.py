from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assigned_to=self.request.user)
        ).distinct()
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assigned_to=self.request.user)
        ).distinct()