"""
StreetSteel — Fabrikant introteksten in HTML zetten
====================================================
Leest fabrikant_data.py en vervangt in elke fabrikantpagina:
  1. De placeholder <p id="introTekst">...</p> door de echte introtekst.
  2. De verborgen website-link <a id="websiteLink" ...> krijgt de juiste
     href en wordt zichtbaar gemaakt (style display:none verwijderd),
     mits er een website is opgegeven.

Werkt alleen op fabrikanten die in INTROS staan; andere pagina's blijven
ongemoeid. Veilig om meermaals te draaien (idempotent): een pagina die de
tekst al heeft, wordt overgeslagen.

Gebruik: python fabrikant_intro.py
(fabrikant_data.py moet in dezelfde map staan.)
"""

import html as html_lib
import re
from pathlib import Path

from fabrikant_data import INTROS

FAB_MAP = Path(r"C:\streetsteel\fabrikanten")

PLACEHOLDER = "Introductietekst wordt via het beheerpaneel toegevoegd."


def verwerk_pagina(pad: Path, intro: dict) -> str:
    html = pad.read_text(encoding="utf-8")
    origineel = html
    tekst_html = html_lib.escape(intro["tekst"])

    # 1. Introtekst: vervang OF de placeholder, OF een eerder gezette tekst.
    #    Door de hele <p id="introTekst">...</p> te matchen blijft het idempotent.
    nieuwe_p = f'<p id="introTekst">{tekst_html}</p>'
    html, n_p = re.subn(
        r'<p id="introTekst">.*?</p>',
        lambda m: nieuwe_p,
        html,
        count=1,
        flags=re.DOTALL,
    )

    # 2. Website-link, alleen als er een website is opgegeven.
    website = intro.get("website", "").strip()
    if website:
        nieuwe_a = (
            f'<a href="{html_lib.escape(website)}" id="websiteLink" '
            f'class="manufacturer-website" target="_blank" rel="noopener" '
            f'data-i18n="manufacturer.website">Website fabrikant &rarr;</a>'
        )
        html, n_a = re.subn(
            r'<a href="[^"]*" id="websiteLink".*?</a>',
            lambda m: nieuwe_a,
            html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        n_a = 0

    status = "ongewijzigd"
    if html != origineel:
        pad.write_text(html, encoding="utf-8")
        status = f"tekst✔ {'website✔' if website else 'geen website'}"
    return status


def main():
    print("=" * 55)
    print("  STREETSTEEL — FABRIKANT INTROTEKSTEN")
    print("=" * 55)

    if not FAB_MAP.exists():
        print(f"FOUT: {FAB_MAP} niet gevonden.")
        return

    verwerkt = ontbreekt = 0
    for slug, intro in INTROS.items():
        pad = FAB_MAP / f"{slug}.html"
        if not pad.exists():
            print(f"  ⚠ {slug}.html niet gevonden — overgeslagen")
            ontbreekt += 1
            continue
        status = verwerk_pagina(pad, intro)
        print(f"  {slug:14} {status}")
        verwerkt += 1

    print(f"\nKlaar. {verwerkt} pagina('s) verwerkt, {ontbreekt} niet gevonden.")
    print(f"Nog {0} ... breid fabrikant_data.py uit voor meer fabrikanten.")


if __name__ == "__main__":
    main()
