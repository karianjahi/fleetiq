from django.shortcuts import render

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
