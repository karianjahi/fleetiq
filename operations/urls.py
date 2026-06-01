from django.urls import path
from . import views

urlpatterns = [
    path("api/dashboard/kpis/", views.dashboard_kpis, name="dashboard-kpis"),
    
    path("api/alerts/latest/", views.latest_alerts, name="latest-alerts"),
    
    path("api/alerts/summary-by-type/", views.alert_summary_by_type, name="alert-summary-by-type"),
    
    path("api/alerts/summary-by-severity/", views.alert_count_by_severity),
    
    path("api/voyages/status-summary/", views.voyage_status_summary),
    
    path("api/alerts/over-time/", views.alerts_over_time, name="alerts-over-time"),
    
    path("dashboard/", views.dashboard_view, name="dashboard"),
]


