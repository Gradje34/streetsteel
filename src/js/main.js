/**
 * StreetSteel — Hoofd JavaScript
 * Navigatie, fototeller, lightbox, galerij
 */

// ── FOTO TELLER DATA ──────────────────────────────────────────
// Wordt automatisch bijgewerkt via het beheerpaneel
const PHOTO_COUNTS = {
    "nederland/amsterdam":                    0,
    "nederland/apeldoorn":                    0,
    "nederland/delfzijl":                     0,
    "nederland/eindhoven":                    0,
    "nederland/emmen":                        0,
    "nederland/groningen":                    0,
    "nederland/harderwijk":                   0,
    "nederland/helmond":                      0,
    "nederland/hoogezand":                    0,
    "nederland/lelystad":                     0,
    "nederland/veendam":                      0,
    "nederland/winschoten":                   0,
    "europa/denemarken/korsor":               0,
    "europa/duitsland/bad-neuenahr-ahrweiler":0,
    "europa/duitsland/berlijn":               0,
    "europa/duitsland/hohn":                  0,
    "europa/duitsland/hohenschwangau":        0,
    "europa/duitsland/kavelaer":              0,
    "europa/duitsland/kiel":                  0,
    "europa/duitsland/kornau":                0,
    "europa/duitsland/leer":                  0,
    "europa/duitsland/oberhausen":            0,
    "europa/duitsland/oldenburg":             0,
    "europa/duitsland/riezlern":              0,
    "europa/hongarije/boedapest":             0,
    "europa/italie/como":                     0,
    "europa/italie/sicilie":                  0,
    "europa/kosovo":                          0,
    "europa/kroatie":                         0,
    "europa/macedonie":                       0,
    "europa/noorwegen/bearums-verk":          0,
    "europa/noorwegen/bergen":                0,
    "europa/noorwegen/flaam":                 0,
    "europa/noorwegen/honningsvaag":          0,
    "europa/noorwegen/kristiansand":          0,
    "europa/noorwegen/molde":                 0,
    "europa/noorwegen/olden":                 0,
    "europa/noorwegen/oslo":                  0,
    "europa/noorwegen/stavanger":             0,
    "europa/noorwegen/tromsoe":               0,
    "europa/frankrijk":                       0,
    "europa/oostenrijk":                      0,
    "europa/portugal":                        0,
    "europa/schotland":                       0,
    "europa/slowakije/bratislava":            0,
    "europa/spanje/cordoba":                  0,
    "europa/spanje/granada":                  0,
    "europa/spanje/nerja":                    0,
    "europa/spanje/udeba":                    0,
    "europa/zweden/goeteborg":                0,
    "europa/zweden/malmoe":                   0,
    "europa/zweden/nordby":                   0,
};

// ── NAVIGATIE ─────────────────────────────────────────────────
function initNav() {
    const toggle = document.getElementById("menuToggle");
    const mobileMenu = document.getElementById("mobileMenu");

    if (toggle && mobileMenu) {
        toggle.addEventListener("click", () => {
            mobileMenu.classList.toggle("open");
            toggle.classList.toggle("open");
        });

        // Sluit menu bij klik buiten
        document.addEventListener("click", e => {
            if (!toggle.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.remove("open");
                toggle.classList.remove("open");
            }
        });
    }

    // Markeer actieve navigatielink
    const path = window.location.pathname;
    document.querySelectorAll(".nav-link, .mobile-nav a").forEach(link => {
        const href = link.getAttribute("href");
        if (href && path.endsWith(href)) {
            link.classList.add("active");
        }
    });
}

// ── FOTO TELLER ───────────────────────────────────────────────
function initPhotoCounts() {
    // Op pagina's: tel de daadwerkelijke galerij-items
    const galleryItems = document.querySelectorAll(".gallery-item");
    if (galleryItems.length > 0) {
        const count = galleryItems.length;
        const label = count === 1
            ? `1 ${I18n.t("photos.count.singular")}`
            : `${count} ${I18n.t("photos.count")}`;

        // Update teller in page-meta als die er is
        const metaCount = document.querySelector(".photo-count-live");
        if (metaCount) metaCount.textContent = label;

        // Update paginatitel teller
        const titleCount = document.querySelector(".page-count");
        if (titleCount) titleCount.textContent = count;
    }

    // Op overzichtspagina's: toon tellers uit PHOTO_COUNTS data
    document.querySelectorAll(".photo-count[data-page]").forEach(el => {
        const page = el.getAttribute("data-page");
        const count = PHOTO_COUNTS[page];
        if (count !== undefined) {
            const label = count === 1
                ? `1 ${I18n.t("photos.count.singular")}`
                : `${count} ${I18n.t("photos.count")}`;
            el.textContent = label;
        }
    });
}

