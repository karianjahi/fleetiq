# operations/models.py

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Vessel(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("maintenance", "Maintenance"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=100)
    imo_number = models.CharField(max_length=20, unique=True)
    vessel_type = models.CharField(max_length=100)

    capacity_tons = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    fuel_capacity_tons = models.FloatField(
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Voyage(models.Model):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("delayed", "Delayed"),
        ("cancelled", "Cancelled"),
    ]

    vessel = models.ForeignKey(
        Vessel,
        on_delete=models.CASCADE,
        related_name="voyages",
    )

    departure_port = models.CharField(max_length=100)
    destination_port = models.CharField(max_length=100)

    departure_time = models.DateTimeField()
    estimated_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(
        null=True,
        blank=True,
    )

    distance_nm = models.FloatField(
        validators=[MinValueValidator(0)]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planned",
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-departure_time"]

    def __str__(self):
        return (
            f"{self.vessel.name}: "
            f"{self.departure_port} → {self.destination_port}"
        )


class TelemetryRecord(models.Model):
    voyage = models.ForeignKey(
        Voyage,
        on_delete=models.CASCADE,
        related_name="telemetry_records",
    )

    timestamp = models.DateTimeField(db_index=True)

    latitude = models.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    longitude = models.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
    )

    speed_knots = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    fuel_consumption_tons_per_day = models.FloatField(
        validators=[MinValueValidator(0)]
    )
    engine_temperature_celsius = models.FloatField()

    weather_risk_score = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["voyage", "timestamp"]),
        ]

    def __str__(self):
        return (
            f"{self.voyage.vessel.name} telemetry "
            f"at {self.timestamp}"
        )


class OperationalAlert(models.Model):
    ALERT_TYPES = [
        ("delay_risk", "Delay Risk"),
        ("fuel_anomaly", "Fuel Anomaly"),
        ("engine_overheat", "Engine Overheat"),
        ("weather_warning", "Weather Warning"),
        ("speed_anomaly", "Speed Anomaly"),
    ]

    SEVERITY_CHOICES = [
        (1, "Info"),
        (2, "Low"),
        (3, "Medium"),
        (4, "High"),
        (5, "Critical"),
    ]

    voyage = models.ForeignKey(
        Voyage,
        on_delete=models.CASCADE,
        related_name="alerts",
    )

    telemetry_record = models.ForeignKey(
        TelemetryRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alerts",
    )

    alert_type = models.CharField(
        max_length=50,
        choices=ALERT_TYPES,
        db_index=True,
    )

    severity = models.IntegerField(
        choices=SEVERITY_CHOICES,
        default=3,
        db_index=True,
    )

    message = models.TextField()
    resolved = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    detected_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                fields=["voyage", "resolved", "-created_at"]
            ),
            models.Index(
                fields=["alert_type", "severity"]
            ),
        ]

    def __str__(self):
        return (
            f"{self.get_alert_type_display()} - "
            f"{self.voyage.vessel.name}"
        )

