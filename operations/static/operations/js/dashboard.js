document.addEventListener("DOMContentLoaded", () => {
    loadKPIs();
    loadAlertsTable();
    loadAlertTypeChart();
    loadSeverityChart();
    loadAlertsTimeSeries();
    loadAlertsByVessel();
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
                    title: {
                        display: true,
                        text: "Alert distribution by type",
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
                    title: {
                        display: true,
                        text: "Alert Distribution by Severity",
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

async function loadAlertsTimeSeries() {
    try {
        const data = await fetchData("/api/alerts/over-time/");
        const labels = data.map(item => new Date(item.date).toLocaleDateString(
            "en-US",
            {
                year: "numeric",
                month: "short",
                day: "numeric",
            }
        ));
        const totalAlerts = data.map(item => item.total_alerts);
        const criticalAlerts = data.map(item => item.critical_alerts);
        const alertEvolutionCanvas = document.getElementById("alert-time-evolution");

        new Chart(alertEvolutionCanvas, {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: "All Alerts (Both High and Critical)",
                        data: totalAlerts,
                        tension: 0.3,
                    },
                    {
                        label: "Critical Alerts",
                        data: criticalAlerts,
                        tension: 0.3,
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: "top",
                    },
                    title: {
                        display: false,
                        text: "Time Evolution of Alerts",
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.raw} alerts`;
                            }
                        }
                    }
                }
            }
        })
    } catch(error) {
        console.error(error)
    }
}

async function loadAlertsByVessel() {
    try {
        const data = await fetchData("/api/alerts/top-vessels/")
        const labels = data.map(item => item.vessel_name);
        const alertCounts = data.map(item => item.alert_count);
        const alertByVesselCanvas = document.getElementById("alert-by-vessel-chart");
        new Chart(alertByVesselCanvas, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        data: alertCounts,
                        label: "Alert count",
                    }
                ]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const item = data[context.dataIndex]
                                return (
                                    `${item.percentage}% of top 10 alerts`
                                )
                            }
                        }
                    }
                }
            }
        });

    } catch(error) {
        console.error(error);
    }
}