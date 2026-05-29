from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)

from operations.services.alert_engine import (
    generate_alerts_for_telemetry,
)


class AlertEngineTest(TestCase):
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

    def test_engine_overheat_alert_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=12,
            fuel_consumption_tons_per_day=40,
            engine_temperature_celsius=110,
            weather_risk_score=0.2,
        )

        alerts = generate_alerts_for_telemetry(telemetry)
        self.assertEqual(len(alerts), 1)

        alert = alerts[0]
        self.assertEqual(alert.alert_type, "engine_overheat")
        self.assertEqual(alert.severity, 5)

    def test_weather_warning_alert_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=12,
            fuel_consumption_tons_per_day=40,
            engine_temperature_celsius=80,
            weather_risk_score=0.92,
        )
        alerts = generate_alerts_for_telemetry(telemetry)
        self.assertEqual(len(alerts), 1)

        alert = alerts[0]
        self.assertEqual(alert.alert_type, "weather_warning")
        self.assertEqual(alert.severity, 5)

    def test_delay_risk_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=1.5,
            fuel_consumption_tons_per_day=40,
            engine_temperature_celsius=80,
            weather_risk_score=0.3,
        )
        alerts = generate_alerts_for_telemetry(telemetry)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].alert_type, "delay_risk")

    def test_fuel_alert_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=9,
            fuel_consumption_tons_per_day=60,
            engine_temperature_celsius=80,
            weather_risk_score=0.3,
        )

        alerts = generate_alerts_for_telemetry(telemetry)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].alert_type, "fuel_anomaly")
        self.assertEqual(alerts[0].severity, 4)

    def test_multiple_alerts_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=1.5,
            fuel_consumption_tons_per_day=55,
            engine_temperature_celsius=120,
            weather_risk_score=0.95,
        )

        alerts = generate_alerts_for_telemetry(telemetry)
        self.assertEqual(len(alerts), 3)

        alert_types = [item.alert_type for item in alerts]
        self.assertIn("engine_overheat", alert_types)
        self.assertIn("weather_warning", alert_types)
        self.assertIn("delay_risk", alert_types)
        self.assertNotIn("fuel_anomaly", alert_types)

    def test_no_alert_created(self):
        telemetry = TelemetryRecord.objects.create(
            voyage=self.voyage,
            timestamp=timezone.now(),
            latitude=-4.05,
            longitude=39.67,
            speed_knots=3.5,
            fuel_consumption_tons_per_day=50,
            engine_temperature_celsius=75,
            weather_risk_score=0.65,
        )
        
        alerts = generate_alerts_for_telemetry(telemetry)
        
        self.assertEqual(len(alerts), 0)
        self.assertEqual(OperationalAlert.objects.count(), 0)
