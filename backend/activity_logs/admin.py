from django.contrib import admin
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "target",
        "created_at",
    )

    list_filter = (
        "action",
    )

    search_fields = (
        "user__username",
        "target",
    )

    ordering = (
        "-created_at",
    )