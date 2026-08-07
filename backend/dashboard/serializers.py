from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()

    total_teams = serializers.IntegerField()

    unread_notifications = serializers.IntegerField()

    recent_activities = serializers.ListField()