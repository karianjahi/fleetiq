from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)

from operations.serializers import (
    VesselSerializer,
    VoyageSerializer,
    TelemetrySerializer,
    OperationalAlertSerializer,
)


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
        
        # Redundant serializers
    def test_vessel_serializer(self):
        serializer = VesselSerializer(self.vessel)

        self.assertEqual(
            serializer.data["name"],
            "MV Test Vessel"
        )

    def test_voyage_serializer(self):
        serializer = VoyageSerializer(self.voyage)

        self.assertEqual(
            serializer.data["departure_port"],
            "Mombasa"
        )

        self.assertEqual(
            serializer.data["destination_port"],
            "Rotterdam"
        )

    def test_telemetry_serializer(self):
        serializer = TelemetrySerializer(self.telemetry)

        self.assertEqual(
            serializer.data["speed_knots"],
            12.0
        )

        self.assertEqual(
            serializer.data["engine_temperature_celsius"],
            108.0
        )



