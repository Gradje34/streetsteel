"""
StreetSteel — fotos.js Toevoegen aan HTML Pagina's
====================================================
Dit script voegt de fotos.js script tag toe aan alle
HTML pagina's in nederland/, europa/ en fabrikanten/.

Gebruik: python voeg_fotosjs_toe.py
"""

from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
WEBSITE_MAP = Path(r"c:\streetsteel")

MAPPEN = ["nederland", "europa", "fabrikanten"]

# ── FUNCTIES ──────────────────────────────────────────────────

def voeg_toe(html_pad, diepte):
    """Voeg fotos.js toe aan een HTML bestand als het er nog niet in zit."""
    inhoud = html_pad.read_text(encoding="utf-8")

    # Al toegevoegd?
    if "fotos.js" in inhoud:
        return "overgeslagen"

    # Bepaal relatief pad naar src/js/ op basis van diepte
    prefix = "../" * diepte
    script_tag = f'<script src="{prefix}src/js/fotos.js"></script>'

    # Voeg toe vlak voor </body>
    if "</body>" in inhoud:
        nieuwe_inhoud = inhoud.replace("</body>", f"{script_tag}\n</body>")
        html_pad.write_text(nieuwe_inhoud, encoding="utf-8")
        return "toegevoegd"
    else:
        return "mislukt"


# ── HOOFDPROGRAMMA ────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  STREETSTEEL — FOTOS.JS TOEVOEGEN")
    print("=" * 55)

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Map niet gevonden: {WEBSITE_MAP}")
        input("\nDruk op Enter om af te sluiten...")
        return

    toegevoegd  = 0
    overgeslagen = 0
    mislukt     = 0

    for map_naam in MAPPEN:
        map_pad = WEBSITE_MAP / map_naam
        if not map_pad.exists():
            continue

        print(f"\n📁 {map_naam}/")

        # HTML bestanden in de hoofdmap (bijv. europa/noorwegen.html)
        for html in sorted(map_pad.glob("*.html")):
            diepte = 1  # één niveau diep
            resultaat = voeg_toe(html, diepte)
            if resultaat == "toegevoegd":
                toegevoegd += 1
                print(f"  ✅ {map_naam}/{html.name}")
            elif resultaat == "overgeslagen":
                overgeslagen += 1
            else:
                mislukt += 1
                print(f"  ❌ {map_naam}/{html.name}")

        # HTML bestanden in submappen (bijv. europa/noorwegen/oslo.html)
        for submap in sorted(map_pad.iterdir()):
            if submap.is_dir():
                for html in sorted(submap.glob("*.html")):
                    diepte = 2  # twee niveaus diep
                    resultaat = voeg_toe(html, diepte)
                    if resultaat == "toegevoegd":
                        toegevoegd += 1
                        print(f"  ✅ {map_naam}/{submap.name}/{html.name}")
                    elif resultaat == "overgeslagen":
                        overgeslagen += 1
                    else:
                        mislukt += 1
                        print(f"  ❌ {map_naam}/{submap.name}/{html.name}")

    print(f"\n{'=' * 55}")
    print(f"  KLAAR!")
    print(f"  ✅ fotos.js toegevoegd: {toegevoegd} pagina's")
    print(f"  ⏭️  Al aanwezig:        {overgeslagen} pagina's")
    print(f"  ❌ Mislukt:            {mislukt} pagina's")
    print(f"{'=' * 55}")
    print(f"\nVolgende stap: commit en push via GitHub Desktop!")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()