
const currentPath = window.location.pathname
const vesselId = currentPath.split("/")[2];

loadVesselDetail(vesselId);
loadVoyageList(vesselId);
loadVesselAlerts(vesselId);

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
        const voyageListEl = document.getElementById("voyage-list");
        const tableBodyEl = document.getElementById("voyage-table-body");
        let html = "";
        for (const item of data) {
            // html += `
            //         <div class="voyage-card">
            //             <div class="voyage-route">
            //                 ${item.departure_port} → ${item.destination_port}
            //             </div>

            //             <div class="voyage-meta">
            //                 <span>Status: ${item.status}</span>
            //             </div>
            //         </div>
            // `
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

        // voyageListEl.innerHTML = html;
        tableBodyEl.innerHTML = html;

    } catch (error) {
        console.error(error);
    }

}

async function loadVesselAlerts(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/alerts/`;
        const data = await fetchData(url);
        const alertsListEl = document.getElementById("vessel-alert-list");
        const alertTableBody = document.getElementById("alert-table-body");
        let html = "";

        for (const item of data) {
            // html += `
            //         <div class="alert-card">
            //             <div class="alert-header">
            //                 <h4>${item.alert_type_display}</h4>
            //                 <span class="severity-badge">
            //                     ${item.severity_display}
            //                 </span>
            //             </div>
            //         <p>${item.message}</p>
            //         </div>
            // `
            html += `
                <tr>
                    <td>${formatDateTime(item.detected_at)}</td>
                    <td>${item.alert_type_display}</td>
                    <td>${item.severity_display}</td>
                    <td>${item.message}</td>
                </tr>
    `;

        }

        // alertsListEl.innerHTML = html;
        alertTableBody.innerHTML = html;
    } catch (error) {
        console.error(error);
    }
}