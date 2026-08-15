/**
 * StreetSteel — Hoofd JavaScript
 * Navigatie, fototeller, lightbox, galerij
 */

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
        // Gebruik data-src (de echte URL) als die er is; door lazy loading
        // staat in src soms nog een lege placeholder.
        return img ? (img.dataset.src || img.src) : "";
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
