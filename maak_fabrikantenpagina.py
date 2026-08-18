#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
StreetSteel — Fabrikantenpagina Generator
============================================
Genereert de A-Z-navigatiebalk EN het fabrikanten-overzicht (tegels) op
fabrikanten.html vanuit EEN enkele lijst hieronder (FABRIKANTEN_NAMEN).
Zo kunnen de tegels en de A-Z-balk nooit meer los van elkaar raken —
eerder ontstond precies dat probleem (P.Konings en Globe stonden wel als
tegel, maar niet in de A-Z-lijst) omdat beide blokken met de hand apart
werden bijgehouden.

Gebruik: python maak_fabrikantenpagina.py
Draai dit nadat je een fabrikant hebt toegevoegd, hernoemd of verwijderd
(via het beheerpaneel of handmatig), vlak voor je commit/pusht.

Werkwijze:
1. Voeg de nieuwe fabrikant-slug toe aan FABRIKANTEN_NAMEN hieronder, met
   de exacte weergavenaam (hoofdletters/leestekens zoals "AVK", "B-OZ",
   "P.Konings" kunnen niet automatisch worden afgeleid uit de slug).
2. Draai dit script. Het:
   - Waarschuwt als er een map onder fotos/fabrikanten-a-m of
     fotos/fabrikanten-n-z bestaat die nog niet in FABRIKANTEN_NAMEN staat
     (of andersom: een naam in de lijst zonder bijbehorende fotomap).
   - Herschrijft het A-Z-blok en het tegel-overzicht in fabrikanten.html
     tussen de AUTO-GENERATED-markers, in alfabetische volgorde op naam.
   - Werkt de "NN+ producenten"-tekst in de pagina-hero bij.

