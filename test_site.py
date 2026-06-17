"""
StreetSteel — Site Tester
==========================
Test alle pagina's van streetsteel.eu en geeft een rapport
van welke pagina's werken en welke een fout geven.

Gebruik: python test_site.py
"""

import requests
from datetime import datetime

BASE_URL = "https://streetsteel.eu"

ALLE_PAGINAS = [
    # Hoofdpagina's
    "/",
    "/nederland",
    "/europa",
    "/fabrikanten",
    "/over",

    # Nederland steden
    "/nederland/amsterdam",
    "/nederland/apeldoorn",
    "/nederland/delfzijl",
    "/nederland/eindhoven",
    "/nederland/emmen",
    "/nederland/groningen",
    "/nederland/harderwijk",
    "/nederland/helmond",
    "/nederland/hoogezand",
    "/nederland/lelystad",
    "/nederland/veendam",
    "/nederland/winschoten",

    # Europa landen
    "/europa/denemarken",
    "/europa/duitsland",
    "/europa/frankrijk",
    "/europa/hongarije",
    "/europa/italie",
    "/europa/kosovo",
    "/europa/kroatie",
    "/europa/macedonie",
    "/europa/noorwegen",
    "/europa/oostenrijk",
    "/europa/portugal",
    "/europa/schotland",
    "/europa/slowakije",
    "/europa/spanje",
    "/europa/zweden",

    # Europa steden
    "/europa/denemarken/korsor",
    "/europa/duitsland/bad-neuenahr-ahrweiler",
    "/europa/duitsland/berlijn",
    "/europa/duitsland/hohn",
    "/europa/duitsland/hohenschwangau",
    "/europa/duitsland/kavelaer",
    "/europa/duitsland/kiel",
    "/europa/duitsland/kornau",
    "/europa/duitsland/leer",
    "/europa/duitsland/oberhausen",
    "/europa/duitsland/oldenburg",
    "/europa/duitsland/riezlern",
    "/europa/hongarije/boedapest",
    "/europa/italie/como",
    "/europa/italie/sicilie",
    "/europa/noorwegen/bearums-verk",
    "/europa/noorwegen/bergen",
    "/europa/noorwegen/flaam",
    "/europa/noorwegen/honningsvaag",
    "/europa/noorwegen/kristiansand",
    "/europa/noorwegen/molde",
    "/europa/noorwegen/olden",
    "/europa/noorwegen/oslo",
    "/europa/noorwegen/stavanger",
    "/europa/noorwegen/tromsoe",
    "/europa/slowakije/bratislava",
    "/europa/spanje/cordoba",
    "/europa/spanje/granada",
    "/europa/spanje/nerja",
    "/europa/spanje/udeba",
    "/europa/zweden/goeteborg",
    "/europa/zweden/malmoe",
    "/europa/zweden/nordby",

    # Fabrikanten
    "/fabrikanten/alphacan",
    "/fabrikanten/aquagate",
    "/fabrikanten/aquafix",
    "/fabrikanten/aqauway",
    "/fabrikanten/avk",
    "/fabrikanten/b-oz",
    "/fabrikanten/de-globe",
    "/fabrikanten/de-leidinggroothandel",
    "/fabrikanten/delta-plast",
    "/fabrikanten/dijg",
    "/fabrikanten/draka-polva",
    "/fabrikanten/dyka",
    "/fabrikanten/ewe",
    "/fabrikanten/fibrelita",
    "/fabrikanten/fmh-pompservice",
    "/fabrikanten/frelu",
    "/fabrikanten/friand",
    "/fabrikanten/geertsema",
    "/fabrikanten/hauraton",
    "/fabrikanten/hermelock",
    "/fabrikanten/joosten",
    "/fabrikanten/kamphuis",
    "/fabrikanten/kb",
    "/fabrikanten/kessel",
    "/fabrikanten/ksk",
    "/fabrikanten/landustrie",
    "/fabrikanten/lhs",
    "/fabrikanten/lovink",
    "/fabrikanten/martens",
    "/fabrikanten/meijer",
    "/fabrikanten/milder",
    "/fabrikanten/mous",
    "/fabrikanten/natuurbeton-milieu",
    "/fabrikanten/neering-bogel",
    "/fabrikanten/nki",
    "/fabrikanten/norinco",
    "/fabrikanten/nyloplast",
    "/fabrikanten/oogink",
    "/fabrikanten/pam",
    "/fabrikanten/passevant",
    "/fabrikanten/pipelife",
    "/fabrikanten/poly",
    "/fabrikanten/samson",
    "/fabrikanten/sotra",
    "/fabrikanten/stora",
    "/fabrikanten/stradus",
    "/fabrikanten/strucom",
    "/fabrikanten/tbs",
    "/fabrikanten/thijssen",
    "/fabrikanten/topatec",
    "/fabrikanten/van-der-velden",
    "/fabrikanten/veko",
    "/fabrikanten/vulcanus",
    "/fabrikanten/w-ten-cate",
    "/fabrikanten/waprog",
    "/fabrikanten/waterleiding-mij-prov-groningen",
    "/fabrikanten/wavin",
    "/fabrikanten/weegels",
    "/fabrikanten/mij-onbekende-producent-en",

    # Data JSON bestanden
    "/data/nederland/groningen.json",
    "/data/nederland/veendam.json",
    "/data/europa/noorwegen/oslo.json",
    "/data/europa/denemarken/korsor.json",
    "/data/tellers.json",
]

def test_pagina(url, sessie):
    """Test één pagina en geef de statuscode terug."""
    try:
        r = sessie.get(url, timeout=10, allow_redirects=True)
        return r.status_code
    except Exception as e:
        return f"FOUT: {e}"

def main():
    print("=" * 60)
    print("  STREETSTEEL.EU — SITE TESTER")
    print(f"  {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    print("=" * 60)
    print(f"\n🌐 {len(ALLE_PAGINAS)} pagina's testen...\n")

    sessie = requests.Session()
    sessie.headers.update({"User-Agent": "Mozilla/5.0 StreetSteel-Tester"})

    ok = []
    fouten = []

    for pad in ALLE_PAGINAS:
        url = BASE_URL + pad
        status = test_pagina(url, sessie)

        if status == 200:
            ok.append(pad)
            print(f"  ✅ {pad}")
        else:
            fouten.append((pad, status))
            print(f"  ❌ {pad} → {status}")

    # Eindrapport
    print(f"\n{'=' * 60}")
    print(f"  EINDRAPPORT")
    print(f"{'=' * 60}")
    print(f"  ✅ Werkt:   {len(ok)} pagina's")
    print(f"  ❌ Fouten:  {len(fouten)} pagina's")

    if fouten:
        print(f"\n  PAGINA'S MET FOUTEN:")
        for pad, status in fouten:
            print(f"  ❌ {pad} → {status}")

    # Sla rapport op
    rapport_pad = "C:\\streetsteel\\test_rapport.txt"
    with open(rapport_pad, "w", encoding="utf-8") as f:
        f.write(f"STREETSTEEL.EU — SITE TEST RAPPORT\n")
        f.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M')}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Totaal getest: {len(ALLE_PAGINAS)}\n")
        f.write(f"Werkt: {len(ok)}\n")
        f.write(f"Fouten: {len(fouten)}\n\n")
        if fouten:
            f.write("PAGINA'S MET FOUTEN:\n")
            for pad, status in fouten:
                f.write(f"  {pad} → {status}\n")

    print(f"\n  📋 Rapport opgeslagen: {rapport_pad}")
    input("\nDruk op Enter om af te sluiten...")

if __name__ == "__main__":
    main()
