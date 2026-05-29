from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)

from operations.serializers import OperationalAlertSerializer

class OperationAlertSerializerTest(TestCase):
    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="MV Test Vessel",
            imo_number="IMO1234567",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )
        self.voyage = Voyage.objects.create(
            vessel=self.vessel,
            departure_port="Mombasa",
            destination_port="Rotterdam",
            departure_time=timezone.now(),
            estimated_arrival=timezone.now() + timedelta(days=10),
            distance_nm=6200,
            status="ongoing",
        )
        self.telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=12,
            fuel_consumption_tons_per_day=40,
            engine_temperature_celsius=108,
            weather_risk_score=0.92,
        )

        self.alert = OperationalAlert.objects.create(
            voyage=self.voyage,
            telemetry_record=self.telemetry,
            alert_type="engine_overheat",
            severity=5,
            message="Engine temperature exceeded safe threshold.",
        )
    
    def test_operational_alert_serializer_output(self):
        serializer = OperationalAlertSerializer(self.alert)
        data = serializer.data
        self.assertEqual(data["alert_type"], "engine_overheat")
        self.assertEqual(data["alert_type_display"], "Engine Overheat")
        self.assertEqual(data["severity"], 5)
        self.assertEqual(data["severity_display"], "Critical")
        self.assertEqual(data["vessel_name"], "MV Test Vessel")
        self.assertEqual(
            data["message"],
            "Engine temperature exceeded safe threshold."
        )
        