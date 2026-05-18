/**
 * StreetSteel — Foto Loader
 * Laadt foto's automatisch via JSON data bestanden
 * Werkt met én zonder .html in de URL
 */

document.addEventListener("DOMContentLoaded", () => {

    const grid  = document.getElementById("galleryGrid");
    const empty = document.getElementById("galleryEmpty");
    if (!grid) return;

    // Verwijder .html uit het pad zodat het altijd hetzelfde werkt
    const pad = window.location.pathname.replace(/\.html$/, "");
    let jsonPad = null;

    // /nederland/groningen → /data/nederland/groningen.json
    const nlMatch = pad.match(/\/nederland\/([^/]+)$/);
    if (nlMatch) jsonPad = `/data/nederland/${nlMatch[1]}.json`;

    // /europa/noorwegen/oslo → /data/europa/noorwegen/oslo.json
    const euStadMatch = pad.match(/\/europa\/([^/]+)\/([^/]+)$/);
    if (euStadMatch) jsonPad = `/data/europa/${euStadMatch[1]}/${euStadMatch[2]}.json`;

    // /europa/noorwegen → /data/europa/noorwegen.json
    const euLandMatch = pad.match(/\/europa\/([^/]+)$/);
    if (euLandMatch && !euStadMatch) jsonPad = `/data/europa/${euLandMatch[1]}.json`;

    // /fabrikanten/wavin → /data/fabrikanten/wavin.json
    const fabMatch = pad.match(/\/fabrikanten\/([^/]+)$/);
    if (fabMatch) jsonPad = `/data/fabrikanten/${fabMatch[1]}.json`;

    if (!jsonPad) return;

    // Laad de JSON data
    fetch(jsonPad)
        .then(r => {
            if (!r.ok) throw new Error("Geen data");
            return r.json();
        })
        .then(data => {
            const fotos = data.fotos || [];

            if (fotos.length === 0) {
                if (empty) empty.textContent = "Nog geen foto's beschikbaar.";
                return;
            }

            if (empty) empty.style.display = "none";

            fotos.forEach(fotoUrl => {
                const item = document.createElement("div");
                item.className = "gallery-item";
                item.innerHTML = `
                    <img data-src="${fotoUrl}"
                         src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
                         alt="Putdeksel"
                         loading="lazy">
                    <div class="gallery-item-overlay"></div>
                `;
                grid.appendChild(item);
            });

            // Initialiseer lazy loading en lightbox
            if (typeof initLazyLoad === "function") initLazyLoad();
            if (typeof initLightbox  === "function") initLightbox();
            if (typeof initPhotoCounts === "function") initPhotoCounts();

            // Update de fototeller bovenaan de pagina
            const teller = document.querySelector(".photo-count-live");
            if (teller) {
                const aantal = fotos.length;
                teller.textContent = aantal === 1 ? `1 foto` : `${aantal} foto's`;
            }
        })
        .catch(() => {
            if (empty) empty.textContent = "Foto's worden binnenkort toegevoegd.";
        });

    // Laad ook de tellers voor overzichtspagina's
    const tellerEls = document.querySelectorAll(".photo-count[data-page]");
    if (tellerEls.length > 0) {
        fetch("/data/tellers.json")
            .then(r => r.json())
            .then(tellers => {
                tellerEls.forEach(el => {
                    const page = el.getAttribute("data-page");
                    const aantal = tellers[page] || 0;
                    el.textContent = aantal === 1 ? `1 foto` : `${aantal} foto's`;
                });
            })
            .catch(() => {});
    }
});