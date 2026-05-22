# operations/management/commands/generate_demo_data.py

from datetime import timedelta
import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from operations.models import Vessel, Voyage, TelemetryRecord
from operations.services.alert_engine import generate_alerts_for_telemetry


class Command(BaseCommand):
    help = "Generate demo vessels, voyages, telemetry records, and alerts."

    def handle(self, *args, **kwargs):
        Vessel.objects.all().delete()

        vessel = Vessel.objects.create(
            name="MV Ocean Pioneer",
            imo_number="IMO9321456",
            vessel_type="Bulk Carrier",
            capacity_tons=75000,
            fuel_capacity_tons=3500,
            status="active",
        )

        voyage = Voyage.objects.create(
            vessel=vessel,
            departure_port="Mombasa",
            destination_port="Rotterdam",
            departure_time=timezone.now() - timedelta(days=5),
            estimated_arrival=timezone.now() + timedelta(days=15),
            distance_nm=6200,
            status="ongoing",
        )

        start_time = timezone.now() - timedelta(hours=24)

        for i in range(48):
            record = TelemetryRecord.objects.create(
                voyage=voyage,
                timestamp=start_time + timedelta(minutes=30 * i),
                latitude=-4.05 + (i * 0.15),
                longitude=39.67 + (i * 0.20),
                speed_knots=random.choice([2.5, 8.5, 12.0, 14.2]),
                fuel_consumption_tons_per_day=random.choice([28, 32, 45, 58, 62]),
                engine_temperature_celsius=random.choice([78, 84, 91, 97, 108]),
                weather_risk_score=random.choice([0.2, 0.4, 0.65, 0.78, 0.92]),
            )

            generate_alerts_for_telemetry(record)

        self.stdout.write(
            self.style.SUCCESS("Demo data and alerts generated successfully.")
        )