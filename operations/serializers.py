from rest_framework import serializers
from .models import Vessel, Voyage, TelemetryRecord, OperationalAlert

class VesselSerializer(serializers.ModelSerializer):
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


    
    
