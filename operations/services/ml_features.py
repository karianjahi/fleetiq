import pandas as pd
from django.db.models import Avg, Count

from operations.models import (
    Vessel,
    TelemetryRecord,
    OperationalAlert,
)


def build_vessel_feature_dataset():
    dataset = []

    for vessel in Vessel.objects.all():

        telemetry = TelemetryRecord.objects.filter(
            voyage__vessel=vessel
        )

        alerts = OperationalAlert.objects.filter(
            voyage__vessel=vessel
        )

        row = {
            "vessel_id": vessel.id,
            "avg_speed": telemetry.aggregate(
                Avg("speed_knots")
            )["speed_knots__avg"],

            "avg_engine_temp": telemetry.aggregate(
                Avg("engine_temperature_celsius")
            )["engine_temperature_celsius__avg"],

            "avg_weather_risk": telemetry.aggregate(
                Avg("weather_risk_score")
            )["weather_risk_score__avg"],

            "avg_fuel": telemetry.aggregate(
                Avg("fuel_consumption_tons_per_day")
            )["fuel_consumption_tons_per_day__avg"],

            "total_alerts": alerts.count(),

            "critical_alerts": alerts.filter(
                severity=5
            ).count(),
        }

        dataset.append(row)

    return pd.DataFrame(dataset)

print(build_vessel_feature_dataset())