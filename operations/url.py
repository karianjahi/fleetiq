from django.urls import path
from . import views

urlpatters = [
    path("api/dashboard/kpis/", views.dashboard_kpis, name="dashboard-kpis"),
    path("api/alerts/latest/", views.latest_alerts, name="latest-alerts"),
]


