const totalVesselsEl = document.getElementById("total-vessels");
const activeVesselsEl = document.getElementById("active-vessels");
const totalVoyagesEl = document.getElementById("total-voyages");
const telemetryRecordsEl = document.getElementById("telemetry-records");
const totalAlertsEl = document.getElementById("total-alerts");
const criticalAlertsEl = document.getElementById("critical-alerts");
const unresolvedAlerts = document.getElementById("unresolved-alerts");
const ongoingVoyagesEl = document.getElementById("ongoing-voyages");


getSummaryKPIs();

function getSummaryKPIs() {
    url = '/api/dashboard/kpis/'
    fetch(url)
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
        
}
