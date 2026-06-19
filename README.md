# 🚢 FleetIQ

<div align="center">

# AI-Powered Fleet Operations, Predictive Analytics and Maritime Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge\&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?style=for-the-badge\&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge\&logo=postgresql)
![Django REST Framework](https://img.shields.io/badge/DRF-Django%20REST%20Framework-red?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge\&logo=javascript)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-orange?style=for-the-badge\&logo=chartdotjs)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange?style=for-the-badge\&logo=scikitlearn)

</div>

---

# 📖 Overview

FleetIQ is an enterprise-style maritime operations platform that combines operational analytics, telemetry monitoring and machine learning to provide intelligent fleet monitoring and operational decision support.

The system simulates a realistic fleet operations centre capable of monitoring vessel performance, generating operational alerts, assessing fleet health and laying the foundation for predictive analytics using machine learning.

FleetIQ demonstrates:

* Backend software engineering
* Full-stack web development
* REST API development
* Operational analytics
* Dashboard engineering
* Machine learning integration
* Synthetic data generation

---

# ✨ Features

## 🚢 Fleet Management

* Vessel management
* Voyage management
* Fleet operational status tracking
* Vessel health scoring
* Fleet health distribution
* Vessel operational dashboards

---

## 📡 Telemetry Monitoring

FleetIQ generates realistic vessel telemetry including:

* Vessel speed
* Fuel consumption
* Engine temperature
* Weather risk score
* Time-series operational measurements

Telemetry generation supports configurable operational risk profiles.

---

## 🚨 Operational Alert Engine

FleetIQ automatically generates operational alerts from telemetry analysis.

Supported alert types include:

* Delay Risk
* Fuel Anomaly
* Engine Overheat
* Weather Warning
* Speed Anomaly

Alerts drive fleet health assessment and machine learning feature generation.

---

# 🖥️ Application Pages

| Page             | Description                  |
| ---------------- | ---------------------------- |
| `/dashboard/`    | Fleet analytics dashboard    |
| `/vessels/`      | Fleet vessel listing         |
| `/vessels/<id>/` | Vessel operational dashboard |

---

# 🌐 REST APIs

| Endpoint                                      | Description                  |
| --------------------------------------------- | ---------------------------- |
| `/api/dashboard/kpis/`                        | Dashboard KPIs               |
| `/api/alerts/latest/`                         | Latest operational alerts    |
| `/api/alerts/summary-by-type/`                | Alert type distribution      |
| `/api/alerts/summary-by-severity/`            | Alert severity distribution  |
| `/api/alerts/over-time/`                      | Alert evolution over time    |
| `/api/alerts/top-vessels/`                    | Alert distribution by vessel |
| `/api/voyages/status-summary/`                | Voyage status summary        |
| `/api/vessels/`                               | Fleet vessel list            |
| `/api/vessels/<int:pk>/`                      | Vessel details               |
| `/api/vessels/<int:vessel_id>/voyages/`       | Vessel voyages               |
| `/api/vessels/<int:vessel_id>/alerts/`        | Vessel alerts                |
| `/api/vessels/<int:vessel_id>/kpis/`          | Vessel operational KPIs      |
| `/api/vessels/<int:vessel_id>/health-status/` | Vessel health status         |
| `/api/fleet/health-distribution/`             | Fleet health distribution    |

---

# 📊 Interactive Dashboard

FleetIQ provides a modern operational dashboard featuring:

* KPI cards
* Latest operational alerts
* Fleet Health Distribution
* Alert Type Distribution
* Alert Severity Distribution
* Alert Time Evolution
* Alerts by Vessel
* Interactive drill-down navigation
* Responsive frontend

Dashboard charts support drill-down navigation into filtered vessel views.

---

# 🚢 Vessel Operations Portal

Each vessel includes a dedicated operational page containing:

* Vessel information
* Operational KPIs
* Fleet health status
* Voyage history
* Operational alerts
* Alert pagination
* Alert sorting
* Alert filtering

---

# 🤖 Machine Learning

FleetIQ includes an initial machine learning pipeline for vessel risk prediction.

Current capabilities include:

* Feature engineering
* Vessel-level feature dataset generation
* Random Forest model training
* Train/Test split
* Model persistence using Joblib

The ML pipeline forms the foundation for predictive operational analytics.

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

FleetIQ contains a dedicated operational alert engine located in:

```text
operations/services/alert_engine.py
```

The engine analyses telemetry measurements and automatically generates operational alerts.

Example:

```python
if record.engine_temperature_celsius >= 95:
    create_engine_overheat_alert()
```

---

# 📂 Project Structure

```text
fleetiq/

├── core/

├── operations/
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
│   └── commands/
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

## Analytics & Machine Learning

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

* 🚢 Vessels
* 🌍 Voyages
* 📡 Telemetry
* 🚨 Operational Alerts
* 📊 Fleet Health Profiles

Telemetry is generated using configurable Healthy, Watch and High Risk operational profiles, producing realistic datasets for analytics and machine learning experiments.

---

# 📈 Development Progress

## ✅ Completed

* Django backend
* PostgreSQL integration
* Operational models
* Telemetry generation
* Operational alert engine
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
* Vessel risk prediction interface
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

* Fleet map visualisation
* Predictive dashboards
* Fleet comparison analytics
* Operational reporting exports

---

### Infrastructure

* Docker deployment
* Real-time telemetry streaming
* Cloud deployment
* CI/CD pipelines
* Scalable analytics infrastructure

---

# 🧭 Development Philosophy

FleetIQ is intentionally designed as:

* A realistic maritime operations platform
* A backend engineering showcase
* An operational analytics platform
* A machine learning portfolio project
* A foundation for AI-driven maritime decision support systems

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
