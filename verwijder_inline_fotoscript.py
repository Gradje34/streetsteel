"""
StreetSteel — Verwijder verouderd inline foto-script (nederland)
================================================================
De 12 pagina's in nederland/ bevatten een oud inline <script>-blok dat
de fotomap als HTML-mapindex probeert op te halen:

    fetch("/fotos/nederland/<stad>/")

Dat werkt op een lokale python-server (die een mapindex teruggeeft),
maar NIET op Netlify (404). De moderne fotos.js laadt de foto's correct
via de JSON in /data/, dus het oude blok kan weg.

Dit script verwijdert per nederland-pagina het inline <script>-blok dat
begint met de comment "Laad foto's automatisch uit de fotos map" tot en
met de bijbehorende </script>. De regel <script src="../src/js/fotos.js">
blijft staan.

Veilig om meermaals te draaien: een pagina zonder het blok wordt overgeslagen.

Gebruik: python verwijder_inline_fotoscript.py
"""

import re
from pathlib import Path

NL_MAP = Path(r"C:\streetsteel\nederland")

# Matcht het volledige oude inline scriptblok. Anker op de unieke comment
# zodat we nooit per ongeluk een ander <script> raken.
BLOK_RE = re.compile(
    r'<script>\s*\n?\s*document\.addEventListener\("DOMContentLoaded".*?'
    r'Laad foto\'s automatisch uit de fotos map.*?</script>\s*\n?',
    re.DOTALL,
)


def main():
    if not NL_MAP.exists():
        print(f"FOUT: {NL_MAP} niet gevonden.")
        return

    verwijderd = overgeslagen = 0
    for pagina in sorted(NL_MAP.glob("*.html")):
        html = pagina.read_text(encoding="utf-8")
        nieuw, n = BLOK_RE.subn("", html)
        if n > 0:
            pagina.write_text(nieuw, encoding="utf-8")
            print(f"  {pagina.name}: oud inline-blok verwijderd")
            verwijderd += 1
        else:
            print(f"  {pagina.name}: geen blok gevonden (al schoon)")
            overgeslagen += 1

    print(f"\nKlaar. {verwijderd} opgeschoond, {overgeslagen} overgeslagen.")
    print("De foto's laden nu uitsluitend via fotos.js (JSON), net als de "
          "europa- en fabrikantpagina's.")


if __name__ == "__main__":
    main()
