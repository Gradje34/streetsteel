"""
straat-staal.jouwweb.nl - Foto Downloader
==========================================
Dit script downloadt automatisch alle foto's van jouw JouwWeb site
en slaat ze op in een nette mappenstructuur.

Gebruik: python download_straatstaal.py
"""

import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
from bs4 import BeautifulSoup

# ============================================================
# INSTELLINGEN
# ============================================================

BASE_URL = "https://straat-staal.jouwweb.nl"
OUTPUT_DIR = r"M:\Streetsteel.com\fotos"   # map waar foto's worden opgeslagen op QNAP
DELAY = 1.0                                 # wachttijd tussen verzoeken (beleefd scrapen)
MIN_FOTO_BREEDTE = 200                      # kleinere afbeeldingen (iconen etc.) overslaan

# Alle bekende pagina's van de site
ALLE_PAGINAS = [
    "/",
    "/nederland",
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
    "/europa",
    "/europa/denemarken",
    "/europa/denemarken/korsor",
    "/europa/duitsland",
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
    "/europa/hongarije",
    "/europa/hongarije/boedapest",
    "/europa/italie",
    "/europa/italie/como",
    "/europa/italie/sicilie",
    "/europa/kosovo",
    "/europa/kroatie",
    "/europa/macedonie",
    "/europa/noorwegen",
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
    "/europa/frankrijk",
    "/europa/oostenrijk",
    "/europa/portugal",
    "/europa/schotland",
    "/europa/slowakije",
    "/europa/slowakije/bratislava",
    "/europa/spanje",
    "/europa/spanje/cordoba",
    "/europa/spanje/granada",
    "/europa/spanje/nerja",
    "/europa/spanje/udeba",
    "/europa/zweden",
    "/europa/zweden/goeteborg",
    "/europa/zweden/malmoe",
    "/europa/zweden/nordby",
    "/fabrikanten-a-m",
    "/fabrikanten-a-m/alphacan",
    "/fabrikanten-a-m/aquagate",
    "/fabrikanten-a-m/aquafix",
    "/fabrikanten-a-m/aqauway",
    "/fabrikanten-a-m/avk",
    "/fabrikanten-a-m/b-oz",
    "/fabrikanten-a-m/de-leidinggroothandel",
    "/fabrikanten-a-m/de-globe",
    "/fabrikanten-a-m/delta-plast",
    "/fabrikanten-a-m/dijg",
    "/fabrikanten-a-m/draka-polva",
    "/fabrikanten-a-m/dyka",
    "/fabrikanten-a-m/ewe",
    "/fabrikanten-a-m/fibrelita",
    "/fabrikanten-a-m/fmh-pompservice",
    "/fabrikanten-a-m/frelu",
    "/fabrikanten-a-m/friand",
    "/fabrikanten-a-m/geertsema",
    "/fabrikanten-a-m/hauraton",
    "/fabrikanten-a-m/hermelock",
    "/fabrikanten-a-m/joosten",
    "/fabrikanten-a-m/kamphuis",
    "/fabrikanten-a-m/kb",
    "/fabrikanten-a-m/kessel",
    "/fabrikanten-a-m/ksk",
    "/fabrikanten-a-m/landustrie",
    "/fabrikanten-a-m/lhs",
    "/fabrikanten-a-m/lovink",
    "/fabrikanten-a-m/martens",
    "/fabrikanten-a-m/meijer",
    "/fabrikanten-a-m/milder",
    "/fabrikanten-a-m/mous",
    "/fabrikanten-n-z",
    "/fabrikanten-n-z/natuurbeton-milieu",
    "/fabrikanten-n-z/neering-bogel",
    "/fabrikanten-n-z/nki",
    "/fabrikanten-n-z/norinco",
    "/fabrikanten-n-z/nyloplast",
    "/fabrikanten-n-z/oogink",
    "/fabrikanten-n-z/pam",
    "/fabrikanten-n-z/passevant",
    "/fabrikanten-n-z/pipelife",
    "/fabrikanten-n-z/poly",
    "/fabrikanten-n-z/samson",
    "/fabrikanten-n-z/sotra",
    "/fabrikanten-n-z/stora",
    "/fabrikanten-n-z/stradus",
    "/fabrikanten-n-z/strucom",
    "/fabrikanten-n-z/tbs",
    "/fabrikanten-n-z/thijssen",
    "/fabrikanten-n-z/topatec",
    "/fabrikanten-n-z/van-der-velden",
    "/fabrikanten-n-z/veko",
    "/fabrikanten-n-z/vulcanus",
    "/fabrikanten-n-z/w-ten-cate",
    "/fabrikanten-n-z/waprog",
    "/fabrikanten-n-z/waterleiding-mij-prov-groningen",
    "/fabrikanten-n-z/wavin",
    "/fabrikanten-n-z/weegels",
    "/fabrikanten-n-z/mij-onbekende-producent-en",
]

