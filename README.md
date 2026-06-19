# 🚢 FleetIQ

<div align="center">

# AI-Powered Fleet Operations, Predictive Analytics and Maritime Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?style=for-the-badge\&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge\&logo=postgresql)
![Django REST Framework](https://img.shields.io/badge/DRF-Django%20REST%20Framework-red?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge\&logo=javascript)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-orange?style=for-the-badge\&logo=chartdotjs)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange?style=for-the-badge\&logo=scikitlearn)

</div>

---

# 📖 Overview

FleetIQ is an enterprise-style maritime operations platform that combines operational analytics, telemetry monitoring and machine learning to provide intelligent fleet monitoring and decision support.

The system simulates a realistic maritime operations centre capable of monitoring fleet performance, generating operational alerts, visualising fleet health and building predictive analytics pipelines for vessel risk assessment.

FleetIQ demonstrates:

* Backend software engineering
* REST API development
* Operational analytics
* Dashboard development
* Machine learning integration
* Synthetic operational data generation

---

# ✨ Features

## 🚢 Fleet Management

* Vessel management
* Voyage management
* Operational status tracking
* Fleet health scoring
* Vessel operational dashboards
* Fleet-wide analytics

---

## 📡 Telemetry Monitoring

FleetIQ generates realistic vessel telemetry including:

* Vessel speed
* Fuel consumption
* Engine temperature
* Weather risk score
* Time-series operational measurements

Telemetry generation is configurable through operational risk profiles.

---

## 🚨 Operational Alert Engine

FleetIQ automatically generates operational alerts based on telemetry analysis.

Supported alert types include:

* Delay Risk
* Fuel Anomaly
* Engine Overheat
* Weather Warning
* Route Deviation
* Speed Anomaly

Operational alerts drive fleet health assessment and machine learning features.

---

# 📊 Interactive Dashboard

FleetIQ includes a fully interactive analytics dashboard featuring:

* KPI Cards
* Latest Operational Alerts
* Fleet Health Distribution
* Alert Type Distribution
* Alert Severity Distribution
* Alert Time Evolution
* Alerts by Vessel
* Interactive chart drill-down
* Responsive design

Charts can be clicked to navigate directly into filtered operational views.

---

# 🚢 Vessel Operations Portal

Each vessel has a dedicated operational page containing:

* Vessel information
* Operational KPIs
* Fleet health status
* Voyage history
* Operational alerts
* Alert pagination
* Alert sorting
* Alert filtering

---

# 🌐 REST APIs

FleetIQ exposes operational data through Django REST Framework.

| Endpoint                           | Description                 |
| ---------------------------------- | --------------------------- |
| `/api/dashboard/kpis/`             | Dashboard KPIs              |
| `/api/alerts/latest/`              | Latest operational alerts   |
| `/api/alerts/summary-by-type/`     | Alert distribution          |
| `/api/alerts/summary-by-severity/` | Alert severity distribution |
| `/api/alerts/over-time/`           | Alert evolution over time   |
| `/api/alerts/top-vessels/`         | Alerts by vessel            |
| `/api/fleet/health-distribution/`  | Fleet health distribution   |
| `/api/vessels/`                    | Fleet vessel list           |
| `/api/vessels/<id>/`               | Vessel details              |
| `/api/vessels/<id>/voyages/`       | Vessel voyages              |
| `/api/vessels/<id>/alerts/`        | Vessel alerts               |
| `/api/vessels/<id>/kpis/`          | Vessel KPIs                 |

---

# 🤖 Machine Learning

FleetIQ now includes an initial machine learning pipeline.

Current capabilities:

* Feature engineering
* Vessel-level feature dataset generation
* Random Forest classification
* Train/Test splitting
* Model persistence using Joblib

The ML pipeline forms the basis for predictive operational analytics and future AI-powered risk prediction.

---

# 🏗️ System Architecture

```text
Vessel
    ↓
Voyage
    ↓
TelemetryRecord
    ↓
OperationalAlert
    ↓
Feature Engineering
    ↓
Machine Learning
    ↓
REST APIs
    ↓
Interactive Dashboard
```

---

# 🧠 Core Models

## Vessel

* Name
* IMO Number
* Vessel Type
* Capacity
* Fuel Capacity
* Operational Status

---

## Voyage

* Departure Port
* Destination Port
* Departure Time
* Estimated Arrival
* Voyage Status

---

## TelemetryRecord

* Timestamp
* Latitude
* Longitude
* Speed
* Fuel Consumption
* Engine Temperature
* Weather Risk Score

---

## OperationalAlert

* Alert Type
* Severity
* Message
* Timestamp
* Voyage
* Telemetry Traceability

---

# ⚙️ Operational Alert Engine

Operational alerts are generated automatically from telemetry analysis.

Example:

```python
if engine_temperature >= 95:
    generate_engine_overheat_alert()
```

The alert engine resides in:

```text
operations/services/alert_engine.py
```

---

# 📂 Project Structure

```text
fleetiq/

core/

operations/
│
├── models.py
├── serializers.py
├── views.py
├── urls.py
│
├── services/
│   ├── alert_engine.py
│   ├── services_utils.py
│   └── ml_features.py
│
├── management/
│
├── templates/
└── static/

manage.py
requirements.txt
```

---

# 🛠️ Technology Stack

## Backend

* Python
* Django
* Django REST Framework
* PostgreSQL

---

## Data & Machine Learning

* pandas
* NumPy
* scikit-learn

---

## Frontend

* HTML
* CSS
* JavaScript
* Chart.js

---

# 🚀 Setup

```bash
git clone https://github.com/karianjahi/fleetiq.git

cd fleetiq

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

---

# 🧪 Demo Data Generation

Generate synthetic operational data:

```bash
python manage.py generate_demo_data
```

Generated data includes:

* Vessels
* Voyages
* Telemetry
* Operational Alerts
* Fleet Health Profiles

Telemetry is generated from configurable Healthy, Watch and High Risk operational profiles, producing realistic operational behaviour suitable for dashboard analytics and machine learning experiments.

---

# 📈 Development Progress

## ✅ Completed

* Django backend
* PostgreSQL integration
* Operational models
* Telemetry generation
* Alert engine
* REST APIs
* Interactive dashboard
* Fleet health scoring
* Vessel detail pages
* Alert pagination
* Alert sorting
* Alert filtering
* Interactive chart drill-down
* Machine learning feature engineering
* Random Forest training pipeline

---

## 🚧 In Progress

* Model evaluation
* Prediction APIs
* Vessel risk prediction UI
* Dashboard AI integration

---

## 🔮 Planned Features

### Machine Learning

* Predictive maintenance
* Vessel risk prediction
* ETA prediction
* Fuel anomaly prediction
* Remaining useful life estimation

---

### AI

* AI operational summaries
* Intelligent anomaly explanations
* Natural language fleet queries
* Operational recommendations

---

### Dashboard

* Fleet map
* Predictive dashboards
* Fleet comparison analytics
* Operational reporting

---

### Infrastructure

* Docker
* Real-time telemetry streaming
* Cloud deployment
* CI/CD
* Scalable analytics pipelines

---

# 👨‍💻 Author

## Dr. rer. nat. Joseph Karianjahi Njeri

* Data Science
* Backend Engineering
* Full-Stack Development
* Operational Analytics
* Machine Learning
* AI Systems

---

<div align="center">

# 🚢 FleetIQ

### Intelligent Fleet Operations, Predictive Analytics and Maritime Intelligence

</div>
