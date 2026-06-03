
const currentPath = window.location.pathname
const vesselId = currentPath.split("/")[2];

loadVesselDetail(vesselId);
loadVoyageList(vesselId);

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
        let html = "";
        html += `<h2><strong></strong> ${data.name}</h2>`;
        html += `<p><strong>Vessel type:</strong> ${data.vessel_type}</p>`;
        html += `<p><strong>Status:</strong> ${data.status}</p>`;

        containerEl.innerHTML = html;
    } catch(error) {
        console.error(error);
    }
    
}

async function loadVoyageList(vesselId) {
    try {
        const url = `/api/vessels/${vesselId}/voyages/`;
        const data = await fetchData(url);
        console.log(data);
        const voyageListEl = document.getElementById("voyage-list");
        let html = "";
        for (const item of data) {
            html += `
                <div>
                    <p>
                        <strong>
                            Route:
                        </strong>
                        ${item.departure_port} → ${item.destination_port} 
                    </p>

                    <p>
                        <strong>
                            Status:
                        </strong>
                        ${item.status}
                    </p>
                </div>
            `
        }

        voyageListEl.innerHTML = html;
    } catch(error) {
        console.error(error);
    }
    
}