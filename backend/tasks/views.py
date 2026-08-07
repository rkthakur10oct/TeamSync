from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from django.db.models import Q
from notifications.models import Notification
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from activity_logs.utils import create_activity
from activity_logs.models import ActivityLog


class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "priority",
        "assigned_to",
        "team",
    ]

    search_fields = [
        "title",
        "description",
    ]

    ordering_fields = [
        "due_date",
        "created_at",
        "priority",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(created_by=self.request.user) |
            Q(assigned_to=self.request.user)
        ).distinct()

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date:
            queryset = queryset.filter(due_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(due_date__lte=end_date)

        return queryset
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)

        if task.assigned_to:
            Notification.objects.create(
               user=task.assigned_to,
               title="New Task Assigned",
               message=f'You have been assigned the task "{task.title}".',
               notification_type=Notification.Type.TASK_ASSIGNED,
            )
        
        # Activity Log
        create_activity(
            user=self.request.user,
            action=ActivityLog.Action.CREATED,
            target=task.title,
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
            
        create_activity(
            user=self.request.user,
            action=ActivityLog.Action.UPDATED,
            target=task.title,
        )    
        
        
    def perform_destroy(self, instance):
        title = instance.title

        create_activity(
            user=self.request.user,
            action=ActivityLog.Action.DELETED,
            target=title,
        )

        instance.delete()    