"""
StreetSteel — Pagina Generator
================================
Dit script maakt automatisch alle ontbrekende HTML pagina's aan
voor alle steden, landen en fabrikanten.

Gebruik: python maak_paginas.py
"""

import os
from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
WEBSITE_MAP = Path(r"C:\streetsteel")

# ── ALLE LOCATIES ─────────────────────────────────────────────

NEDERLAND_STEDEN = [
    "amsterdam", "apeldoorn", "delfzijl", "eindhoven", "emmen",
    "groningen", "harderwijk", "helmond", "hoogezand", "lelystad",
    "veendam", "winschoten"
]

EUROPA_LANDEN = {
    "denemarken": ["korsor"],
    "duitsland":  ["bad-neuenahr-ahrweiler", "berlijn", "hohn",
                   "hohenschwangau", "kavelaer", "kiel", "kornau",
                   "leer", "oberhausen", "oldenburg", "riezlern"],
    "frankrijk":  [],
    "hongarije":  ["boedapest"],
    "italie":     ["como", "sicilie"],
    "kosovo":     [],
    "kroatie":    [],
    "macedonie":  [],
    "noorwegen":  ["bearums-verk", "bergen", "flaam", "honningsvaag",
                   "kristiansand", "molde", "olden", "oslo",
                   "stavanger", "tromsoe"],
    "oostenrijk": [],
    "portugal":   [],
    "schotland":  [],
    "slowakije":  ["bratislava"],
    "spanje":     ["cordoba", "granada", "nerja", "udeba"],
    "zweden":     ["goeteborg", "malmoe", "nordby"],
    "belgie": ["maaseik"],

}

LAND_VLAGGEN = {
    "denemarken": "🇩🇰", "duitsland": "🇩🇪", "frankrijk": "🇫🇷",
    "hongarije":  "🇭🇺", "italie":    "🇮🇹", "kosovo":    "🇽🇰",
    "kroatie":    "🇭🇷", "macedonie": "🇲🇰", "noorwegen": "🇳🇴",
    "oostenrijk": "🇦🇹", "portugal":  "🇵🇹", "schotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "slowakije":  "🇸🇰", "spanje":    "🇪🇸", "zweden":    "🇸🇪",
    "belgie": "🇧🇪",
}

LAND_NAMEN = {
    "denemarken": "Denemarken", "duitsland": "Duitsland",
    "frankrijk":  "Frankrijk",  "hongarije": "Hongarije",
    "italie":     "Italië",     "kosovo":    "Kosovo",
    "kroatie":    "Kroatië",    "macedonie": "Macedonië",
    "noorwegen":  "Noorwegen",  "oostenrijk":"Oostenrijk",
    "portugal":   "Portugal",   "schotland": "Schotland",
    "slowakije":  "Slowakije",  "spanje":    "Spanje",
    "zweden":     "Zweden",
    "belgie": "België",
}

LAND_I18N = {
    "denemarken": "country.dk", "duitsland": "country.de",
    "frankrijk":  "country.fr", "hongarije": "country.hu",
    "italie":     "country.it", "kosovo":    "country.xk",
    "kroatie":    "country.hr", "macedonie": "country.mk",
    "noorwegen":  "country.no", "oostenrijk":"country.at",
    "portugal":   "country.pt", "schotland": "country.gb",
    "slowakije":  "country.sk", "spanje":    "country.es",
    "zweden":     "country.se",
    "belgie": "country.be",
}

FABRIKANTEN = [
    "alphacan", "aqauway", "aquafix", "aquagate", "avk",
    "b-oz", "de-globe", "de-leidinggroothandel", "delta-plast", "dijg",
    "draka-polva", "dyka", "ewe", "fibrelita", "fmh-pompservice",
    "frelu", "friand", "geertsema", "globe", "hauraton",
    "hermelock", "joosten", "kamphuis", "kb", "kessel",
    "ksk", "landustrie", "lhs", "lovink", "martens",
    "meijer", "mij-onbekende-producent-en", "milder", "mous", "natuurbeton-milieu",
    "neering-bogel", "nki", "norinco", "nyloplast", "oogink",
    "p-konings", "pam", "passevant", "pipelife", "poly",
    "samson", "sotra", "stora", "stradus", "strucom",
    "tbs", "thijssen", "topatec", "van-der-velden", "veko",
    "vulcanus", "w-ten-cate", "waprog", "waterleiding-mij-prov-groningen", "wavin",
    "weegels"
]