// ── LIGHTBOX ──────────────────────────────────────────────────
let lightboxImages = [];
let lightboxIndex  = 0;

function initLightbox() {
    const items = document.querySelectorAll(".gallery-item");
    if (!items.length) return;

    // Verzamel alle afbeeldingen
    lightboxImages = Array.from(items).map(item => {
        const img = item.querySelector("img");
        return img ? img.src : "";
    }).filter(Boolean);

    // Maak lightbox element
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.id = "lightbox";
    lb.innerHTML = `
        <span class="lightbox-close" id="lbClose">✕</span>
        <span class="lightbox-nav lightbox-prev" id="lbPrev">‹</span>
        <img class="lightbox-img" id="lbImg" src="" alt="Foto">
        <span class="lightbox-nav lightbox-next" id="lbNext">›</span>
    `;
    document.body.appendChild(lb);

    // Klik op galerij-item
    items.forEach((item, index) => {
        item.addEventListener("click", () => openLightbox(index));
    });

    // Navigatie
    document.getElementById("lbClose").addEventListener("click", closeLightbox);
    document.getElementById("lbPrev").addEventListener("click", () => navigateLightbox(-1));
    document.getElementById("lbNext").addEventListener("click", () => navigateLightbox(1));

    // Klik buiten foto = sluiten
    lb.addEventListener("click", e => { if (e.target === lb) closeLightbox(); });

    // Toetsenbord navigatie
    document.addEventListener("keydown", e => {
        if (!lb.classList.contains("open")) return;
        if (e.key === "Escape")      closeLightbox();
        if (e.key === "ArrowLeft")   navigateLightbox(-1);
        if (e.key === "ArrowRight")  navigateLightbox(1);
    });
}

function openLightbox(index) {
    lightboxIndex = index;
    document.getElementById("lbImg").src = lightboxImages[index];
    document.getElementById("lightbox").classList.add("open");
    document.body.style.overflow = "hidden";
}

function closeLightbox() {
    document.getElementById("lightbox").classList.remove("open");
    document.body.style.overflow = "";
}

function navigateLightbox(dir) {
    lightboxIndex = (lightboxIndex + dir + lightboxImages.length) % lightboxImages.length;
    document.getElementById("lbImg").src = lightboxImages[lightboxIndex];
}

// ── LAZY LOADING AFBEELDINGEN ─────────────────────────────────
function initLazyLoad() {
    const imgs = document.querySelectorAll("img[data-src]");
    if (!imgs.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute("data-src");
                observer.unobserve(img);
            }
        });
    }, { rootMargin: "200px" });

    imgs.forEach(img => observer.observe(img));
}

// ── SCROLL ANIMATIES ──────────────────────────────────────────
function initScrollAnimations() {
    const elements = document.querySelectorAll(
        ".location-card, .manufacturer-item, .section-header, .gallery-item"
    );

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach((el, i) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition = `opacity 0.5s ease ${i * 0.04}s, transform 0.5s ease ${i * 0.04}s`;
        observer.observe(el);
    });
}

// ── DRIJVENDE STEUNKNOP ───────────────────────────────────────
function initFloatingSupport() {
    const btn = document.getElementById("floatingSupport");
    if (!btn) return;

    // Verberg aan het begin, toon na scrollen
    btn.style.opacity = "0";
    btn.style.transform = "translateY(20px)";
    btn.style.transition = "opacity 0.4s, transform 0.4s";

    window.addEventListener("scroll", () => {
        if (window.scrollY > 400) {
            btn.style.opacity = "1";
            btn.style.transform = "translateY(0)";
        } else {
            btn.style.opacity = "0";
            btn.style.transform = "translateY(20px)";
        }
    }, { passive: true });
}

// ── HEADER SCROLL EFFECT ──────────────────────────────────────
function initHeaderScroll() {
    const header = document.querySelector(".site-header");
    if (!header) return;

    window.addEventListener("scroll", () => {
        header.style.borderBottomColor = window.scrollY > 50
            ? "rgba(46,46,46,0.8)"
            : "rgba(46,46,46,1)";
    }, { passive: true });
}

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    initNav();
    initPhotoCounts();
    initLightbox();
    initLazyLoad();
    initScrollAnimations();
    initFloatingSupport();
    initHeaderScroll();
});
