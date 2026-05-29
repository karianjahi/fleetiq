from unittest.mock import patch
import pandas as pd

from django.core.management import call_command
from django.test import TestCase

from operations.models import (
    Vessel,
    Voyage,
    TelemetryRecord,
    OperationalAlert,
)


class GenerateDemoDataCommandTest(TestCase):

    @patch("operations.management.commands.generate_demo_data.pd.read_csv")
    def test_generate_demo_data_command_creates_records(self, mock_read_csv):
        test_df = pd.DataFrame(
            [
                {
                    "name": "MV Test Vessel 1",
                    "imo_number": "IMO1234567",
                    "vessel_type": "Bulk Carrier",
                    "capacity_tons": 75000,
                    "fuel_capacity_tons": 3500,
                    "status": "active",
                },
                {
                    "name": "MV Test Vessel 2",
                    "imo_number": "IMO7654321",
                    "vessel_type": "Container Ship",
                    "capacity_tons": 68000,
                    "fuel_capacity_tons": 3200,
                    "status": "active",
                },
                {
                    "name": "MV Test Vessel 3",
                    "imo_number": "IMO1111111",
                    "vessel_type": "Tanker",
                    "capacity_tons": 85000,
                    "fuel_capacity_tons": 4200,
                    "status": "maintenance",
                },
                {
                    "name": "MV Test Vessel 4",
                    "imo_number": "IMO2222222",
                    "vessel_type": "Bulk Carrier",
                    "capacity_tons": 73000,
                    "fuel_capacity_tons": 3600,
                    "status": "active",
                },
                {
                    "name": "MV Test Vessel 5",
                    "imo_number": "IMO3333333",
                    "vessel_type": "Container Ship",
                    "capacity_tons": 66000,
                    "fuel_capacity_tons": 3100,
                    "status": "inactive",
                },
            ]
        )

        mock_read_csv.return_value = test_df
        call_command("generate_demo_data")
        
        self.assertEqual(Vessel.objects.count(), 5)
        self.assertGreater(Voyage.objects.count(), 0)
        self.assertEqual(
            TelemetryRecord.objects.count(),
            Voyage.objects.count() * 48
        )
        self.assertGreater(
            OperationalAlert.objects.count(),
            0
        )
    
    @patch("operations.management.commands.generate_demo_data.pd.read_csv")
    def test_departure_and_destination_ports_are_different(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame([
            {
                "name": "MV Test Vessel",
                "imo_number": "IMO1234567",
                "vessel_type": "Bulk Carrier",
                "capacity_tons": 75000,
                "fuel_capacity_tons": 3500,
                "status": "active",
            }
        ])

        call_command("generate_demo_data")

        voyages = Voyage.objects.all()

        for voyage in voyages:
            self.assertNotEqual(
                voyage.departure_port,
                voyage.destination_port
            )
        
    @patch("operations.management.commands.generate_demo_data.pd.read_csv")
    def test_command_clears_existing_vessels_before_generating_new_data(self, mock_read_csv):
        Vessel.objects.create(
            name="Old Vessel",
            imo_number="IMO9999999",
            vessel_type="Bulk Carrier",
            capacity_tons=70000,
            fuel_capacity_tons=3000,
            status="active",
        )

        mock_read_csv.return_value = pd.DataFrame([
            {
                "name": "MV New Vessel",
                "imo_number": "IMO1234567",
                "vessel_type": "Bulk Carrier",
                "capacity_tons": 75000,
                "fuel_capacity_tons": 3500,
                "status": "active",
            }
        ])

        call_command("generate_demo_data")

        self.assertFalse(
            Vessel.objects.filter(name="Old Vessel").exists()
        )

        self.assertTrue(
            Vessel.objects.filter(name="MV New Vessel").exists()
        )