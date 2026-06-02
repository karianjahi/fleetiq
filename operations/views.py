from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncDate

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Vessel, Voyage, TelemetryRecord, OperationalAlert
from .serializers import OperationalAlertSerializer




@api_view(["GET"])
def dashboard_kpis(request):
    data = {
        "total_vessels": Vessel.objects.count(),
        "active_vessels": Vessel.objects.filter(status="active").count(),
        "total_voyages": Voyage.objects.count(),
        "ongoing_voyages": Voyage.objects.filter(status="ongoing").count(),
        "telemetry_records": TelemetryRecord.objects.count(),
        "total_alerts": OperationalAlert.objects.count(),
        "critical_alerts": OperationalAlert.objects.filter(severity=5).count(),
        "unresolved_alerts": OperationalAlert.objects.filter(resolved=False).count(),
    }
    return Response(data)


@api_view(["GET"])
def latest_alerts(request):
    alerts = OperationalAlert.objects.select_related(
        "voyage",
        "voyage__vessel",
        "telemetry_record",
    ).order_by("-created_at")[:10]
    serializer = OperationalAlertSerializer(alerts, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def alert_summary_by_type(request):
    data = (
        OperationalAlert.objects.values("alert_type")
        .annotate(count=Count("id"))
        .order_by("alert_type")
    )
    alert_type_map = dict(OperationalAlert.ALERT_TYPES)

    counts = [item["count"] for item in data]
    total_counts = sum(counts)

    results = []
    for item in data:
        alert_type = item["alert_type"]
        results.append(
            {
                "alert_type": alert_type,
                "alert_type_display": alert_type_map[alert_type],
                "count": item["count"],
                "percentage": (
                    round(item["count"] / total_counts * 100, 2) if total_counts else 0
                ),
            }
        )
    return Response(results)


@api_view(["GET"])
def alert_count_by_severity(request):
    data = (
        OperationalAlert.objects
        .values("severity")
        .annotate(count=Count("id"))
        .order_by("severity")
    )
    severity_map = dict(OperationalAlert.SEVERITY_CHOICES)
    total_count = sum(item["count"] for item in data)
    
    results = []
    
    for item in data:
        severity = item["severity"]
        results.append({
            "severity": severity,
            "severity_display": severity_map[severity],
            "count": item["count"],
            "percentage": round(
                item["count"] / total_count * 100, 2
            ) if total_count else 0
        })
    return Response(results)


@api_view(["GET"])
def voyage_status_summary(request):
    data = (
        Voyage.objects.values("status").annotate(count=Count("id")).order_by("status")
    )
    return Response(list(data))


@api_view(["GET"])
def alerts_over_time(request):
    data = (
        OperationalAlert.objects
        .annotate(date=TruncDate("detected_at"))
        .values("date")
        .annotate(
            total_alerts=Count("id"),
            critical_alerts=Count(
                "id",
                filter=Q(severity=5)
                )
            )
        .order_by("date")
    )
    return Response(data)

def dashboard_view(request):
    return render(request, "operations/dashboard.html")
