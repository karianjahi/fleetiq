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
            status="active",)
        
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
            status="active",)

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
            status="planned",)

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
        

