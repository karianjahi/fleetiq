from django.urls import path
from . import views

urlpatterns = [
    path("api/dashboard/kpis/", views.dashboard_kpis, name="dashboard-kpis"),
    path("api/alerts/latest/", views.latest_alerts, name="latest-alerts"),
    path("dashboard/", views.dashboard, name="dashboard"),
]