# ── TEMPLATES ─────────────────────────────────────────────────

def stad_template_nl(stad_naam, fotos_pad, css_pad, js_pad):
    """HTML template voor een Nederlandse stad."""
    stad_titel = stad_naam.replace("-", " ").title()
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="page-country" content="nederland">
    <title>{stad_titel} — StreetSteel</title>
    <meta name="description" content="Putdeksels en straatkolken gefotografeerd in {stad_titel}, Nederland.">
    <link rel="stylesheet" href="{css_pad}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
            <span class="logo-icon">⬡</span>
            <div class="logo-text">
                <span class="logo-main">STREET</span><span class="logo-accent">STEEL</span>
                <span class="logo-sub">.EU</span>
            </div>
        </a>
        <nav class="main-nav">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="nav-link">Home</a>
            <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" class="nav-link active">Nederland</a>
            <a href="{css_pad.replace("src/css/main.css", "europa.html")}" class="nav-link">Europa</a>
            <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" class="nav-link">Fabrikanten</a>
            <a href="{css_pad.replace("src/css/main.css", "over.html")}" class="nav-link">Over</a>
        </nav>
        <div class="header-right">
            <div class="lang-switcher" id="langSwitcher"></div>
            <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
        </div>
    </div>
</header>
<div class="mobile-menu" id="mobileMenu">
    <nav class="mobile-nav">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
        <a href="{css_pad.replace("src/css/main.css", "nederland.html")}">Nederland</a>
        <a href="{css_pad.replace("src/css/main.css", "europa.html")}">Europa</a>
        <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}">Fabrikanten</a>
        <a href="{css_pad.replace("src/css/main.css", "over.html")}">Over</a>
    </nav>
</div>
<div class="page-hero">
    <div class="container">
        <div class="breadcrumb">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
            <span>›</span>
            <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" data-i18n="country.nl">Nederland</a>
            <span>›</span>
            {stad_titel}
        </div>
        <h1 class="page-title">{stad_titel}</h1>
        <div class="page-meta">
            <div class="page-meta-item"><span>🇳🇱</span><span data-i18n="country.nl">Nederland</span></div>
            <div class="page-meta-item">
                <strong class="photo-count-live"></strong>&nbsp;<span data-i18n="page.photos">op deze pagina</span>
            </div>
        </div>
    </div>
</div>
<section class="photo-gallery">
    <div class="container">
        <div class="gallery-grid" id="galleryGrid"></div>
        <div class="gallery-empty" id="galleryEmpty" style="text-align:center;padding:80px 0;color:#555;font-family:'Barlow Condensed',sans-serif;font-size:18px;letter-spacing:0.1em;text-transform:uppercase;">
            Foto's worden geladen...
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
                <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
                    <span class="logo-icon">⬡</span>
                    <div class="logo-text"><span class="logo-main">STREET</span><span class="logo-accent">STEEL</span></div>
                </a>
                <p data-i18n="footer.tagline">Putdeksels van de wereld.</p>
                
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.locations">Locaties</h4>
                <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" data-i18n="country.nl">Nederland</a>
                <a href="{css_pad.replace("src/css/main.css", "europa.html")}" data-i18n="nav.europe">Europa</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.manufacturers">Fabrikanten</h4>
                <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" data-i18n="footer.all.manufacturers">Alle fabrikanten A-Z</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.more">Meer</h4>
                <a href="{css_pad.replace("src/css/main.css", "over.html")}" data-i18n="nav.about">Over dit project</a>
                <a href="https://paypal.me/gradje340" target="_blank" data-i18n="nav.support">Steun de maker</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2021–2026 StreetSteel.com</p>
            <p data-i18n="footer.rights">Alle foto's zijn eigendom van de maker.</p>
        </div>
    </div>
