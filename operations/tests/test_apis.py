from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)

class DashBoardAPITest(APITestCase):
    def setUp(self):
        self.vessel  =  Vessel.objects.create(
            name = "MV Test Vessel",
            imo_number = "IMO1234567",
            vessel_type = "Bulk Carrier",
            capacity_tons = 75000,
            fuel_capacity_tons = 3500,
            status = "active",
        )
        
        self.voyage  =  Voyage.objects.create(
            vessel = self.vessel,
            departure_port = "Mombasa",
            destination_port = "Rotterdam",
            departure_time = timezone.now(),
            estimated_arrival = timezone.now() + timedelta(days = 10),
            distance_nm = 6200,
            status = "ongoing",
        )
        
        self.telemetry  =  TelemetryRecord.objects.create(
            voyage = self.voyage,
            timestamp = timezone.now(),
            latitude = -4.05,
            longitude = 39.67,
            speed_knots = 12,
            fuel_consumption_tons_per_day = 40,
            engine_temperature_celsius = 108,
            weather_risk_score = 0.92,
        )
        
        self.alert = OperationalAlert.objects.create(
            voyage = self.voyage,
            telemetry_record = self.telemetry,
            alert_type = "engine_overheat",
            severity = 5,
            message = "Engine temperature exceeded safe threshold.",            
        )
        
    def test_dashboard_kpis_api(self):
        response = self.client.get("/api/dashboard/kpis/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["total_vessels"], 1)
        self.assertEqual(data["active_vessels"], 1)
        self.assertEqual(data["total_voyages"], 1)
        self.assertEqual(data["ongoing_voyages"], 1)
        self.assertEqual(data["telemetry_records"], 1)
        self.assertEqual(data["total_alerts"], 1)
        self.assertEqual(data["critical_alerts"], 1)
    
    def test_latest_alert_api(self):
        response = self.client.get("/api/alerts/latest/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["alert_type"], "engine_overheat")
        self.assertEqual(data[0]["alert_type_display"], "Engine Overheat")
        self.assertEqual(data[0]["severity"], 5)
        self.assertEqual(data[0]["severity_display"], "Critical")
        self.assertEqual(data[0]["vessel_name"], "MV Test Vessel")
        self.assertIn("ngine", data[0]["message"])
    
    def test_alert_summary_by_type(self):
        response = self.client.get("/api/alerts/summary-by-type/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data[0]["alert_type"], "engine_overheat")
        self.assertEqual(data[0]["count"], 1)
    
    def test_alert_count_by_severity(self):
        response = self.client.get("/api/alerts/summary-by-severity/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["alert_type"], "engine_overheat")
        self.assertEqual(data[0]["severity"], 5)
        self.assertIn("ngine", data[0]["message"])
        self.assertEqual(data[0]["count"], 1)
    
    def test_voyage_status_summary(self):
        response = self.client.get("/api/voyages/status-summary/")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["status"], "ongoing")
        self.assertEqual(data[0]["count"], 1)
        
        