from datetime import timedelta

from django.utils import timezone
from django.test import TestCase

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)


class VesselModelTest(TestCase):
    def test_create_vessel(self):
        vessel = Vessel.objects.create(
            name="Mv Test Vessel",
            imo_number="IMO1234567",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )

        self.assertEqual(vessel.name, "Mv Test Vessel")
        self.assertEqual(vessel.imo_number, "IMO1234567")
        self.assertEqual(vessel.vessel_type, "Bulk Carrier")
        self.assertEqual(vessel.capacity_tons, 75000)
        self.assertEqual(vessel.fuel_capacity_tons, 3500)
        self.assertEqual(vessel.status, "active")
        self.assertEqual(str(vessel), "Mv Test Vessel")


class VoyageModelTest(TestCase):
    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="Mv Test Vessel",
            imo_number="IMO1234567",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )

    def test_create_voyage(self):
        departure_time = timezone.now()
        estimated_arrival = departure_time + timedelta(days=10)

        voyage = Voyage.objects.create(
            vessel=self.vessel,
            departure_port="Port A",
            destination_port="Port B",
            departure_time=departure_time,
            estimated_arrival=estimated_arrival,
            distance_nm=2000,
            status="planned",
        )

        self.assertEqual(voyage.vessel, self.vessel)
        self.assertEqual(voyage.departure_port, "Port A")
        self.assertEqual(voyage.destination_port, "Port B")
        self.assertEqual(voyage.departure_time, departure_time)
        self.assertEqual(voyage.estimated_arrival, estimated_arrival)
        self.assertIsNone(voyage.actual_arrival)
        self.assertEqual(voyage.distance_nm, 2000)
        self.assertEqual(voyage.status, "planned")
        self.assertEqual(str(voyage), "Mv Test Vessel: Port A → Port B")
        self.assertIn("Mv Test Vessel", str(voyage))


class TelemetryRecordModelTest(TestCase):
    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="Mv Test Vessel",
            imo_number="IMO1234567",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )

        departure_time = timezone.now()
        estimated_arrival = departure_time + timedelta(days=10)

        self.voyage = Voyage.objects.create(
            vessel=self.vessel,
            departure_port="Port A",
            destination_port="Port B",
            departure_time=departure_time,
            estimated_arrival=estimated_arrival,
            distance_nm=2000,
            status="planned",
        )

    def test_create_telemetry_record(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=37.7749,
            longitude=-122.4194,
            speed_knots=15.5,
            fuel_consumption_tons_per_day=2.5,
            engine_temperature_celsius=85.0,
            weather_risk_score=0.4,
        )

        self.assertEqual(telemetry.voyage, self.voyage)
        self.assertEqual(telemetry.speed_knots, 15.5)
        self.assertEqual(telemetry.engine_temperature_celsius, 85.0)
        self.assertEqual(telemetry.weather_risk_score, 0.4)
        self.assertEqual(telemetry.fuel_consumption_tons_per_day, 2.5)
        self.assertEqual(telemetry.latitude, 37.7749)
        self.assertEqual(telemetry.longitude, -122.4194)


class OperationalAlertModelTest(TestCase):
    def setUp(self):
        self.vessel = Vessel.objects.create(
            name="MV Test Vessel",
            imo_number="IMO1234567",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )

        departure_time = timezone.now()

        self.voyage = Voyage.objects.create(
            vessel=self.vessel,
            departure_port="Mombasa",
            destination_port="Rotterdam",
            departure_time=departure_time,
            estimated_arrival=departure_time + timedelta(days=10),
            distance_nm=6200,
            status="ongoing",
        )

        self.telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=12.5,
            fuel_consumption_tons_per_day=32.0,
            engine_temperature_celsius=108.0,
            weather_risk_score=0.4,
        )

    def test_create_operational_alert(self):
        alert = OperationalAlert.objects.create(
            voyage=self.voyage,
            telemetry_record=self.telemetry,
            alert_type="engine_overheat",
            severity=5,
            message="Engine temperature exceeded safe threshold.",
        )

        self.assertEqual(alert.voyage, self.voyage)
        self.assertEqual(alert.telemetry_record, self.telemetry)
        self.assertEqual(alert.alert_type, "engine_overheat")
        self.assertEqual(alert.get_alert_type_display(), "Engine Overheat")
        self.assertEqual(alert.severity, 5)
        self.assertEqual(alert.get_severity_display(), "Critical")
        self.assertFalse(alert.resolved)

    def test_alert_survives_when_telemetry_is_deleted(self):
        alert = OperationalAlert.objects.create(
            voyage=self.voyage,
            telemetry_record=self.telemetry,
            alert_type="engine_overheat",
            severity=5,
            message="Engine temperature exceeded safe threshold.",
        )

        self.telemetry.delete()

        alert.refresh_from_db()

        self.assertIsNone(alert.telemetry_record)
        self.assertEqual(alert.voyage, self.voyage)