</footer>
<script src="{js_pad.replace("main.js", "i18n.js")}"></script>
<script src="{js_pad}"></script>
</body>
</html>'''


def europa_stad_template(land, stad, fotos_pad, css_pad, js_pad):
    """HTML template voor een Europese stad."""
    stad_titel = stad.replace("-", " ").title() if stad else LAND_NAMEN.get(land, land.title())
    land_naam  = LAND_NAMEN.get(land, land.title())
    vlag       = LAND_VLAGGEN.get(land, "🌍")
    i18n_key   = LAND_I18N.get(land, "nav.europe")

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="page-country" content="{land}">
    <title>{stad_titel} — StreetSteel</title>
    <meta name="description" content="Putdeksels en straatkolken gefotografeerd in {stad_titel}, {land_naam}.">
    <link rel="stylesheet" href="{css_pad}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
            <span class="logo-icon">⬡</span>
            <div class="logo-text">
                <span class="logo-main">STREET</span><span class="logo-accent">STEEL</span>
                <span class="logo-sub">.EU</span>
            </div>
        </a>
        <nav class="main-nav">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="nav-link">Home</a>
            <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" class="nav-link">Nederland</a>
            <a href="{css_pad.replace("src/css/main.css", "europa.html")}" class="nav-link active">Europa</a>
            <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" class="nav-link">Fabrikanten</a>
            <a href="{css_pad.replace("src/css/main.css", "over.html")}" class="nav-link">Over</a>
        </nav>
        <div class="header-right">
            <div class="lang-switcher" id="langSwitcher"></div>
            <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
        </div>
    </div>
</header>
<div class="mobile-menu" id="mobileMenu">
    <nav class="mobile-nav">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
        <a href="{css_pad.replace("src/css/main.css", "nederland.html")}">Nederland</a>
        <a href="{css_pad.replace("src/css/main.css", "europa.html")}">Europa</a>
        <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}">Fabrikanten</a>
        <a href="{css_pad.replace("src/css/main.css", "over.html")}">Over</a>
    </nav>
</div>
<div class="page-hero">
    <div class="container">
        <div class="breadcrumb">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
            <span>›</span>
            <a href="{css_pad.replace("src/css/main.css", "europa.html")}">Europa</a>
            <span>›</span>
            <a href="{css_pad.replace("src/css/main.css", f"europa/{land}.html")}">{land_naam}</a>
            {f"<span>›</span>{stad_titel}" if stad else ""}
        </div>
        <h1 class="page-title">{stad_titel}</h1>
        <div class="page-meta">
            <div class="page-meta-item"><span>{vlag}</span><span data-i18n="{i18n_key}">{land_naam}</span></div>
            <div class="page-meta-item">
                <strong class="photo-count-live"></strong>&nbsp;<span data-i18n="page.photos">op deze pagina</span>
            </div>
        </div>
    </div>
</div>
<section class="photo-gallery">
    <div class="container">
        <div class="gallery-grid" id="galleryGrid"></div>
        <div class="gallery-empty" id="galleryEmpty" style="text-align:center;padding:80px 0;color:#555;font-family:'Barlow Condensed',sans-serif;font-size:18px;letter-spacing:0.1em;text-transform:uppercase;">
            Foto's worden geladen...
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
                <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
                    <span class="logo-icon">⬡</span>
                    <div class="logo-text"><span class="logo-main">STREET</span><span class="logo-accent">STEEL</span></div>
                </a>
                <p data-i18n="footer.tagline">Putdeksels van de wereld.</p>
                
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.locations">Locaties</h4>
                <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" data-i18n="country.nl">Nederland</a>
                <a href="{css_pad.replace("src/css/main.css", "europa.html")}" data-i18n="nav.europe">Europa</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.manufacturers">Fabrikanten</h4>
                <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" data-i18n="footer.all.manufacturers">Alle fabrikanten A-Z</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.more">Meer</h4>
                <a href="{css_pad.replace("src/css/main.css", "over.html")}" data-i18n="nav.about">Over dit project</a>
                <a href="https://paypal.me/gradje340" target="_blank" data-i18n="nav.support">Steun de maker</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2021–2026 StreetSteel.com</p>
            <p data-i18n="footer.rights">Alle foto's zijn eigendom van de maker.</p>
        </div>
    </div>
</footer>
<script src="{js_pad.replace("main.js", "i18n.js")}"></script>
<script src="{js_pad}"></script>
</body>
</html>'''


