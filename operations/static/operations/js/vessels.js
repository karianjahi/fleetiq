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
        console.log(data);
        const vesselEl = document.getElementById("vessel-list");
        let html = "";
        for (const item of data) {
            html += `
            <a href="/vessels/${item.id}/" class="vessel-card">
            <h3>${item.name}</h3>
            <p>${item.vessel_type}</p>
            <p>Status: ${item.status}</p>
            </a>
            `
        }
        vesselEl.innerHTML = html;
    } catch(error) {
        console.error(error);
    }
}