# Domeinen waarvan afbeeldingen geaccepteerd worden
TOEGESTANE_DOMEINEN = ["assets.jwwb.nl", "straat-staal.jouwweb.nl"]

# Afbeeldingen die we NIET willen (template/thema plaatjes)
UITSLUIT_PATRONEN = [
    "hero.jpg",
    "placeholder",
    "logo",
    "icon",
    "banner",
    "template",
    "concert-banner",
]

# ============================================================
# HULPFUNCTIES
# ============================================================

def maak_mapnaam(pad):
    """Zet een URL-pad om naar een veilige mapnaam."""
    pad = pad.strip("/").replace("/", os.sep)
    if not pad:
        pad = "home"
    return pad


def is_foto_url(url):
    """Controleer of de URL een echte foto is (geen icoon/template)."""
    url_lower = url.lower()
    
    # Moet een afbeeldingsextensie hebben
    if not any(url_lower.endswith(ext) or ext + "?" in url_lower 
               for ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]):
        return False
    
    # Uitsluitingspatronen checken
    for patroon in UITSLUIT_PATRONEN:
        if patroon in url_lower:
            return False
    
    # Domein checken
    domein = urlparse(url).netloc
    if not any(toegestaan in domein for toegestaan in TOEGESTANE_DOMEINEN):
        return False
    
    return True


def haal_fotos_op_van_pagina(url, sessie):
    """Haal alle foto-URLs op van één pagina."""
    try:
        print(f"  📄 Pagina ophalen: {url}")
        resp = sessie.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        fotos = set()
        
        # Zoek in <img> tags
        for img in soup.find_all("img"):
            for attrib in ["src", "data-src", "data-lazy-src", "data-original"]:
                src = img.get(attrib)
                if src:
                    absolute = urljoin(url, src)
                    # Verwijder query parameters voor vergelijking maar bewaar origineel
                    if is_foto_url(absolute):
                        # Haal schone URL op (zonder resize parameters)
                        schoon = absolute.split("?")[0]
                        fotos.add(schoon)
        
        # Zoek in achtergrondstijlen (background-image)
        for tag in soup.find_all(style=True):
            stijl = tag["style"]
            matches = re.findall(r'url\(["\']?(https?://[^"\')\s]+)["\']?\)', stijl)
            for match in matches:
                if is_foto_url(match):
                    fotos.add(match.split("?")[0])
        
        # Zoek in <source> tags (picture element)
        for source in soup.find_all("source"):
            srcset = source.get("srcset", "")
            for deel in srcset.split(","):
                url_deel = deel.strip().split(" ")[0]
                if url_deel and is_foto_url(url_deel):
                    fotos.add(url_deel.split("?")[0])
        
        return fotos
        
    except Exception as e:
        print(f"  ⚠️  Fout bij {url}: {e}")
        return set()