def europa_land_met_steden_template(land, steden, css_pad, js_pad):
    """HTML template voor een Europees LAND met een of meer steden: toont stad-tegels."""
    land_naam = LAND_NAMEN.get(land, land.title())
    vlag      = LAND_VLAGGEN.get(land, "\U0001F30D")
    i18n_key  = LAND_I18N.get(land, "nav.europe")
    n = len(steden)
    stad_woord = "stad" if n == 1 else "steden"

    tegels = ""
    for stad in steden:
        stad_titel = stad.replace("-", " ").title()
        tegels += f'''
            <a href="/europa/{land}/{stad}.html" class="location-card">
                <div class="card-img-placeholder">
                    <span class="card-flag">{vlag}</span>
                </div>
                <div class="card-body">
                    <span class="card-country" data-i18n="{i18n_key}">{land_naam}</span>
                    <h3 class="card-city">{stad_titel}</h3>
                    <span class="card-count photo-count" data-page="europa/{land}/{stad}"></span>
                </div>
            </a>'''

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="page-country" content="{land}">
    <title>{land_naam} \u2014 StreetSteel</title>
    <meta name="description" content="Putdeksels gefotografeerd in {land_naam}.">
    <link rel="stylesheet" href="{css_pad}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="../../index.html" class="logo">
            <span class="logo-icon">\u2B21</span>
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
            <span>\u203A</span>
            <a href="../../europa.html">Europa</a>
            <span>\u203A</span>
            {land_naam}
        </div>
        <h1 class="page-title">{land_naam}</h1>
        <div class="page-meta">
            <div class="page-meta-item">
                <span>{vlag}</span>
                <span data-i18n="{i18n_key}">{land_naam}</span>
            </div>
            <div class="page-meta-item">
                <span>{n} {stad_woord}</span>
            </div>
        </div>
    </div>
</div>

<section class="section">
    <div class="container">
        <div class="cards-grid">
            {tegels}
        </div>
    </div>
</section>

<div class="floating-support" id="floatingSupport">
    <a href="https://paypal.me/gradje340" target="_blank" rel="noopener" class="floating-support__btn">
        \u2665 <span data-i18n="support.floating">Steun</span>
    </a>
</div>

<footer class="site-footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand">
                <a href="../../index.html" class="logo">
                    <span class="logo-icon">\u2B21</span>
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
            <p>\u00A9 2021\u20132026 StreetSteel.eu</p>
            <p data-i18n="footer.rights">Alle foto\u0027s zijn eigendom van de maker.</p>
        </div>
    </div>