Andere delen van fabrikanten.html (header, footer, CSS, hero) blijven
onaangeroerd — dit script vervangt alleen de twee gemarkeerde blokken.
"""

import re
import sys
from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
WEBSITE_MAP = Path(r"C:\streetsteel")
FABRIKANTEN_HTML = WEBSITE_MAP / "fabrikanten.html"
FOTOS_MAP = WEBSITE_MAP / "fotos"
FABRIKANTEN_FOTOMAPPEN = ["fabrikanten-a-m", "fabrikanten-n-z"]

# ── BRONLIJST: slug -> weergavenaam ─────────────────────────────
# Dit is de ENIGE plek waar fabrikantnamen voor de overzichtspagina worden
# ingesteld. Voeg hier je nieuwe fabrikant toe (slug moet overeenkomen met
# de mapnaam onder fotos/fabrikanten-a-m of fotos/fabrikanten-n-z, en met
# de bestandsnaam fabrikanten/<slug>.html).
FABRIKANTEN_NAMEN = {
    "alphacan": "Alphacan",
    "aquafix": "Aquafix",
    "aquagate": "Aquagate",
    "aqauway": "Aquaway",
    "avk": "AVK",
    "b-oz": "B-OZ",
    "de-globe": "De Globe",
    "de-leidinggroothandel": "De Leidinggroothandel",
    "delta-plast": "Delta Plast",
    "dijg": "DIJG",
    "draka-polva": "Draka Polva",
    "dyka": "Dyka",
    "ewe": "EWE",
    "fibrelita": "Fibrelita",
    "fmh-pompservice": "FMH Pompservice",
    "frelu": "Frelu",
    "friand": "Friand",
    "geertsema": "Geertsema",
    "globe": "Globe",
    "hauraton": "Hauraton",
    "hermelock": "Hermelock",
    "joosten": "Joosten",
    "kamphuis": "Kamphuis",
    "kb": "KB",
    "kessel": "Kessel",
    "ksk": "KSK",
    "landustrie": "Landustrie",
    "lhs": "LHS",
    "lovink": "Lovink",
    "martens": "Martens",
    "meijer": "Meijer",
    "milder": "Milder",
    "mous": "Mous",
    "natuurbeton-milieu": "Natuurbeton Milieu",
    "neering-bogel": "Neering Bogel",
    "nki": "NKI",
    "norinco": "Norinco",
    "nyloplast": "Nyloplast",
    "mij-onbekende-producent-en": "Onbekende producenten",
    "oogink": "Oogink",
    "p-konings": "P.Konings",
    "pam": "PAM",
    "passevant": "Passevant",
    "pipelife": "Pipelife",
    "poly": "Poly",
    "samson": "Samson",
    "sotra": "Sotra",
    "stora": "Stora",
    "stradus": "Stradus",
    "strucom": "Strucom",
    "tbs": "TBS",
    "thijssen": "Thijssen",
    "topatec": "Topatec",
    "van-der-velden": "Van der Velden",
    "veko": "Veko",
    "vulcanus": "Vulcanus",
    "w-ten-cate": "W. ten Cate",
    "waprog": "Waprog",
    "waterleiding-mij-prov-groningen": "Waterleiding Mij. Prov. Groningen",
    "wavin": "Wavin",
    "weegels": "Weegels",
}

AZBAR_START = "<!-- AUTO-GENERATED:AZBAR:START (bron: maak_fabrikantenpagina.py, niet handmatig bewerken) -->"
AZBAR_END = "<!-- AUTO-GENERATED:AZBAR:END -->"
GRID_START = "<!-- AUTO-GENERATED:GRID:START (bron: maak_fabrikantenpagina.py, niet handmatig bewerken) -->"
GRID_END = "<!-- AUTO-GENERATED:GRID:END -->"


def controleer_op_afwijkingen():
    """Vergelijk FABRIKANTEN_NAMEN met de mappen die echt op schijf staan."""
    slugs_op_schijf = set()
    for mapnaam in FABRIKANTEN_FOTOMAPPEN:
        fab_map = FOTOS_MAP / mapnaam
        if fab_map.exists():
            slugs_op_schijf |= {p.name for p in fab_map.iterdir() if p.is_dir()}

    slugs_in_lijst = set(FABRIKANTEN_NAMEN.keys())

    ontbrekend = sorted(slugs_op_schijf - slugs_in_lijst)
    overtollig = sorted(slugs_in_lijst - slugs_op_schijf)

    if ontbrekend:
        print("\n⚠️  Deze mappen staan op schijf maar NIET in FABRIKANTEN_NAMEN:")
        for slug in ontbrekend:
            print(f"     - {slug}  (voeg toe aan FABRIKANTEN_NAMEN met de juiste weergavenaam)")
    if overtollig:
        print("\n⚠️  Deze namen staan in FABRIKANTEN_NAMEN maar hebben GEEN fotomap:")
        for slug in overtollig:
            print(f"     - {slug}  (typefout, of de map is verwijderd/hernoemd?)")
    if not ontbrekend and not overtollig:
        print("\n✅ FABRIKANTEN_NAMEN komt overeen met de mappen op schijf.")

    return ontbrekend, overtollig


def bouw_azbar(gesorteerd):
    """Bouw de A-Z-balk: elke letter A-Z, leeg of met flyout-links."""
    regels = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        items = [(s, n) for s, n in gesorteerd if n[:1].upper() == letter]
        if items:
            links = "".join(
                f'<a href="fabrikanten/{s}.html" class="az-flyout-item">{n}</a>'
                for s, n in items
            )
            regels.append(
                f'            <div class="az-letter" tabindex="0">'
                f'<span class="az-letter-label">{letter}</span>'
                f'<div class="az-flyout">{links}</div></div>'
            )
        else:
            regels.append(
                f'            <div class="az-letter az-letter--empty">'
                f'<span class="az-letter-label">{letter}</span></div>'
            )
    return "\n".join(regels)


def bouw_grid(gesorteerd):
    """Bouw de doorlopende, alfabetische tegel-lijst (geen A-M/N-Z-scheiding meer)."""
    regels = []
    for slug, naam in gesorteerd:
        regels.append(
            f'            <a href="fabrikanten/{slug}.html" class="manufacturer-item">'
            f'<span class="manufacturer-name">{naam}</span>'
            f'<span class="manufacturer-arrow">→</span></a>'
        )
    return "\n".join(regels)


def vervang_blok(html, start_marker, end_marker, nieuwe_inhoud):
    patroon = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker), re.DOTALL
    )
    vervanging = f"{start_marker}\n{nieuwe_inhoud}\n        {end_marker}"
    nieuw_html, n = patroon.subn(vervanging, html)
    if n == 0:
        sys.exit(
            f"❌ Marker '{start_marker}' niet gevonden in fabrikanten.html.\n"
            "   De structuur van het bestand is aangepast — pas de markers "
            "handmatig aan of herstel ze."
        )
    return nieuw_html


def main():
    print("=" * 55)
    print("  STREETSTEEL — FABRIKANTENPAGINA GENERATOR")
    print("=" * 55)

    if not FABRIKANTEN_HTML.exists():
        sys.exit(f"❌ Bestand niet gevonden: {FABRIKANTEN_HTML}")

    controleer_op_afwijkingen()

    gesorteerd = sorted(FABRIKANTEN_NAMEN.items(), key=lambda kv: kv[1].lower())

    html = FABRIKANTEN_HTML.read_text(encoding="utf-8")
    html = vervang_blok(html, AZBAR_START, AZBAR_END, bouw_azbar(gesorteerd))
    html = vervang_blok(html, GRID_START, GRID_END, bouw_grid(gesorteerd))

    # Werk het aantal producenten in de hero bij.
    aantal = len(gesorteerd)
    html, n = re.subn(
        r'(<span>)\d+\+?( producenten</span>)', rf'\g<1>{aantal}+\g<2>', html
    )
    if n == 0:
        print('  ⚠️  "producenten"-tekst niet gevonden in de hero, niet bijgewerkt.')

    FABRIKANTEN_HTML.write_text(html, encoding="utf-8")

    print(f"\n✅ fabrikanten.html bijgewerkt: {aantal} fabrikanten, A-Z-balk en tegels synchroon.")
    print("\nVolgende stap: lokaal testen, dan commit/push/deploy.")


if __name__ == "__main__":
    main()