def download_foto(foto_url, doel_pad, sessie):
    """Download één foto naar het opgegeven pad."""
    try:
        if doel_pad.exists():
            return "overgeslagen"
        
        doel_pad.parent.mkdir(parents=True, exist_ok=True)
        
        resp = sessie.get(foto_url, timeout=30, stream=True)
        resp.raise_for_status()
        
        with open(doel_pad, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return "gedownload"
        
    except Exception as e:
        print(f"    ❌ Fout: {e}")
        return "mislukt"


def maak_bestandsnaam(url):
    """Genereer een bestandsnaam van een URL."""
    pad = urlparse(url).path
    naam = os.path.basename(pad)
    if not naam or "." not in naam:
        naam = "foto_" + str(hash(url))[-8:] + ".jpg"
    # Ongeldige tekens verwijderen
    naam = re.sub(r'[<>:"/\\|?*]', "_", naam)
    return naam


# ============================================================
# HOOFDPROGRAMMA
# ============================================================

def main():
    print("=" * 60)
    print("  STRAAT-STAAL FOTO DOWNLOADER")
    print("  → Opslag: M:\\Streetsteel.com")
    print("=" * 60)

    # ── Controleer of QNAP (M:) bereikbaar is ──────────────────
    qnap_root = Path(r"M:\Streetsteel.com")
    if not qnap_root.exists():
        print("\n❌ FOUT: De map M:\\Streetsteel.com is niet bereikbaar!")
        print("   Controleer het volgende:")
        print("   1. Is je QNAP ingeschakeld?")
        print("   2. Open Verkenner — zie je schijf M: staan?")
        print("   3. Zo niet: verbind eerst met je QNAP en probeer opnieuw.")
        input("\nDruk op Enter om af te sluiten...")
        return

    print(f"\n✅ QNAP bereikbaar: M:\\Streetsteel.com")
    print(f"📁 Foto's worden opgeslagen in: {OUTPUT_DIR}")
    print(f"🌐 Aantal pagina's te doorzoeken: {len(ALLE_PAGINAS)}")
    print("\nStart over 3 seconden... (Ctrl+C om te stoppen)\n")
    time.sleep(3)

    # Sessie aanmaken met nette headers
    sessie = requests.Session()
    sessie.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    })

    # Statistieken bijhouden
    totaal_gevonden = 0
    totaal_gedownload = 0
    totaal_overgeslagen = 0
    totaal_mislukt = 0

    # Log bestand en mappen aanmaken
    log_pad = Path(OUTPUT_DIR) / "download_log.txt"
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    alle_fotos = {}  # {foto_url: [pagina1, pagina2, ...]}
    
    # FASE 1: Alle pagina's doorzoeken en foto-URLs verzamelen
    print("FASE 1: Pagina's doorzoeken...")
    print("-" * 40)
    
    for pagina_pad in ALLE_PAGINAS:
        pagina_url = BASE_URL + pagina_pad
        fotos = haal_fotos_op_van_pagina(pagina_url, sessie)
        
        for foto in fotos:
            if foto not in alle_fotos:
                alle_fotos[foto] = []
            alle_fotos[foto].append(pagina_pad)
        
        print(f"  ✅ {len(fotos)} foto(s) gevonden op {pagina_pad}")
        time.sleep(DELAY)
    
    totaal_gevonden = len(alle_fotos)
    print(f"\n📊 Totaal unieke foto's gevonden: {totaal_gevonden}")
    
    # FASE 2: Foto's downloaden in mappenstructuur
    print("\nFASE 2: Foto's downloaden...")
    print("-" * 40)
    
    with open(log_pad, "w", encoding="utf-8") as log:
        log.write("STRAAT-STAAL DOWNLOAD LOG\n")
        log.write("=" * 50 + "\n\n")
        
        teller = 0
        for foto_url, paginas in alle_fotos.items():
            teller += 1
            
            # Gebruik de eerste pagina als primaire map
            eerste_pagina = paginas[0]
            map_naam = maak_mapnaam(eerste_pagina)
            bestandsnaam = maak_bestandsnaam(foto_url)
            doel_pad = Path(OUTPUT_DIR) / map_naam / bestandsnaam
            
            print(f"  [{teller}/{totaal_gevonden}] {bestandsnaam[:40]:<40}", end=" ")
            
            resultaat = download_foto(foto_url, doel_pad, sessie)
            
            if resultaat == "gedownload":
                totaal_gedownload += 1
                print("✅ gedownload")
                log.write(f"OK  | {doel_pad} | {foto_url}\n")
            elif resultaat == "overgeslagen":
                totaal_overgeslagen += 1
                print("⏭️  al aanwezig")
                log.write(f"SKIP| {doel_pad} | {foto_url}\n")
            else:
                totaal_mislukt += 1
                print("❌ mislukt")
                log.write(f"ERR | {doel_pad} | {foto_url}\n")
            
            time.sleep(0.3)  # Kort wachten tussen downloads
    
    # EINDRAPPORT
    print("\n" + "=" * 60)
    print("  KLAAR! EINDRAPPORT")
    print("=" * 60)
    print(f"  📸 Totaal gevonden:     {totaal_gevonden}")
    print(f"  ✅ Gedownload:          {totaal_gedownload}")
    print(f"  ⏭️  Al aanwezig:         {totaal_overgeslagen}")
    print(f"  ❌ Mislukt:             {totaal_mislukt}")
    print(f"\n  📁 Foto's staan in:    ./{OUTPUT_DIR}/")
    print(f"  📋 Log bestand:        ./{OUTPUT_DIR}/download_log.txt")
    print("\n✨ Je foto's zijn klaar voor de nieuwe website!")


if __name__ == "__main__":
    main()
