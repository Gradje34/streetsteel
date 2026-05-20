"""
StreetSteel — Fototeller bijwerken
===================================
Dit script telt alle foto's per map en schrijft
de aantallen weg naar main.js zodat de website
automatisch de juiste tellers toont.

Gebruik: python update_tellers.py
Draai dit na elke keer dat je nieuwe foto's toevoegt.
"""

import os
import json
import re
from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
FOTOS_MAP    = Path(r"M:\Streetsteel.com\fotos")
WEBSITE_MAP  = Path(r"M:\Streetsteel.com\website")
MAIN_JS      = WEBSITE_MAP / "src" / "js" / "main.js"

FOTO_EXTENSIES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ── FUNCTIES ──────────────────────────────────────────────────

def tel_fotos(map_pad):
    """Tel het aantal foto's in een map (niet recursief)."""
    if not map_pad.exists():
        return 0
    return sum(
        1 for f in map_pad.iterdir()
        if f.is_file() and f.suffix.lower() in FOTO_EXTENSIES
    )


def bouw_teller_dict():
    """Bouw een dict op met alle paden en hun fotaantallen."""
    tellers = {}

    # Nederland steden
    nl_map = FOTOS_MAP / "nederland"
    if nl_map.exists():
        for stad in nl_map.iterdir():
            if stad.is_dir():
                sleutel = f"nederland/{stad.name}"
                tellers[sleutel] = tel_fotos(stad)

    # Europa landen en steden
    europa_map = FOTOS_MAP / "europa"
    if europa_map.exists():
        for land in europa_map.iterdir():
            if land.is_dir():
                # Controleer of er direct foto's in het land staan
                directe_fotos = tel_fotos(land)
                if directe_fotos > 0:
                    tellers[f"europa/{land.name}"] = directe_fotos

                # Steden binnen het land
                for stad in land.iterdir():
                    if stad.is_dir():
                        sleutel = f"europa/{land.name}/{stad.name}"
                        tellers[sleutel] = tel_fotos(stad)

    # Fabrikanten A-M
    fab_am = FOTOS_MAP / "fabrikanten-a-m"
    if fab_am.exists():
        for fab in fab_am.iterdir():
            if fab.is_dir():
                tellers[f"fabrikanten-a-m/{fab.name}"] = tel_fotos(fab)

    # Fabrikanten N-Z
    fab_nz = FOTOS_MAP / "fabrikanten-n-z"
    if fab_nz.exists():
        for fab in fab_nz.iterdir():
            if fab.is_dir():
                tellers[f"fabrikanten-n-z/{fab.name}"] = tel_fotos(fab)

    return tellers


def update_main_js(tellers):
    """Schrijf de tellers weg in main.js."""
    if not MAIN_JS.exists():
        print(f"❌ main.js niet gevonden op: {MAIN_JS}")
        return False

    inhoud = MAIN_JS.read_text(encoding="utf-8")

    # Bouw nieuwe PHOTO_COUNTS dict op
    regels = ["const PHOTO_COUNTS = {"]
    for sleutel, aantal in sorted(tellers.items()):
        regels.append(f'    "{sleutel}": {aantal},')
    regels.append("};")
    nieuwe_dict = "\n".join(regels)

    # Vervang bestaande PHOTO_COUNTS in het bestand
    patroon = r"const PHOTO_COUNTS = \{[^}]*\};"
    if re.search(patroon, inhoud, re.DOTALL):
        nieuwe_inhoud = re.sub(patroon, nieuwe_dict, inhoud, flags=re.DOTALL)
        MAIN_JS.write_text(nieuwe_inhoud, encoding="utf-8")
        return True
    else:
        print("⚠️  PHOTO_COUNTS niet gevonden in main.js — handmatig controleren")
        return False


def druk_rapport(tellers):
    """Toon een overzicht van alle tellers."""
    print("\n📊 FOTOTELLERS OVERZICHT")
    print("=" * 50)

    totaal = 0
    categorie = ""

    for sleutel, aantal in sorted(tellers.items()):
        # Categorie header
        cat = sleutel.split("/")[0]
        if cat != categorie:
            print(f"\n  [{cat.upper()}]")
            categorie = cat

        # Inspringen op basis van diepte
        diepte = sleutel.count("/")
        spaties = "    " * diepte
        naam = sleutel.split("/")[-1]

        status = "✅" if aantal > 0 else "⚠️ "
        print(f"  {spaties}{status} {naam}: {aantal} foto('s)")
        totaal += aantal

    print(f"\n{'=' * 50}")
    print(f"  TOTAAL: {totaal} foto's")
    print(f"{'=' * 50}\n")


# ── HOOFDPROGRAMMA ────────────────────────────────────────────

def main():
    print("=" * 50)
    print("  STREETSTEEL — FOTOTELLER BIJWERKEN")
    print("=" * 50)

    # Controleer of QNAP bereikbaar is
    if not FOTOS_MAP.exists():
        print(f"\n❌ Fotomap niet bereikbaar: {FOTOS_MAP}")
        print("   Controleer of je QNAP (M:) verbonden is.")
        input("\nDruk op Enter om af te sluiten...")
        return

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Websitemap niet bereikbaar: {WEBSITE_MAP}")
        print("   Controleer of M:\\Streetsteel.com\\website bestaat.")
        input("\nDruk op Enter om af te sluiten...")
        return

    print("\n🔍 Foto's tellen per pagina...")
    tellers = bouw_teller_dict()

    druk_rapport(tellers)

    print("📝 Tellers wegschrijven naar main.js...")
    if update_main_js(tellers):
        print("✅ main.js succesvol bijgewerkt!")
        print(f"\n   Vergeet niet de website opnieuw te uploaden naar Netlify")
        print(f"   zodat de nieuwe tellers live gaan.")
    else:
        print("❌ Bijwerken mislukt — zie melding hierboven.")

    # Sla ook een JSON kopie op voor de backup
    json_pad = WEBSITE_MAP / "_data" / "fototellers.json"
    json_pad.parent.mkdir(parents=True, exist_ok=True)
    json_pad.write_text(
        json.dumps(tellers, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"💾 Backup opgeslagen: {json_pad}")

    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()
