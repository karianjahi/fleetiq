const currentPath = window.location.pathname
const vesselId = currentPath.split("/")[2];

let allVoyages = [];
let currentVoyagePage = 1;
const voyagesPerPage = 5;

let allAlerts = [];
let currentAlertPage = 1;
const alertsPerPage = 10;

loadVesselDetail(vesselId);
loadVoyageList(vesselId);
loadVesselAlerts(vesselId);
loadVesselKPIs(vesselId);
setUpAlertPagination();
setUpAlertSorting();
setUpAlertFiltering();
setUpVoyagePagination()

function formatDateTime(date) {
    return new Date(date).toLocaleString(
        "en-GB",
        {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
            hour12: false,
            timeZone: "UTC",
        }
    ) + " UTC";
}

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
    }
    return response.json();
}

async function loadVesselDetail(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/`;
        const data = await fetchData(url);
        const containerEl = document.getElementById("vessel-detail");
        const html = `
            <div class="vessel-info-card">
                <h2>${data.name}</h2>
                <p><strong>Vessel Type:</strong> ${data.vessel_type}</p>
                <p><strong>Status:</strong> ${data.status}</p>
                <p><strong>IMO Number:</strong> ${data.imo_number}</p>
            </div>
`;

        containerEl.innerHTML = html;
    } catch (error) {
        console.error(error);
    }

}

async function loadVoyageList(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/voyages/`;
        const data = await fetchData(url);
        allVoyages = data;
        currentVoyagePage = 1;
        renderVoyageTable();
    } catch (error) {
        console.error(error);
    }

}

async function renderVoyageTable() {
    const voyageTableBody = document.getElementById("voyage-table-body");

    const start = (currentVoyagePage - 1) * voyagesPerPage;

    const end = start + voyagesPerPage;

    const pageVoyages = allVoyages.slice(start, end);

    let html = "";

    for (const item of pageVoyages) {
        html += `
            <tr>
                <td>${item.departure_port}</td>
                <td>${item.destination_port}</td>
                <td>${formatDateTime(item.departure_time)}</td>
                <td>${formatDateTime(item.estimated_arrival)}</td>
                <td>${item.status}</td>
            </tr>
        `;
    }
    voyageTableBody.innerHTML = html;

    const totalPages = Math.ceil(
        allVoyages.length / voyagesPerPage
    ) || 1;
    document.getElementById("voyage-page-info").textContent = `Page ${currentVoyagePage} of ${totalPages}`;

    document.getElementById("prev-voyage-page").disabled = currentVoyagePage === 1;

    document.getElementById("next-voyage-page").disabled = currentVoyagePage === totalPages;
}

async function loadVesselAlerts(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/alerts/`;
        const data = await fetchData(url);

        allAlerts = data;
        currentAlertPage = 1;

        renderAlertTable();
    } catch (error) {
        console.error(error);
    }
}

async function loadVesselKPIs(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/kpis/`;
        const data = await fetchData(url);
        document.getElementById("total-voyages").textContent = data.total_voyages;
        document.getElementById("total-alerts").textContent = data.total_alerts;
        document.getElementById("critical-alerts").textContent = data.critical_alerts;
        document.getElementById("latest-alert-type").textContent = data.latest_alert;
        document.getElementById("health-status").textContent = data.health_status;
    } catch (error) {
        console.error("Failed to load vessel KPIs:", error);
    }
}

async function renderAlertTable() {
    const alertTableBody = document.getElementById("alert-table-body");
    const sortValue = document.getElementById("alert-sort").value;
    const filterValue = document.getElementById("alert-filter").value;

    let filteredAlerts = [...allAlerts];

    if (filterValue !== "all") {
        filteredAlerts = filteredAlerts.filter(item => item.severity === Number(filterValue))
    }


    let sortedAlerts = [...filteredAlerts];
    if (sortValue === "newest") {
        sortedAlerts.sort((a, b) => new Date(b.detected_at) - new Date(a.detected_at));
    }

    if (sortValue === "oldest") {
        sortedAlerts.sort((a, b) => new Date(a.detected_at) - new Date(b.detected_at));
    }

    if (sortValue === "severity-high") {
        sortedAlerts.sort((a, b) => b.severity - a.severity);
    }

    if (sortValue === "severity-low") {
        sortedAlerts.sort((a, b) => a.severity - b.severity);
    }

    const start = (currentAlertPage - 1) * alertsPerPage;
    const end = start + alertsPerPage;
    const pageAlerts = sortedAlerts.slice(start, end);
    if (pageAlerts.length === 0) {
        alertTableBody.innerHTML = `
        <tr>
            <td colspan="4" style="text-align:center;">
                No alerts found.
            </td>
        </tr>
    `;
        return;
    }
    let html = "";

    for (const item of pageAlerts) {
        html += `
            <tr>
                <td>${formatDateTime(item.detected_at)}</td>
                <td>${item.alert_type_display}</td>
                <td>${item.severity_display}</td>
                <td>${item.message}</td>
            </tr>
        `
    }

    alertTableBody.innerHTML = html;

    const totalPages = Math.ceil(
        sortedAlerts.length / alertsPerPage
    ) || 1;

    document.getElementById("alert-page-info").textContent = `Page ${currentAlertPage} of ${totalPages}`;

    document.getElementById("prev-alert-page").disabled = currentAlertPage === 1;
    document.getElementById("next-alert-page").disabled = currentAlertPage === totalPages;


}

function setUpAlertPagination() {
    document.getElementById("prev-alert-page").addEventListener("click", () => {
        if (currentAlertPage > 1) {
            currentAlertPage--;
            renderAlertTable();
        }
    });

    document.getElementById("next-alert-page").addEventListener("click", () => {
        const totalPages = Math.ceil(allAlerts.length / alertsPerPage);

        if (currentAlertPage < totalPages) {
            currentAlertPage++;
            renderAlertTable();
        }
    });
}

function setUpVoyagePagination() {
    document.getElementById("prev-voyage-page").addEventListener("click", () => {
        if (currentVoyagePage > 1) {
            currentVoyagePage--;
            renderVoyageTable();
        }
    });

    document.getElementById("next-voyage-page").addEventListener("click", () => {
        const totalPages = Math.ceil(allVoyages.length / voyagesPerPage) || 1;
        if (currentVoyagePage < totalPages) {
            currentVoyagePage++;
            renderVoyageTable();
        }
    });
}


function setUpAlertSorting() {
    document.getElementById("alert-sort").addEventListener("change", () => {
        currentAlertPage = 1;
        renderAlertTable();
    });
}

function setUpAlertFiltering() {
    document.getElementById("alert-filter").addEventListener("change", () => {
        currentAlertPage = 1;
        renderAlertTable();
    });
}

