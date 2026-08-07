from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q
from notifications.models import Notification

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assigned_to=self.request.user)
        ).distinct()
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)

        if task.assigned_to:
            Notification.objects.create(
               user=task.assigned_to,
               title="New Task Assigned",
               message=f'You have been assigned the task "{task.title}".',
               notification_type=Notification.Type.TASK_ASSIGNED,
            )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assigned_to=self.request.user)
        ).distinct()
        
    def perform_update(self, serializer):
        task = serializer.save()

        if task.assigned_to:
            Notification.objects.create(
                user=task.assigned_to,
                title="Task Updated",
                message=f'Task "{task.title}" has been updated.',
                notification_type=Notification.Type.TASK_UPDATED,
            )    
            
            