"""
StreetSteel — Land Overzichtspagina Generator
===============================================
Maakt voor elk Europees land een overzichtspagina
met alle steden als klikbare kaarten.

Gebruik: python maak_landpaginas.py
"""

from pathlib import Path

WEBSITE_MAP = Path(r"C:\streetsteel")

LANDEN = {
    "denemarken": {
        "naam": "Denemarken", "vlag": "🇩🇰", "i18n": "country.dk",
        "steden": [("korsor", "Korsør")],
    },
    "duitsland": {
        "naam": "Duitsland", "vlag": "🇩🇪", "i18n": "country.de",
        "steden": [
            ("bad-neuenahr-ahrweiler", "Bad Neuenahr-Ahrweiler"),
            ("berlijn", "Berlijn"), ("hohn", "Hohn"),
            ("hohenschwangau", "Hohenschwangau"), ("kavelaer", "Kavelaer"),
            ("kiel", "Kiel"), ("kornau", "Kornau"), ("leer", "Leer"),
            ("oberhausen", "Oberhausen"), ("oldenburg", "Oldenburg"),
            ("riezlern", "Riezlern"),
        ],
    },
    "frankrijk": {
        "naam": "Frankrijk", "vlag": "🇫🇷", "i18n": "country.fr",
        "steden": [],
    },
    "hongarije": {
        "naam": "Hongarije", "vlag": "🇭🇺", "i18n": "country.hu",
        "steden": [("boedapest", "Boedapest")],
    },
    "italie": {
        "naam": "Italië", "vlag": "🇮🇹", "i18n": "country.it",
        "steden": [("como", "Como"), ("sicilie", "Sicilië")],
    },
    "kosovo": {
        "naam": "Kosovo", "vlag": "🇽🇰", "i18n": "country.xk",
        "steden": [],
    },
    "kroatie": {
        "naam": "Kroatië", "vlag": "🇭🇷", "i18n": "country.hr",
        "steden": [],
    },
    "macedonie": {
        "naam": "Macedonië", "vlag": "🇲🇰", "i18n": "country.mk",
        "steden": [],
    },
    "noorwegen": {
        "naam": "Noorwegen", "vlag": "🇳🇴", "i18n": "country.no",
        "steden": [
            ("bearums-verk", "Bearums Verk"), ("bergen", "Bergen"),
            ("flaam", "Flåm"), ("honningsvaag", "Honningsvåg"),
            ("kristiansand", "Kristiansand"), ("molde", "Molde"),
            ("olden", "Olden"), ("oslo", "Oslo"),
            ("stavanger", "Stavanger"), ("tromsoe", "Tromsø"),
        ],
    },
    "oostenrijk": {
        "naam": "Oostenrijk", "vlag": "🇦🇹", "i18n": "country.at",
        "steden": [],
    },
    "portugal": {
        "naam": "Portugal", "vlag": "🇵🇹", "i18n": "country.pt",
        "steden": [],
    },
    "schotland": {
        "naam": "Schotland", "vlag": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "i18n": "country.gb",
        "steden": [],
    },
    "slowakije": {
        "naam": "Slowakije", "vlag": "🇸🇰", "i18n": "country.sk",
        "steden": [("bratislava", "Bratislava")],
    },
    "spanje": {
        "naam": "Spanje", "vlag": "🇪🇸", "i18n": "country.es",
        "steden": [
            ("cordoba", "Córdoba"), ("granada", "Granada"),
            ("nerja", "Nerja"), ("udeba", "Úbeda"),
        ],
    },
    "zweden": {
        "naam": "Zweden", "vlag": "🇸🇪", "i18n": "country.se",
        "steden": [
            ("goeteborg", "Göteborg"), ("malmoe", "Malmö"),
            ("nordby", "Nordby"),
        ],
    },
}


def maak_steden_kaarten(land, info):
    """Maak kaarten voor steden of een bericht als er geen steden zijn."""
    if not info["steden"]:
        return f'''
        <div style="text-align:center;padding:80px 0;color:#555;
                    font-family:'Barlow Condensed',sans-serif;
                    font-size:18px;letter-spacing:0.1em;text-transform:uppercase;">
            Foto's worden binnenkort toegevoegd.
        </div>'''

    kaarten = ""
    for slug, naam in info["steden"]:
        kaarten += f'''
            <a href="/europa/{land}/{slug}.html" class="location-card">
                <div class="card-img-placeholder">
                    <span class="card-flag">{info["vlag"]}</span>
                </div>
                <div class="card-body">
                    <span class="card-country" data-i18n="{info["i18n"]}">{info["naam"]}</span>
                    <h3 class="card-city">{naam}</h3>
                    <span class="card-count photo-count" data-page="europa/{land}/{slug}"></span>
                </div>
            </a>'''
    return kaarten


