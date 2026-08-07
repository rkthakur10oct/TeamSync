from .models import ActivityLog


def create_activity(user, action, target):
    ActivityLog.objects.create(
        user=user,
        action=action,
        target=target,
    )