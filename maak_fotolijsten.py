"""
StreetSteel — Fotolijst Generator
===================================
Dit script maakt per stad/land/fabrikant een JSON bestand
met de lijst van alle foto's. De website leest dit JSON
bestand om de foto's automatisch te tonen.

Gebruik: python maak_fotolijsten.py
Draai dit na elke keer dat je nieuwe foto's toevoegt.
"""

import os
import json
import re
from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
FOTOS_MAP   = Path(r"C:\streetsteel\fotos")
WEBSITE_MAP = Path(r"C:\streetsteel")
DATA_MAP    = WEBSITE_MAP / "data"

FOTO_EXTENSIES = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

# ── FUNCTIES ──────────────────────────────────────────────────

def maak_fotolijst(map_pad, web_pad):
    """Maak een lijst van foto-URLs voor een gegeven map."""
    if not map_pad.exists():
        return []
    fotos = []
    for f in sorted(map_pad.iterdir()):
        if f.is_file() and f.suffix.lower() in FOTO_EXTENSIES:
            fotos.append(f"/{web_pad}/{f.name}")
    return fotos


def schrijf_json(pad, data):
    """Schrijf data naar een JSON bestand."""
    pad.parent.mkdir(parents=True, exist_ok=True)
    pad.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )



def werk_hero_fallback_bij(totaal_fotos):
    """Werk het fallback-getal id="totaalFotos" in index.html bij.

    Het live getal wordt door fotos.js gezet; dit is alleen de fallback
    voor als JavaScript niet laadt. Naar beneden afgerond op 50, met "+".
    """
    index_pad = WEBSITE_MAP / "index.html"
    if not index_pad.exists():
        print("  ⚠️  index.html niet gevonden, fallback niet bijgewerkt.")
        return
    afgerond = (totaal_fotos // 10) * 10
    html = index_pad.read_text(encoding="utf-8")
    nieuw, n = re.subn(
        r'(<span class="stat-num" id="totaalFotos">)[^<]*(</span>)',
        rf'\g<1>{afgerond}+\g<2>',
        html,
    )
    if n == 0:
        print('  ⚠️  id="totaalFotos" niet gevonden in index.html.')
        return
    index_pad.write_text(nieuw, encoding="utf-8")
    print(f"  ✅ Hero-fallback bijgewerkt: {afgerond}+")


# ── HOOFDPROGRAMMA ────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  STREETSTEEL — FOTOLIJST GENERATOR")
    print("=" * 55)

    if not FOTOS_MAP.exists():
        print(f"\n❌ Fotomap niet bereikbaar: {FOTOS_MAP}")
        print("   Controleer of je QNAP (M:) verbonden is.")
        input("\nDruk op Enter om af te sluiten...")
        return

    DATA_MAP.mkdir(parents=True, exist_ok=True)
    totaal = 0
    alle_tellers = {}

    # ── NEDERLAND ────────────────────────────────────────────
    print("\n🇳🇱 Nederland...")
    nl_map = FOTOS_MAP / "nederland"
    if nl_map.exists():
        for stad in sorted(nl_map.iterdir()):
            if stad.is_dir():
                web_pad = f"fotos/nederland/{stad.name}"
                fotos = maak_fotolijst(stad, web_pad)
                sleutel = f"nederland/{stad.name}"
                alle_tellers[sleutel] = len(fotos)

                json_pad = DATA_MAP / "nederland" / f"{stad.name}.json"
                schrijf_json(json_pad, {"fotos": fotos, "aantal": len(fotos)})
                totaal += 1
                print(f"  ✅ {sleutel}: {len(fotos)} foto('s)")

    # ── EUROPA ───────────────────────────────────────────────
    print("\n🌍 Europa...")
    europa_map = FOTOS_MAP / "europa"
    if europa_map.exists():
        for land in sorted(europa_map.iterdir()):
            if land.is_dir():
                # Directe foto's in het land
                web_pad = f"fotos/europa/{land.name}"
                fotos = maak_fotolijst(land, web_pad)
                if fotos:
                    sleutel = f"europa/{land.name}"
                    alle_tellers[sleutel] = len(fotos)
                    json_pad = DATA_MAP / "europa" / f"{land.name}.json"
                    schrijf_json(json_pad, {"fotos": fotos, "aantal": len(fotos)})
                    totaal += 1
                    print(f"  ✅ {sleutel}: {len(fotos)} foto('s)")

                # Steden binnen het land
                for stad in sorted(land.iterdir()):
                    if stad.is_dir():
                        web_pad = f"fotos/europa/{land.name}/{stad.name}"
                        fotos = maak_fotolijst(stad, web_pad)
                        sleutel = f"europa/{land.name}/{stad.name}"
                        alle_tellers[sleutel] = len(fotos)

                        json_pad = DATA_MAP / "europa" / land.name / f"{stad.name}.json"
                        schrijf_json(json_pad, {"fotos": fotos, "aantal": len(fotos)})
                        totaal += 1
                        print(f"  ✅ {sleutel}: {len(fotos)} foto('s)")

    # ── FABRIKANTEN ──────────────────────────────────────────
    print("\n🏭 Fabrikanten...")
    for fab_map_naam in ["fabrikanten-a-m", "fabrikanten-n-z"]:
        fab_map = FOTOS_MAP / fab_map_naam
        if fab_map.exists():
            for fab in sorted(fab_map.iterdir()):
                if fab.is_dir():
                    web_pad = f"fotos/{fab_map_naam}/{fab.name}"
                    fotos = maak_fotolijst(fab, web_pad)
                    sleutel = f"fabrikanten/{fab.name}"
                    alle_tellers[sleutel] = len(fotos)

                    json_pad = DATA_MAP / "fabrikanten" / f"{fab.name}.json"
                    schrijf_json(json_pad, {"fotos": fotos, "aantal": len(fotos)})
                    totaal += 1
                    print(f"  ✅ {sleutel}: {len(fotos)} foto('s)")

    # ── OVERZICHT JSON ───────────────────────────────────────
    # Schrijf alle tellers naar één overzichtsbestand
    schrijf_json(DATA_MAP / "tellers.json", alle_tellers)
    print(f"\n✅ Tellers overzicht: data/tellers.json")

    # Werk het fallback-getal in de homepage-hero bij.
    # Let op: telt bewust alleen nederland/europa (unieke foto's). Foto's
    # onder fabrikanten/ zijn dezelfde foto's nogmaals gecategoriseerd per
    # fabrikant, dus die NIET meetellen — anders telt elke foto dubbel.
    totaal_fotos = sum(
        v for k, v in alle_tellers.items() if not k.startswith("fabrikanten/")
    )
    werk_hero_fallback_bij(totaal_fotos)
    print(f"\n📸 Totaal aantal unieke foto's (excl. fabrikant-duplicaten): {totaal_fotos}")

    # ── EINDRAPPORT ──────────────────────────────────────────
    print(f"\n{'=' * 55}")
    print(f"  KLAAR!")
    print(f"  ✅ JSON bestanden aangemaakt: {totaal}")
    print(f"  📁 Opgeslagen in: {DATA_MAP}")
    print(f"\nVolgende stap: commit en push via GitHub Desktop!")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()
