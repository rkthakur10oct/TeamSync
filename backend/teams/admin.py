from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_by",
        "join_code",
        "created_at",
    )

    readonly_fields = (
        "join_code",
        "created_at",
        "updated_at",
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "user",
        "role",
        "joined_at",
    )