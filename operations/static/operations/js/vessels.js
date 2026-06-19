document.addEventListener("DOMContentLoaded", () => {
    loadVessels();
});

async function fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
    }
    return await response.json();
}

async function loadVessels() {
    try {
        const data = await fetchData("/api/vessels/");

        const params = new URLSearchParams(window.location.search);
        const selectedHealth = params.get("health");

        // console.log("selectedHealth:", selectedHealth);
        // console.log("vessel health values:", data.map(item => item.health_status));

        const pageTitle = document.getElementById("vessel-page-title");
        const activeFilterEl = document.getElementById("active-filter");
        const vesselEl = document.getElementById("vessel-list");
        let html = "";

        let vesselsToRender = data;
        if (selectedHealth) {
            vesselsToRender = data.filter(
                item => item.health_status === selectedHealth
            );
        }

        if (selectedHealth && pageTitle) {
            pageTitle.textContent = `FleetIQ Vessels - ${selectedHealth}`;

        }


        if (selectedHealth && activeFilterEl) {
            activeFilterEl.innerHTML = `
                    <p>
                        Showing <strong>${selectedHealth}</strong> vessels.
                        <a href="/vessels/">Show all</a>
                    </p>
    `;
        }

        if (vesselsToRender.length === 0) {
            vesselEl.innerHTML = `
                <p>No vessels currently match the
        <strong>${selectedHealth}</strong> health status.</p>
            `;
            return;
        }
        for (const item of vesselsToRender) {
            html += `
            <a href="/vessels/${item.id}/" class="vessel-card">
                <h3>${item.name}</h3>
                <p>${item.vessel_type}</p>
                <p>Status: ${item.status}</p>
                <p>
                    Health:
                    <span class="health-badge">
                        ${item.health_status}
                    </span>
                </p>
            </a>
            `
        }
        vesselEl.innerHTML = html;
    } catch (error) {
        console.error(error);
    }
}