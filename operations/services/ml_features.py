import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pathlib import Path
from django.db.models import Avg, Count

from operations.models import (
    Vessel,
    TelemetryRecord,
    OperationalAlert,
)

MODEL_PATH = Path("operations/ml_model/vessel_risk.pkl")
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

def build_vessel_feature_dataset():
    dataset = []

    for vessel in Vessel.objects.all():

        telemetry = TelemetryRecord.objects.filter(voyage__vessel=vessel)

        alerts = OperationalAlert.objects.filter(voyage__vessel=vessel)

        row = {
            "vessel_id": vessel.id,
            "avg_speed": telemetry.aggregate(Avg("speed_knots"))["speed_knots__avg"],
            "avg_engine_temp": telemetry.aggregate(Avg("engine_temperature_celsius"))[
                "engine_temperature_celsius__avg"
            ],
            "avg_weather_risk": telemetry.aggregate(Avg("weather_risk_score"))[
                "weather_risk_score__avg"
            ],
            "avg_fuel": telemetry.aggregate(Avg("fuel_consumption_tons_per_day"))[
                "fuel_consumption_tons_per_day__avg"
            ],
            "total_alerts": alerts.count(),
            "critical_alerts": alerts.filter(severity=5).count(),
        }
        row["high_risk"] = 1 if row["critical_alerts"] >= 10 else 0

        dataset.append(row)

    return pd.DataFrame(dataset)


def train_vessel_risk_model():
    df = build_vessel_feature_dataset()

    X = df.drop(columns=["vessel_id", "high_risk", "critical_alerts"])
    y = df["high_risk"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    joblib.dump(model, MODEL_PATH)
    return {
        "model": model,
        "accuracy": score,
        "training_rows": len(X_train),
        "test_rows": len(X_test),
    }
