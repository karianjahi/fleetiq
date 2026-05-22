from django.db import models


class Vessel(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("maintenance", "Maintenance"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=100)
    imo_number = models.CharField(max_length=50, unique=True)
    vessel_type = models.CharField(max_length=100)

    capacity_tons = models.FloatField()
    fuel_capacity = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Voyage(models.Model):
    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("delayed", "Delayed"),
    ]

    vessel = models.ForeignKey(Vessel, on_delete=models.CASCADE, related_name="voyages")

    departure_port = models.CharField(max_length=100)
    destination_port = models.CharField(max_length=100)

    departure_time = models.DateTimeField()
    estimated_arrival = models.DateTimeField()

    actual_arrival = models.DateTimeField(null=True, blank=True)

    distance_nm = models.FloatField(help_text="Distance in nautical miles")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ongoing")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vessel.name}: {self.departure_port} → {self.destination_port}"


class TelemetryRecord(models.Model):
    voyage = models.ForeignKey(
        Voyage, on_delete=models.CASCADE, related_name="telemetry_records"
    )

    timestamp = models.DateTimeField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    speed_knots = models.FloatField()
    fuel_consumption = models.FloatField()

    engine_temperature = models.FloatField()

    weather_risk_score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.voyage.vessel.name} @ {self.timestamp}"


class OperationalAlert(models.Model):
    ALERT_TYPES = [
        ("delay_risk", "Delay Risk"),
        ("fuel_anomaly", "Fuel Anomaly"),
        ("engine_overheat", "Engine Overheat"),
        ("weather_warning", "Weather Warning"),
        ("route_deviation", "Route Deviation"),
        ("speed_anomaly", "Speed Anomaly"),
    ]
    voyage = models.ForeignKey(Voyage, on_delete=models.CASCADE, related_name="alerts")

    telemetry_record = models.ForeignKey(
        TelemetryRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    alert_type = models.CharField(max_length=50)
    severity = models.IntegerField(default=1)
    message = models.TextField()
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
