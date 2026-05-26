document.addEventListener("DOMContentLoaded", () => {
    loadKPIs();
    loadAlertsTable();
});


async function loadKPIs() {
    const response = await fetch("/api/dashboard/kpis/");
    const data = await response.json();

    document.getElementById("total-vessels").textContent = data.total_vessels;
    document.getElementById("active-vessels").textContent = data.active_vessels;
    document.getElementById("total-voyages").textContent = data.total_voyages;
    document.getElementById("total-alerts").textContent = data.total_alerts;
    document.getElementById("critical-alerts").textContent = data.critical_alerts;
    document.getElementById("unresolved-alerts").textContent = data.unresolved_alerts;
}


async function loadAlertsTable() {
    try {
        const response = await fetch("/api/alerts/latest/");
        if (!response.ok) {
            throw new Error("Failed to fetch KPI data");
        }
        const data = await response.json();
        const tableBodyEl = document.getElementById("latest-alerts-table");
        let htmlTable = "";
        for (const item of data) {
            htmlTable += 
            `<tr> 
                <td>${item.vessel_name}</td> 
                <td>${item.alert_type_display}</td> 
                <td>${item.severity_display}</td> 
                <td>${item.message}</td> 
                <td>${new Date(item.created_at).toLocaleString()}</td> 
            </tr>`;
        }
        tableBodyEl.innerHTML = htmlTable;
    } catch(error) {
        console.error(error);
    }
}


