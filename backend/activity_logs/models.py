from django.db import models
from django.conf import settings


class ActivityLog(models.Model):

    class Action(models.TextChoices):
        CREATED = "CREATED", "Created"
        UPDATED = "UPDATED", "Updated"
        DELETED = "DELETED", "Deleted"
        ASSIGNED = "ASSIGNED", "Assigned"
        JOINED = "JOINED", "Joined"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices,
    )

    target = models.CharField(
        max_length=200,
    )

    description = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.user.username} - {self.action}"
    
    