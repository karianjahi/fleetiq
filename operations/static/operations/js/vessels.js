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
            html += `<div class="vessel-card">${item.name}</div>`
        }
        vesselEl.innerHTML = html;
    } catch(error) {
        console.error(error);
    }
}