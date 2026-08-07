from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from teams.models import Team
from tasks.models import Task
from notifications.models import Notification


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_teams = Team.objects.filter(
            created_by=request.user
        ).count()

        total_tasks = Task.objects.filter(
            created_by=request.user
        ).count()

        todo_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.TODO,
        ).count()

        in_progress = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.IN_PROGRESS,
        ).count()

        done_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.DONE,
        ).count()

        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False,
        ).count()

        return Response({
            "total_teams": total_teams,
            "total_tasks": total_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress,
            "completed_tasks": done_tasks,
            "unread_notifications": unread_notifications,
        })