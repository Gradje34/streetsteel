/**
 * StreetSteel — Foto Loader
 * Laadt foto's automatisch via JSON data bestanden
 */

document.addEventListener("DOMContentLoaded", () => {

    // === Tellers voor overzichtspagina's + totaal voor de homepage ===
    // Moet VÓÓR de galleryGrid-check staan, want overzichtspagina's
    // (nederland.html, europa.html, fabrikanten.html) en de homepage
    // hebben geen galleryGrid.
    const tellerEls = document.querySelectorAll(".photo-count[data-page]");
    const totaalEl  = document.getElementById("totaalFotos");

    if (tellerEls.length > 0 || totaalEl) {
        fetch("/data/tellers.json")
            .then(r => r.json())
            .then(tellers => {
                // Vul de tellers op de overzichtskaarten
                tellerEls.forEach(el => {
                    const page = el.getAttribute("data-page");

                    // Voor een land-met-steden (bijv. "europa/duitsland") bestaan er
                    // sub-keys als "europa/duitsland/berlijn". Tel dan het aantal steden
                    // en de som van hun foto's, en toon "X steden - Y foto's".
                    const prefix = page + "/";
                    const substeden = Object.keys(tellers).filter(k => k.startsWith(prefix));

                    if (substeden.length > 0) {
                        const aantalSteden = substeden.length;
                        const somFotos = substeden
                            .reduce((som, k) => som + (Number(tellers[k]) || 0), 0);
                        const stadLabel = aantalSteden === 1 ? "1 stad" : `${aantalSteden} steden`;
                        const fotoLabel = somFotos === 1 ? "1 foto" : `${somFotos} foto's`;
                        el.textContent = `${stadLabel} - ${fotoLabel}`;
                    } else {
                        // Land zonder steden, Nederland-stad of fabrikant: eigen fototal.
                        const aantal = tellers[page] || 0;
                        el.textContent = aantal === 1 ? "1 foto" : `${aantal} foto's`;
                    }
                });

                // Vul het totaal aantal foto's in de hero (homepage)
                if (totaalEl) {
                    const totaal = Object.values(tellers)
                        .reduce((som, n) => som + (Number(n) || 0), 0);
                    // Rond naar beneden af op het dichtstbijzijnde 10-tal,
                    // zodat het getal met "+" altijd waar blijft.
                    const afgerond = Math.floor(totaal / 10) * 10;
                    totaalEl.textContent = `${afgerond}+`;
                }
            })
            .catch(() => {});
    }

    // === Galerij op detailpagina's ===
    const grid  = document.getElementById("galleryGrid");
    const empty = document.getElementById("galleryEmpty");
    if (!grid) return;

    // Bepaal welk JSON bestand we nodig hebben op basis van het URL pad
    const pad = window.location.pathname;
    let jsonPad = null;

// nederland/groningen(.html) → /data/nederland/groningen.json
    const nlMatch = pad.match(/\/nederland\/([^/.]+)(?:\.html)?$/);
    if (nlMatch) jsonPad = `/data/nederland/${nlMatch[1]}.json`;

    // europa/noorwegen/oslo(.html) → /data/europa/noorwegen/oslo.json
    const euStadMatch = pad.match(/\/europa\/([^/]+)\/([^/.]+)(?:\.html)?$/);
    if (euStadMatch) jsonPad = `/data/europa/${euStadMatch[1]}/${euStadMatch[2]}.json`;

    // europa/noorwegen(.html) → /data/europa/noorwegen.json
    const euLandMatch = pad.match(/\/europa\/([^/.]+)(?:\.html)?$/);
    if (euLandMatch && !euStadMatch) jsonPad = `/data/europa/${euLandMatch[1]}.json`;

    // fabrikanten/wavin(.html) → /data/fabrikanten/wavin.json
    const fabMatch = pad.match(/\/fabrikanten\/([^/.]+)(?:\.html)?$/);
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
});
