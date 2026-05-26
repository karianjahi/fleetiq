const totalVesselsEl = document.getElementById("total-vessels");
const activeVesselsEl = document.getElementById("active-vessels");
const totalVoyagesEl = document.getElementById("total-voyages");
const telemetryRecordsEl = document.getElementById("telemetry-records");
const totalAlertsEl = document.getElementById("total-alerts");
const criticalAlertsEl = document.getElementById("critical-alerts");
const unresolvedAlerts = document.getElementById("unresolved-alerts");
const ongoingVoyagesEl = document.getElementById("ongoing-voyages");
const delayRiskFreqEl = document.getElementById("delay-risk-freq");
const engineOverheatFreqEl = document.getElementById("engine-overheat-freq");
const fuelAnomalyFreqEl = document.getElementById("fuel-anomaly-freq");
const weatherWarningFreqEl = document.getElementById("weather-warning-freq");

getSummaryKPIs();

function getSummaryKPIs() {
    urlKpis = '/api/dashboard/kpis/';
    urlSummaries = '/api/kpisummary/'
    fetch(urlKpis)
        .then(response => response.json())
        .then(data =>{
            totalVesselsEl.textContent = data.total_vessels;
            activeVesselsEl.textContent = data.active_vessels;
            totalVoyagesEl.textContent = data.total_voyages;
            ongoingVoyagesEl.textContent = data.ongoing_voyages;
            telemetryRecordsEl.textContent = data.telemetry_records;
            totalAlertsEl.textContent = data.total_alerts;
            criticalAlertsEl.textContent = data.critical_alerts;
            unresolvedAlerts.textContent = data.unresolved_alerts;
        })
    
    fetch(urlSummaries)
        .then(response => response.json())
        .then(data => {
            for (const item of data){
                if (item.alert_type === "delay_risk") delayRiskFreqEl.textContent = item.count;
                if (item.alert_type === "engine_overheat") engineOverheatFreqEl.textContent = item.count;
                if (item.alert_type === "fuel_anomaly") fuelAnomalyFreqEl.textContent = item.count;
                if (item.alert_type === "weather_warning") weatherWarningFreqEl.textContent = item.count;
            }
        })
        
}
