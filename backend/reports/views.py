from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Count

from teams.models import Team
from tasks.models import Task
from notifications.models import Notification
from teams.models import Team
from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

from datetime import date


class DashboardReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        total_teams = Team.objects.filter(
            team_members__user=request.user
        ).distinct().count()

        total_tasks = Task.objects.filter(
            created_by=request.user
        ).count()

        todo_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.TODO
        ).count()

        in_progress_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.IN_PROGRESS
        ).count()

        review_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.REVIEW
        ).count()

        completed_tasks = Task.objects.filter(
            created_by=request.user,
            status=Task.Status.DONE
        ).count()

        unread_notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return Response({
            "total_teams": total_teams,
            "total_tasks": total_tasks,
            "todo_tasks": todo_tasks,
            "in_progress_tasks": in_progress_tasks,
            "review_tasks": review_tasks,
            "completed_tasks": completed_tasks,
            "unread_notifications": unread_notifications,
        })
        
        
class TeamPerformanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        teams = Team.objects.filter(
            team_members__user=request.user
        ).distinct()

        data = []

        for team in teams:

            total_tasks = Task.objects.filter(team=team).count()

            completed_tasks = Task.objects.filter(
                team=team,
                status=Task.Status.DONE
            ).count()

            pending_tasks = total_tasks - completed_tasks

            members = team.team_members.count()

            percentage = 0
            if total_tasks > 0:
                percentage = round(
                    (completed_tasks / total_tasks) * 100,
                    2
                )

            data.append({
                "team": team.name,
                "members": members,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_percentage": percentage,
            })

        return Response(data)
    
    
class UserProductivityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        users = User.objects.all()

        data = []

        for user in users:

            assigned = Task.objects.filter(
                assigned_to=user
            ).count()

            completed = Task.objects.filter(
                assigned_to=user,
                status=Task.Status.DONE
            ).count()

            pending = assigned - completed

            data.append({
                "username": user.username,
                "assigned_tasks": assigned,
                "completed_tasks": completed,
                "pending_tasks": pending,
            })

        return Response(data)            
    
    
class OverdueTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        overdue = Task.objects.filter(
            due_date__lt=date.today()
        ).exclude(
            status=Task.Status.DONE
        )

        data = []

        for task in overdue:
            data.append({
                "task": task.title,
                "assigned_to": (
                    task.assigned_to.username
                    if task.assigned_to
                    else None
                ),
                "due_date": task.due_date,
                "status": task.status,
            })

        return Response(data)
    
class TodayTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        today_tasks = Task.objects.filter(
            due_date=date.today()
        )

        data = []

        for task in today_tasks:
            data.append({
                "task": task.title,
                "assigned_to": (
                    task.assigned_to.username
                    if task.assigned_to
                    else None
                ),
                "status": task.status,
                "team": task.team.name,
            })

        return Response(data)        