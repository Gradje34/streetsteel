"""
StreetSteel — Tellers op het Europa-overzicht
==============================================
Voegt aan elke landkaart in europa.html een teller-element toe en zorgt
dat fotos.js geladen wordt, zodat de kaarten het totaal aantal foto's
per land tonen (data uit data/tellers.json).

Wat het doet:
  1. Per landkaart: voegt na <h3 class="card-city">...</h3> een
     <span class="card-count photo-count" data-page="europa/<land>"></span> toe.
     De <land>-slug wordt afgeleid uit de href van de kaart.
  2. Voegt <script src="src/js/fotos.js"></script> toe vlak voor </body>
     als die er nog niet staat.

Veilig om meermaals te draaien: kaarten die de teller al hebben worden
overgeslagen.

Gebruik: python tellers_europa.py
"""

import re
from pathlib import Path

PAGINA = Path(r"C:\streetsteel\europa.html")

# Matcht een landkaart: de <h3 class="card-city">...</h3> plus een eventueel
# al aanwezige teller-<span> erna. Door die bestaande teller mee te vangen,
# kunnen we hem herkennen en het script veilig meermaals draaien.
KAART_RE = re.compile(
    r'<a\s+href="europa/(?P<slug>[^."]+)\.html"\s+class="location-card">'
    r'.*?<h3\s+class="card-city">[^<]*</h3>'
    r'(?P<bestaand>\s*<span class="card-count photo-count"[^>]*></span>)?',
    re.DOTALL,
)


def voeg_teller_toe(match):
    blok = match.group(0)
    slug = match.group("slug")
    # Staat er al een teller? Dan niets doen (idempotent).
    if match.group("bestaand"):
        return blok
    teller = (
        f'\n                    <span class="card-count photo-count" '
        f'data-page="europa/{slug}"></span>'
    )
    return blok + teller


def main():
    if not PAGINA.exists():
        print(f"FOUT: {PAGINA} niet gevonden.")
        return

    html = PAGINA.read_text(encoding="utf-8")
    origineel = html

    # 1. Tellers in de kaarten
    html, n = KAART_RE.subn(voeg_teller_toe, html)
    toegevoegd = html.count('class="card-count photo-count"') - \
        origineel.count('class="card-count photo-count"')
    print(f"Landkaarten gevonden: {n} — nieuwe tellers toegevoegd: {toegevoegd}")

    # 2. fotos.js laden (vlak voor </body>) indien nog niet aanwezig
    if "src/js/fotos.js" not in html:
        html = html.replace(
            "</body>",
            '<script src="src/js/fotos.js"></script>\n</body>',
            1,
        )
        print("fotos.js toegevoegd vlak voor </body>.")
    else:
        print("fotos.js stond er al — niets gewijzigd.")

    if html != origineel:
        PAGINA.write_text(html, encoding="utf-8")
        print("europa.html bijgewerkt.")
    else:
        print("Geen wijzigingen nodig — alles stond al goed.")


if __name__ == "__main__":
    main()
