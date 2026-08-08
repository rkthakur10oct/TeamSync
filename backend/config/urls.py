"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # =========================================================
    # ADMIN
    # =========================================================
    path("admin/", admin.site.urls),

    # =========================================================
    # AUTHENTICATION
    # =========================================================
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # =========================================================
    # EXISTING API ROUTES
    # =========================================================
    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    path(
        "api/teams/",
        include("teams.urls"),
    ),

    path(
        "api/tasks/",
        include("tasks.urls"),
    ),

    path(
        "api/messages/",
        include("team_messages.urls"),
    ),

    path(
        "api/notifications/",
        include("notifications.urls"),
    ),

    path(
        "api/dashboard/",
        include("dashboard.urls"),
    ),

    path(
        "api/attachments/",
        include("attachments.urls"),
    ),

    path(
        "api/reports/",
        include("reports.urls"),
    ),

    # =========================================================
    # API V1
    # =========================================================
    path(
        "api/v1/accounts/",
        include("accounts.urls"),
    ),

    path(
        "api/v1/teams/",
        include("teams.urls"),
    ),

    path(
        "api/v1/tasks/",
        include("tasks.urls"),
    ),

    path(
        "api/v1/messages/",
        include("team_messages.urls"),
    ),

    path(
        "api/v1/notifications/",
        include("notifications.urls"),
    ),

    path(
        "api/v1/dashboard/",
        include("dashboard.urls"),
    ),

    path(
        "api/v1/attachments/",
        include("attachments.urls"),
    ),

    path(
        "api/v1/reports/",
        include("reports.urls"),
    ),

    # =========================================================
    # API DOCUMENTATION
    # =========================================================

    # OpenAPI schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    # ReDoc
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]


# =============================================================
# MEDIA FILES
# =============================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )