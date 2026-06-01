document.addEventListener("DOMContentLoaded", () => {
    loadKPIs();
    loadAlertsTable();
    loadAlertTypeChart();
    loadSeverityChart();
});

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
    }
    return await response.json();
}


async function loadKPIs() {
    try {
        const data = await fetchData("/api/dashboard/kpis/");
        document.getElementById("total-vessels").textContent = data.total_vessels;
        document.getElementById("active-vessels").textContent = data.active_vessels;
        document.getElementById("total-voyages").textContent = data.total_voyages;
        document.getElementById("total-alerts").textContent = data.total_alerts;
        document.getElementById("critical-alerts").textContent = data.critical_alerts;
        document.getElementById("unresolved-alerts").textContent = data.unresolved_alerts;
    } catch(error) {
        console.error(error)
    }
    
}


async function loadAlertsTable() {
    try {
        const data = await fetchData("/api/alerts/latest/");
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

async function loadAlertTypeChart() {
    try {
        const data = await fetchData("/api/alerts/summary-by-type/");
        const labels = data.map(item => item.alert_type_display);
        const counts = data.map(item => item.count);
        const chartCanvas = document.getElementById("alert-type-chart");
    
        new Chart(chartCanvas, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: counts
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "bottom"
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const item = data[context.dataIndex];
                                return (
                                    `${item.alert_type_display}: ` + 
                                    `${item.count} alerts ` +
                                    `(${item.percentage}%)`
                                );
                            }
                        }
                    }
                }
            }
        });
    } catch(error) {
        console.error(error)
    } 
}

async function loadSeverityChart() {
    try {
        const data = await fetchData("/api/alerts/summary-by-severity/");
        const labels = data.map(item => item.severity_display);
        const counts = data.map(item => item.count);
        const severityChartCanvas = document.getElementById("alert-severity-chart");

        new Chart(severityChartCanvas, {
            type: "doughnut",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: counts
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: "bottom",
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const item = data[context.dataIndex];
                                return (
                                    `${item.severity_display}: ` +
                                    `${item.count} alerts ` + 
                                    `(${item.percentage}%)`
                                )
                            }
                        }
                    }
                }
            }
        })
    } catch(error) {
        console.error(error);
    }
    
}