</footer>
<script src="../../src/js/i18n.js"></script>
<script src="../../src/js/main.js"></script>
<script src="../../src/js/fotos.js"></script>
</body>
</html>'''


def fabrikant_template(fab_naam, css_pad, js_pad):
    """HTML template voor een fabrikant."""
    fab_titel = fab_naam.replace("-", " ").title()
    fotos_pad = f"fotos/fabrikanten/{fab_naam}"

    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="page-country" content="fabrikanten">
    <title>{fab_titel} — StreetSteel</title>
    <meta name="description" content="Putdeksels van fabrikant {fab_titel}, gefotografeerd in Nederland en Europa.">
    <link rel="stylesheet" href="{css_pad}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="site-header">
    <div class="header-inner">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
            <span class="logo-icon">⬡</span>
            <div class="logo-text">
                <span class="logo-main">STREET</span><span class="logo-accent">STEEL</span>
                <span class="logo-sub">.EU</span>
            </div>
        </a>
        <nav class="main-nav">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="nav-link">Home</a>
            <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" class="nav-link">Nederland</a>
            <a href="{css_pad.replace("src/css/main.css", "europa.html")}" class="nav-link">Europa</a>
            <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" class="nav-link active">Fabrikanten</a>
            <a href="{css_pad.replace("src/css/main.css", "over.html")}" class="nav-link">Over</a>
        </nav>
        <div class="header-right">
            <div class="lang-switcher" id="langSwitcher"></div>
            <button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
        </div>
    </div>
</header>
<div class="mobile-menu" id="mobileMenu">
    <nav class="mobile-nav">
        <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
        <a href="{css_pad.replace("src/css/main.css", "nederland.html")}">Nederland</a>
        <a href="{css_pad.replace("src/css/main.css", "europa.html")}">Europa</a>
        <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}">Fabrikanten</a>
        <a href="{css_pad.replace("src/css/main.css", "over.html")}">Over</a>
    </nav>
</div>
<div class="page-hero">
    <div class="container">
        <div class="breadcrumb">
            <a href="{css_pad.replace("src/css/main.css", "index.html")}">Home</a>
            <span>›</span>
            <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}">Fabrikanten</a>
            <span>›</span>
            {fab_titel}
        </div>
        <h1 class="page-title">{fab_titel}</h1>
        <div class="page-meta">
            <div class="page-meta-item"><span>🏭</span><span>Fabrikant</span></div>
            <div class="page-meta-item">
                <strong class="photo-count-live"></strong>&nbsp;<span data-i18n="page.photos">op deze pagina</span>
            </div>
        </div>
    </div>
</div>
<section class="manufacturer-intro">
    <div class="container">
        <p id="introTekst">Introductietekst wordt via het beheerpaneel toegevoegd.</p>
        <a href="#" id="websiteLink" class="manufacturer-website" style="display:none" data-i18n="manufacturer.website">Website fabrikant →</a>
    </div>
</section>
<section class="photo-gallery">
    <div class="container">
        <div class="gallery-grid" id="galleryGrid"></div>
        <div class="gallery-empty" id="galleryEmpty" style="text-align:center;padding:80px 0;color:#555;font-family:'Barlow Condensed',sans-serif;font-size:18px;letter-spacing:0.1em;text-transform:uppercase;">
            Foto's worden geladen...
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
                <a href="{css_pad.replace("src/css/main.css", "index.html")}" class="logo">
                    <span class="logo-icon">⬡</span>
                    <div class="logo-text"><span class="logo-main">STREET</span><span class="logo-accent">STEEL</span></div>
                </a>
                <p data-i18n="footer.tagline">Putdeksels van de wereld.</p>
                
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.locations">Locaties</h4>
                <a href="{css_pad.replace("src/css/main.css", "nederland.html")}" data-i18n="country.nl">Nederland</a>
                <a href="{css_pad.replace("src/css/main.css", "europa.html")}" data-i18n="nav.europe">Europa</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.manufacturers">Fabrikanten</h4>
                <a href="{css_pad.replace("src/css/main.css", "fabrikanten.html")}" data-i18n="footer.all.manufacturers">Alle fabrikanten A-Z</a>
            </div>
            <div class="footer-nav">
                <h4 data-i18n="footer.nav.more">Meer</h4>
                <a href="{css_pad.replace("src/css/main.css", "over.html")}" data-i18n="nav.about">Over dit project</a>
                <a href="https://paypal.me/gradje340" target="_blank" data-i18n="nav.support">Steun de maker</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2021–2026 StreetSteel.com</p>
            <p data-i18n="footer.rights">Alle foto's zijn eigendom van de maker.</p>
        </div>
    </div>
</footer>
<script src="{js_pad.replace("main.js", "i18n.js")}"></script>
<script src="{js_pad}"></script>
</body>
</html>'''