def maak_landpagina(land, info):
    steden_kaarten = maak_steden_kaarten(land, info)
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="page-country" content="{land}">
    <title>{info["naam"]} — StreetSteel</title>
    <meta name="description" content="Putdeksels gefotografeerd in {info["naam"]}.">
    <link rel="stylesheet" href="../../src/css/main.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="../../index.html" class="logo">
            <span class="logo-icon">⬡</span>
            <div class="logo-text">
                <span class="logo-main">STREET</span><span class="logo-accent">STEEL</span>
                <span class="logo-sub">.EU</span>
            </div>
        </a>
        <nav class="main-nav">
            <a href="../../index.html" class="nav-link">Home</a>
            <a href="../../nederland.html" class="nav-link">Nederland</a>
            <a href="../../europa.html" class="nav-link active">Europa</a>
            <a href="../../fabrikanten.html" class="nav-link">Fabrikanten</a>
            <a href="../../over.html" class="nav-link">Over</a>
        </nav>
        <div class="header-right">
            <div class="lang-switcher" id="langSwitcher"></div>
            <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
        </div>
    </div>
</header>
<div class="mobile-menu" id="mobileMenu">
    <nav class="mobile-nav">
        <a href="../../index.html">Home</a>
        <a href="../../nederland.html">Nederland</a>
        <a href="../../europa.html">Europa</a>
        <a href="../../fabrikanten.html">Fabrikanten</a>
        <a href="../../over.html">Over</a>
    </nav>
</div>

<div class="page-hero">
    <div class="container">
        <div class="breadcrumb">
            <a href="../../index.html">Home</a>
            <span>›</span>
            <a href="../../europa.html">Europa</a>
            <span>›</span>
            {info["naam"]}
        </div>
        <h1 class="page-title">{info["naam"]}</h1>
        <div class="page-meta">
            <div class="page-meta-item">
                <span>{info["vlag"]}</span>
                <span data-i18n="{info["i18n"]}">{info["naam"]}</span>
            </div>
            <div class="page-meta-item">
                <span>{len(info["steden"])} {"stad" if len(info["steden"]) == 1 else "steden"}</span>
            </div>
        </div>
    </div>
</div>

<section class="section">
    <div class="container">
        <div class="cards-grid">
            {steden_kaarten}
        </div>
    </div>
</section>

<div class="floating-support" id="floatingSupport">
    <a href="https://paypal.me/gradje340" target="_blank" rel="noopener" class="floating-support__btn">
        ♥ <span data-i18n="support.floating">Steun</span>
    </a>
</div>

<footer class="site-footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="../../index.html" class="logo">
                    <span class="logo-icon">⬡</span>
                    <div class="logo-text"><span class="logo-main">STREET</span><span class="logo-accent">STEEL</span></div>
                </a>
                <p data-i18n="footer.tagline">Putdeksels van de wereld.</p>
            </div>
            <div class="footer-nav">
                <h4>Locaties</h4>
                <a href="../../nederland.html">Nederland</a>
                <a href="../../europa.html">Europa</a>
            </div>
            <div class="footer-nav">
                <h4>Fabrikanten</h4>
                <a href="../../fabrikanten.html">Alle fabrikanten A-Z</a>
            </div>
            <div class="footer-nav">
                <h4>Meer</h4>
                <a href="../../over.html">Over dit project</a>
                <a href="https://paypal.me/gradje340" target="_blank">Steun de maker</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2021–2026 StreetSteel.eu</p>
            <p data-i18n="footer.rights">Alle foto's zijn eigendom van de maker.</p>
        </div>
    </div>
</footer>
<script src="../../src/js/i18n.js"></script>
<script src="../../src/js/main.js"></script>
<script src="../../src/js/fotos.js"></script>
</body>
</html>'''


def main():
    print("=" * 55)
    print("  STREETSTEEL — LAND OVERZICHTSPAGINA GENERATOR")
    print("=" * 55)

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Map niet gevonden: {WEBSITE_MAP}")
        input("\nDruk op Enter om af te sluiten...")
        return

    aangemaakt = 0

    for land, info in LANDEN.items():
        land_map = WEBSITE_MAP / "europa" / land
        land_map.mkdir(parents=True, exist_ok=True)

        pad = land_map / f"{land}.html"
        html = maak_landpagina(land, info)
        pad.write_text(html, encoding="utf-8")
        aangemaakt += 1
        print(f"  ✅ europa/{land}/{land}.html")

    print(f"\n{'=' * 55}")
    print(f"  KLAAR! {aangemaakt} landpagina's aangemaakt")
    print(f"{'=' * 55}")
    print(f"\nVolgende stap: commit en push via GitHub Desktop!")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()