from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "team",
        "assigned_to",
        "priority",
        "status",
        "due_date",
    )

    list_filter = (
        "status",
        "priority",
        "team",
    )

    search_fields = (
        "title",
        "description",
    )