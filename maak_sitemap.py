"""
StreetSteel — Sitemap generator
================================
Doorzoekt C:\\streetsteel naar alle HTML-pagina's en schrijft een
sitemap.xml met schone URLs (zonder .html, want netlify.toml leidt
die door). Sluit automatisch uit:
  - de 15 dubbele land/land.html pagina's (bijv. europa/duitsland/duitsland.html),
    want de echte staat in europa/duitsland.html
  - admin/ en andere niet-inhoudelijke mappen

Veilig om meermaals te draaien: overschrijft sitemap.xml.
Draai opnieuw als je pagina's toevoegt of verwijdert.

Gebruik: python maak_sitemap.py
"""

from datetime import date
from pathlib import Path

WEBSITE_MAP = Path(r"C:\streetsteel")
DOMEIN = "https://streetsteel.eu"

# Mappen die NIET in de sitemap horen
NEGEER_MAPPEN = {"admin", "src", "data", "_data", "fotos", "files",
                 "node_modules", ".git", "__pycache__", "streetsteel", "website"}


def is_land_duplicaat(rel_pad: Path) -> bool:
    """europa/duitsland/duitsland.html -> True (dubbele landpagina)."""
    delen = rel_pad.with_suffix("").parts  # zonder .html
    return (len(delen) == 3 and delen[0] == "europa"
            and delen[1] == delen[2])


def schone_url(rel_pad: Path) -> str:
    """index.html -> /, overige -> /pad/zonder/.html"""
    zonder = rel_pad.with_suffix("").as_posix()
    if zonder == "index":
        return f"{DOMEIN}/"
    return f"{DOMEIN}/{zonder}"


def main():
    if not WEBSITE_MAP.exists():
        print(f"FOUT: {WEBSITE_MAP} niet gevonden.")
        return

    urls = []
    for html in sorted(WEBSITE_MAP.rglob("*.html")):
        rel = html.relative_to(WEBSITE_MAP)
        # Sla bestanden in genegeerde mappen over
        if any(deel in NEGEER_MAPPEN for deel in rel.parts[:-1]):
            continue
        # Sla de dubbele land/land.html pagina's over
        if is_land_duplicaat(rel):
            continue
        urls.append(schone_url(rel))

    vandaag = date.today().isoformat()
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        regels.append("  <url>")
        regels.append(f"    <loc>{url}</loc>")
        regels.append(f"    <lastmod>{vandaag}</lastmod>")
        regels.append("  </url>")
    regels.append("</urlset>")

    uitvoer = WEBSITE_MAP / "sitemap.xml"
    uitvoer.write_text("\n".join(regels) + "\n", encoding="utf-8")
    print(f"sitemap.xml geschreven met {len(urls)} URLs.")


if __name__ == "__main__":
    main()
