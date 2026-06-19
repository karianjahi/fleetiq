from rest_framework import serializers
from .models import Vessel, Voyage, TelemetryRecord, OperationalAlert
from .services import services_utils

class VesselSerializer(serializers.ModelSerializer):
    health_status = serializers.SerializerMethodField()
    def get_health_status(self, vessel):
        alerts = OperationalAlert.objects.filter(
            voyage__vessel = vessel
        )
        total_alerts = alerts.count()
        critical_alerts = alerts.filter(severity=5).count()
        
        return services_utils.determine_risk_profile(
            critical_alerts,
            total_alerts,
        )
    class Meta:
        model = Vessel
        fields = "__all__"
        

class VoyageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voyage
        fields = "__all__"

class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryRecord
        fields = "__all__"
        
class OperationalAlertSerializer(serializers.ModelSerializer):
    alert_type_display = serializers.CharField(
        source="get_alert_type_display",
        read_only=True
    )
    
    severity_display = serializers.CharField(
        source="get_severity_display",
        read_only=True
    )
    
    vessel_name = serializers.CharField(
    source="voyage.vessel.name",
    read_only=True
    )
    
    class Meta:
        model = OperationalAlert
        fields = "__all__"


    
    
