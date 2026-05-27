# 🚢 FleetIQ

<div align="center">

## AI-Powered Fleet Operations and Maritime Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-darkgreen?style=for-the-badge&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![DRF](https://img.shields.io/badge/DRF-Django%20REST%20Framework-red?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-orange?style=for-the-badge&logo=chartdotjs)

</div>

---

# 📖 Overview

FleetIQ is an enterprise-style maritime operations and analytics platform designed to monitor vessel activity, analyse telemetry data, detect operational anomalies, and support intelligent operational decision-making.

The project simulates a realistic operational intelligence environment similar to systems used in:

- 🚢 Shipping operations
- 📦 Logistics platforms
- 🏭 Industrial monitoring systems
- 📊 Operational intelligence platforms
- 🤖 AI-driven analytics environments

---

# ✨ Current Features

## 🚢 Fleet Management

- Vessel management
- Voyage management
- Operational status tracking

---

## 📡 Telemetry Monitoring

FleetIQ currently supports:

- Time-series telemetry generation
- Vessel operational measurements
- Engine temperature monitoring
- Fuel consumption tracking
- Weather risk monitoring
- Vessel speed tracking

---

## 🚨 Operational Alert Engine

Automatic operational alert generation based on telemetry analysis.

### Current Alert Types

- ⚠️ Delay Risk
- ⛽ Fuel Anomaly
- 🔥 Engine Overheat
- 🌩️ Weather Warning
- 🧭 Route Deviation
- 📉 Speed Anomaly

---

## 🌐 API Layer

REST APIs built with Django REST Framework.

### Current APIs

| API | Description |
|---|---|
| `/api/dashboard/kpis/` | Dashboard summary KPIs |
| `/api/alerts/latest/` | Latest operational alerts |
| `/api/alerts/summary-by-type/` | Alert distribution |
| `/api/alerts/summary-by-severity/` | Severity distribution |
| `/api/voyages/status-summary/` | Voyage status analytics |

---

## 📊 Dashboard

Current dashboard capabilities:

- KPI cards
- Latest alerts table
- API-driven frontend
- Responsive layout
- Separate frontend concerns

---

# 🏗️ Current System Architecture

```text
Vessel
   ↓
Voyage
   ↓
TelemetryRecord
   ↓
OperationalAlert
   ↓
Dashboard APIs
   ↓
Frontend Dashboard
```

---

# 🧠 Core Models

## 🚢 Vessel

Represents a physical ship within the fleet.

### Example Fields

- Name
- IMO number
- Vessel type
- Capacity
- Fuel capacity
- Operational status

---

## 🌍 Voyage

Represents a vessel journey between ports.

### Example Fields

- Departure port
- Destination port
- Departure time
- Estimated arrival
- Voyage status
- Distance in nautical miles

---

## 📡 TelemetryRecord

Stores time-series operational telemetry data.

### Example Fields

- Timestamp
- Latitude
- Longitude
- Speed in knots
- Fuel consumption
- Engine temperature
- Weather risk score

---

## 🚨 OperationalAlert

Stores operational warnings generated automatically from telemetry analysis.

### Key Features

- Linked to voyages
- Optional telemetry traceability
- Severity levels
- Human-readable alert types
- Auto-generated timestamps

---

# ⚙️ Alert Engine

FleetIQ contains a dedicated operational alert engine located in:

```text
operations/services/alert_engine.py
```

The engine analyses telemetry records and generates operational alerts automatically.

---

## 🔥 Example Rule

```python
if record.engine_temperature_celsius >= 95:
    create engine_overheat alert
```

---

# 📂 Project Structure

```text
fleetiq/
│
├── core/
│
├── operations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   │
│   ├── services/
│   │   └── alert_engine.py
│   │
│   ├── management/
│   │   └── commands/
│   │
│   ├── templates/
│   └── static/
│
├── requirements.txt
├── manage.py
└── .env
```

---

# 🛠️ Technology Stack

## 🔙 Backend

- Python
- Django
- Django REST Framework
- PostgreSQL

---

## 📊 Analytics & Data

- pandas
- scikit-learn

---

## 🎨 Frontend

- HTML
- CSS
- JavaScript
- Chart.js

---

# 🚀 Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone <repository_url>
cd fleetiq
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Linux/macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

---

## 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
DB_NAME=fleetiq_db
DB_USER=fleetiq_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

## 7️⃣ Run Development Server

```bash
python manage.py runserver
```

---

# 🧪 Generate Demo Data

FleetIQ currently includes demo data generation commands.

```bash
python manage.py generate_demo_data
```

This creates:

- 🚢 Demo vessels
- 🌍 Demo voyages
- 📡 Telemetry records
- 🚨 Operational alerts

---

# 📈 Current Development Progress

## ✅ Completed

- Django project setup
- PostgreSQL integration
- Core operational models
- Telemetry generation
- Alert engine
- REST APIs
- Dashboard foundation

---

## 🚧 In Progress

- Dashboard visualisations
- Chart integrations
- Large-scale telemetry generation
- Advanced analytics

---

## 🔮 Planned Future Enhancements

### 🤖 Machine Learning

- Predictive maintenance
- ETA prediction
- Fuel anomaly prediction
- Operational risk scoring
- Vessel health scoring

---

### 🧠 AI Features

- AI-generated operational summaries
- Intelligent anomaly explanations
- Natural language operational queries
- Operational recommendation systems

---

### 📊 Dashboard Expansion

- Interactive charts
- Telemetry visualisations
- Vessel detail pages
- Real-time monitoring

---

### ⚡ Infrastructure Improvements

- Real-time telemetry streaming
- Scalable analytics pipelines
- Production deployment
- Docker support
- Cloud hosting

---

# 🧭 Development Philosophy

FleetIQ is intentionally being developed as:

- A realistic operational analytics platform
- A scalable backend architecture project
- A demonstration of software engineering skills
- A foundation for AI-driven operational intelligence systems

---

# 👨‍💻 Author

## Joseph Karianjahi Njeri

- Data Science
- Full-Stack Development
- Operational Analytics
- AI & Machine Learning

---

<div align="center">

# 🚢 FleetIQ

### Intelligent Fleet Operations and Maritime Analytics

</div>