# ── HOOFDPROGRAMMA ────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  STREETSTEEL — PAGINA GENERATOR")
    print("=" * 55)

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Map niet gevonden: {WEBSITE_MAP}")
        print("   Controleer of je QNAP verbonden is.")
        input("\nDruk op Enter om af te sluiten...")
        return

    aangemaakt = 0
    overgeslagen = 0

    # ── NEDERLAND ────────────────────────────────────────────
    print("\n🇳🇱 Nederland steden aanmaken...")
    nl_map = WEBSITE_MAP / "nederland"
    nl_map.mkdir(exist_ok=True)

    for stad in NEDERLAND_STEDEN:
        pad = nl_map / f"{stad}.html"
        if pad.exists():
            overgeslagen += 1
            continue
        fotos_pad = f"fotos/nederland/{stad}"
        html = stad_template_nl(stad, fotos_pad, "../src/css/main.css", "../src/js/main.js")
        pad.write_text(html, encoding="utf-8")
        aangemaakt += 1
        print(f"  ✅ nederland/{stad}.html")

    # ── EUROPA ───────────────────────────────────────────────
    print("\n🌍 Europa pagina's aanmaken...")
    europa_map = WEBSITE_MAP / "europa"
    europa_map.mkdir(exist_ok=True)

    for land, steden in EUROPA_LANDEN.items():
        land_map = europa_map / land
        land_map.mkdir(exist_ok=True)

        # Landpagina: met steden -> tegel-layout; zonder steden -> fotogalerij
        land_pad = europa_map / f"{land}.html"
        if not land_pad.exists():
            if steden:
                html = europa_land_met_steden_template(land, steden, "../../src/css/main.css", "../../src/js/main.js")
            else:
                fotos_pad = f"fotos/europa/{land}"
                html = europa_stad_template(land, "", fotos_pad, "../../src/css/main.css", "../../src/js/main.js")
            land_pad.write_text(html, encoding="utf-8")
            aangemaakt += 1
            print(f"  ✅ europa/{land}.html")
        else:
            overgeslagen += 1

        # Stadspagina's binnen het land
        for stad in steden:
            stad_pad = land_map / f"{stad}.html"
            if stad_pad.exists():
                overgeslagen += 1
                continue
            fotos_pad = f"fotos/europa/{land}/{stad}"
            html = europa_stad_template(land, stad, fotos_pad, "../../../src/css/main.css", "../../../src/js/main.js")
            stad_pad.write_text(html, encoding="utf-8")
            aangemaakt += 1
            print(f"  ✅ europa/{land}/{stad}.html")

    # ── FABRIKANTEN ──────────────────────────────────────────
    print("\n🏭 Fabrikanten pagina's aanmaken...")
    fab_map = WEBSITE_MAP / "fabrikanten"
    fab_map.mkdir(exist_ok=True)

    for fab in FABRIKANTEN:
        pad = fab_map / f"{fab}.html"
        if pad.exists():
            overgeslagen += 1
            continue
        html = fabrikant_template(fab, "../src/css/main.css", "../src/js/main.js")
        pad.write_text(html, encoding="utf-8")
        aangemaakt += 1
        print(f"  ✅ fabrikanten/{fab}.html")

    # ── EINDRAPPORT ──────────────────────────────────────────
    print(f"\n{'=' * 55}")
    print(f"  KLAAR!")
    print(f"  ✅ Aangemaakt:    {aangemaakt} pagina's")
    print(f"  ⏭️  Al aanwezig:  {overgeslagen} pagina's")
    print(f"{'=' * 55}")
    print(f"\n📁 Pagina's staan in: {WEBSITE_MAP}")
    print(f"\nVolgende stap: commit en push via GitHub Desktop!")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()