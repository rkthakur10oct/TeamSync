from django.urls import path
from .views import DashboardReportView, TeamPerformanceView, UserProductivityView, OverdueTasksView, TodayTasksView

urlpatterns = [
    path("", DashboardReportView.as_view(), name="dashboard-report"),
    path("teams/", TeamPerformanceView.as_view(), name="team-performance"),
    path("users/", UserProductivityView.as_view(), name="user-productivity"),
    path("overdue/", OverdueTasksView.as_view(), name="overdue-tasks"),
    path("today/", TodayTasksView.as_view(), name="today-tasks"),
]