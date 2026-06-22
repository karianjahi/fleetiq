from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    
    path("", views.landing_page, name="landing_page"),
    
    path("api/dashboard/kpis/", views.dashboard_kpis, name="dashboard-kpis"),
    
    path("api/alerts/latest/", views.latest_alerts, name="latest-alerts"),
    
    path("api/alerts/summary-by-type/", views.alert_summary_by_type, name="alert-summary-by-type"),
    
    path("api/alerts/summary-by-severity/", views.alert_count_by_severity),
    
    path("api/voyages/status-summary/", views.voyage_status_summary),
    
    path("api/alerts/over-time/", views.alerts_over_time, name="alerts-over-time"),
    
    path("api/alerts/top-vessels/", views.top_vessels_by_alerts, name="top-alerts-vessels"),
    
    path("vessels/", views.vessel_list_view, name="vessel list"),
    
    path("api/vessels/", views.VesselListAPIView.as_view(), name="vessel-list-api"),
    
    path("vessels/<int:vessel_id>/", views.vessel_detail_view, name="vessel-detail"),
    
    path("api/vessels/<int:pk>/", views.VesselDetailAPIView.as_view(), name="vessel-detail-api"),
    
    path("api/vessels/<int:vessel_id>/voyages/", views.VesselVoyageListAPIView.as_view(), name="vessel-voyages-api"),
    
    path("api/vessels/<int:vessel_id>/alerts/", views.VesselAlertListAPIView.as_view(), name="vessel-alerts-api"),
    
    path("api/vessels/<int:vessel_id>/kpis/", views.vessel_kpis, name="vessel-kpis"),
    
    path("api/vessels/<int:vessel_id>/health-status/", views.vessel_health_status, name="vessel-health"),
    
    path("api/fleet/health-distribution/", views.fleet_health_distribution, name="fleet-health-distribution"),
]


