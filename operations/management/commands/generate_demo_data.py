# operations/management/commands/generate_demo_data.py

from datetime import timedelta
import random
from pathlib import Path

import pandas as pd

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from operations.models import Vessel, Voyage, TelemetryRecord
from operations.services.alert_engine import generate_alerts_for_telemetry

FILEPATH = Path(settings.BASE_DIR)

NO_OF_VESSELS = 15

PORTS = [
    "Mombasa",
    "Rotterdam",
    "Singapore",
    "Shanghai",
    "Dubai",
    "Hamburg",
    "Los Angeles",
    "Cape Town",
    "Hong Kong",
    "New York",
]

DISTANCES = [18201, 9842, 12499, 19422, 7921, 11941, 5619]

STATUS_CHOICES = [
    "planned",
    "ongoing",
    "completed",
    "delayed",
    "cancelled",
]

VOYAGES = [3, 2, 5, 6, 1]
TELEMETRY_RECORDS = 48


class Command(BaseCommand):
    help = "Generate demo vessels, voyages, telemetry records, and alerts."

    def handle(self, *args, **kwargs):
        vessel_df = pd.read_csv(
            FILEPATH / "operations" / "management" / "commands" / "vessels.csv"
        )

        subdf = vessel_df.sample(frac=1).head(NO_OF_VESSELS)

        Vessel.objects.all().delete()

        for _, row in subdf.iterrows():
            vessel = Vessel.objects.create(
                name=row["name"],
                imo_number=row["imo_number"],
                vessel_type=row["vessel_type"],
                capacity_tons=row["capacity_tons"],
                fuel_capacity_tons=row["fuel_capacity_tons"],
                status=row["status"],
            )

            n_voyages = random.choice(VOYAGES)
            for voyage_index in range(n_voyages):
                departure_port, destination_port = random.sample(PORTS, 2)
                departure_time = timezone.now() - timedelta(days=random.randint(5, 90))
                estimated_arrival = departure_time + timedelta(days=random.randint(7, 30))

                voyage = Voyage.objects.create(
                    vessel=vessel,
                    departure_port=departure_port,
                    destination_port=destination_port,
                    departure_time=departure_time,
                    estimated_arrival=estimated_arrival,
                    distance_nm=random.choice(DISTANCES),
                    status=random.choice(STATUS_CHOICES),
                )

                start_time = departure_time
                voyage_duration = estimated_arrival - departure_time
                telemetry_interval = voyage_duration / TELEMETRY_RECORDS

                for telemetry_index in range(TELEMETRY_RECORDS):
                    record = TelemetryRecord.objects.create(
                        voyage=voyage,
                        timestamp=start_time + (telemetry_interval * telemetry_index),
                        latitude=-4.05 + (telemetry_index * 0.15),
                        longitude=39.67 + (telemetry_index * 0.20),
                        speed_knots=random.choice([2.5, 8.5, 12.0, 14.2]),
                        fuel_consumption_tons_per_day=random.choice(
                            [28, 32, 45, 58, 62]
                        ),
                        engine_temperature_celsius=random.choice([78, 84, 91, 97, 108]),
                        weather_risk_score=random.choice([0.2, 0.4, 0.65, 0.78, 0.92]),
                    )

                    generate_alerts_for_telemetry(record)

                # self.stdout.write(
                #     f"Wrote {TELEMETRY_RECORDS} telemetry records for "
                #     f"{vessel.name}: {voyage.departure_port} to {voyage.destination_port}"
                # )

        self.stdout.write(
            self.style.SUCCESS("Demo data and alerts generated successfully.")
        )
