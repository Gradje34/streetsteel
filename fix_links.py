"""
StreetSteel — Navigatielinks Fixer
====================================
Dit script zorgt dat alle interne links in de HTML pagina's
correct eindigen op .html zodat navigatie goed werkt.

Gebruik: python fix_links.py
"""

import re
from pathlib import Path

WEBSITE_MAP = Path(r"M:\Streetsteel.com\website\streetsteel")

# Pagina's die .html nodig hebben maar het missen
STEDEN_NL = [
    "amsterdam", "apeldoorn", "delfzijl", "eindhoven", "emmen",
    "groningen", "harderwijk", "helmond", "hoogezand", "lelystad",
    "veendam", "winschoten"
]

LANDEN_EU = [
    "denemarken", "duitsland", "frankrijk", "hongarije", "italie",
    "kosovo", "kroatie", "macedonie", "noorwegen", "oostenrijk",
    "portugal", "schotland", "slowakije", "spanje", "zweden"
]

STEDEN_EU = {
    "denemarken": ["korsor"],
    "duitsland":  ["bad-neuenahr-ahrweiler", "berlijn", "hohn",
                   "hohenschwangau", "kavelaer", "kiel", "kornau",
                   "leer", "oberhausen", "oldenburg", "riezlern"],
    "hongarije":  ["boedapest"],
    "italie":     ["como", "sicilie"],
    "noorwegen":  ["bearums-verk", "bergen", "flaam", "honningsvaag",
                   "kristiansand", "molde", "olden", "oslo",
                   "stavanger", "tromsoe"],
    "slowakije":  ["bratislava"],
    "spanje":     ["cordoba", "granada", "nerja", "udeba"],
    "zweden":     ["goeteborg", "malmoe", "nordby"],
}

FABRIKANTEN = [
    "alphacan", "aquagate", "aquafix", "aqauway", "avk", "b-oz",
    "de-leidinggroothandel", "de-globe", "delta-plast", "dijg",
    "draka-polva", "dyka", "ewe", "fibrelita", "fmh-pompservice",
    "frelu", "friand", "geertsema", "hauraton", "hermelock",
    "joosten", "kamphuis", "kb", "kessel", "ksk", "landustrie",
    "lhs", "lovink", "martens", "meijer", "milder", "mous",
    "natuurbeton-milieu", "neering-bogel", "nki", "norinco",
    "nyloplast", "oogink", "pam", "passevant", "pipelife", "poly",
    "samson", "sotra", "stora", "stradus", "strucom", "tbs",
    "thijssen", "topatec", "van-der-velden", "veko", "vulcanus",
    "w-ten-cate", "waprog", "waterleiding-mij-prov-groningen",
    "wavin", "weegels", "mij-onbekende-producent-en",
]

def fix_html_bestand(pad):
    """Fix alle interne links in een HTML bestand."""
    inhoud = pad.read_text(encoding="utf-8")
    origineel = inhoud

    # Fix nederland steden links
    for stad in STEDEN_NL:
        # href="...nederland/stad" zonder .html
        inhoud = re.sub(
            rf'(href="[^"]*nederland/){stad}(")',
            rf'\g<1>{stad}.html\2',
            inhoud
        )

    # Fix europa landen links
    for land in LANDEN_EU:
        inhoud = re.sub(
            rf'(href="[^"]*europa/){land}(")',
            rf'\g<1>{land}.html\2',
            inhoud
        )
        # Fix europa steden links
        steden = STEDEN_EU.get(land, [])
        for stad in steden:
            inhoud = re.sub(
                rf'(href="[^"]*{land}/){stad}(")',
                rf'\g<1>{stad}.html\2',
                inhoud
            )

    # Fix fabrikanten links
    for fab in FABRIKANTEN:
        inhoud = re.sub(
            rf'(href="[^"]*fabrikanten/){fab}(")',
            rf'\g<1>{fab}.html\2',
            inhoud
        )

    # Fix hoofdpagina links (nederland.html, europa.html etc)
    for pagina in ["nederland", "europa", "fabrikanten", "over"]:
        inhoud = re.sub(
            rf'(href="[^"]*){pagina}(")',
            rf'\g<1>{pagina}.html\2',
            inhoud
        )

    # Voorkom dubbele .html.html
    inhoud = inhoud.replace(".html.html", ".html")

    if inhoud != origineel:
        pad.write_text(inhoud, encoding="utf-8")
        return True
    return False


def main():
    print("=" * 55)
    print("  STREETSTEEL — NAVIGATIELINKS FIXER")
    print("=" * 55)

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Map niet gevonden: {WEBSITE_MAP}")
        input("\nDruk op Enter om af te sluiten...")
        return

    gefixt = 0
    ongewijzigd = 0

    # Fix alle HTML bestanden
    for html in sorted(WEBSITE_MAP.rglob("*.html")):
        # Sla admin map over
        if "admin" in str(html):
            continue
        if fix_html_bestand(html):
            gefixt += 1
            print(f"  ✅ {html.relative_to(WEBSITE_MAP)}")
        else:
            ongewijzigd += 1

    print(f"\n{'=' * 55}")
    print(f"  KLAAR!")
    print(f"  ✅ Gefixt:      {gefixt} pagina's")
    print(f"  ⏭️  Ongewijzigd: {ongewijzigd} pagina's")
    print(f"{'=' * 55}")
    print(f"\nVolgende stap: commit en push via GitHub Desktop!")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()