# operations/admin.py

from django.contrib import admin
from .models import Vessel, Voyage, TelemetryRecord, OperationalAlert


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    list_display = ("name", "imo_number", "vessel_type", "status")
    search_fields = ("name", "imo_number")
    list_filter = ("status", "vessel_type")


@admin.register(Voyage)
class VoyageAdmin(admin.ModelAdmin):
    list_display = (
        "vessel",
        "departure_port",
        "destination_port",
        "departure_time",
        "estimated_arrival",
        "status",
    )
    list_filter = ("status", "departure_port", "destination_port")
    search_fields = ("vessel__name", "departure_port", "destination_port")


@admin.register(TelemetryRecord)
class TelemetryRecordAdmin(admin.ModelAdmin):
    list_display = (
        "voyage",
        "timestamp",
        "speed_knots",
        "fuel_consumption_tons_per_day",
        "engine_temperature_celsius",
        "weather_risk_score",
    )
    list_filter = ("timestamp",)
    search_fields = ("voyage__vessel__name",)


@admin.register(OperationalAlert)
class OperationalAlertAdmin(admin.ModelAdmin):
    list_display = (
        "voyage",
        "alert_type",
        "severity",
        "resolved",
        "created_at",
    )
    list_filter = ("alert_type", "severity", "resolved")
    search_fields = ("voyage__vessel__name", "message")