from operations.models import OperationalAlert

def generate_alerts_for_telemetry(record):
    """
    Analyse one telemetry record and create operational alerts
    when defined thresholds are exceeded.
    """
    alerts = []
    
   # 1. Engine overheat
    if record.engine_temperature_celsius >= 95:
        alerts.append(
            OperationalAlert.objects.create(
                voyage=record.voyage,
                telemetry_record=record,
                alert_type="engine_overheat",
                severity=5 if record.engine_temperature_celsius >= 105 else 4,
                message=(
                    f"Engine temperature reached "
                    f"{record.engine_temperature_celsius}°C."
                ),
            )
        )

 # 2. Weather warning
    if record.weather_risk_score >= 0.75:
        alerts.append(
            OperationalAlert.objects.create(
                voyage=record.voyage,
                telemetry_record=record,
                alert_type="weather_warning",
                severity=5 if record.weather_risk_score >= 0.9 else 4,
                message=(
                    f"High weather risk detected "
                    f"with score {record.weather_risk_score}."
                ),
            )
        )

  # 3. Speed anomaly / delay risk
    if record.speed_knots <= 3:
        alerts.append(
            OperationalAlert.objects.create(
                voyage=record.voyage,
                telemetry_record=record,
                alert_type="delay_risk",
                severity=4,
                message=(
                    f"Low vessel speed detected: "
                    f"{record.speed_knots} knots."
                ),
            )
        )

# 4. Fuel anomaly
    if (
        record.speed_knots > 8
        and record.fuel_consumption_tons_per_day >= 55
    ):
        alerts.append(
            OperationalAlert.objects.create(
                voyage=record.voyage,
                telemetry_record=record,
                alert_type="fuel_anomaly",
                severity=4,
                message=(
                    f"High fuel consumption detected: "
                    f"{record.fuel_consumption_tons_per_day} tons/day "
                    f"at {record.speed_knots} knots."
                ),
            )
        )
