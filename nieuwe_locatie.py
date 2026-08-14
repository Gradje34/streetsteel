# -*- coding: utf-8 -*-
"""
StreetSteel — Nieuwe locatie toevoegen
=======================================
Interactief script om een nieuwe stad, land of fabrikant toe te voegen.
Het regelt de hele keten in de juiste volgorde:

  1. Fotomap aanmaken (jij zet daar je foto's in)
  2. Locatie registreren in maak_paginas.py (+ vlag/naam/i18n bij nieuw land)
  3. maak_fotolijsten.py   -> JSON fotolijsten + tellers
  4. maak_paginas.py       -> HTML pagina('s)
  5. voeg_fotosjs_toe.py   -> fotos.js in de nieuwe pagina('s)
  6. Kaartje / item invoegen op de overzichtspagina

Het script is IDEMPOTENT (twee keer draaien = geen dubbele entries) en
VEILIG (maakt .bak backups voor het bestanden aanpast; doet niets destructiefs;
raakt Netlify niet aan). Na afloop: lokaal testen, dan pushen + deployen.

Gebruik:  python nieuwe_locatie.py
"""

import re
import sys
import subprocess
from pathlib import Path

# ── INSTELLINGEN ──────────────────────────────────────────────
WEBSITE_MAP = Path(r"C:\streetsteel")
FOTOS_MAP   = WEBSITE_MAP / "fotos"

PY = sys.executable  # zelfde python-interpreter als waarmee dit draait

# Landnaam -> (weergavenaam, vlag-emoji, i18n-key)
# i18n-key volgt het patroon country.<iso2>. Bij een nieuw land vragen we ernaar.

# ── KLEINE HULPJES ────────────────────────────────────────────

def iso_naar_vlag(iso2):
    """Zet een 2-letterige ISO-landcode om naar de vlag-emoji.
    Een vlag-emoji bestaat uit twee 'regional indicator symbols':
    elke letter A-Z wordt omgezet naar het bijbehorende symbool (U+1F1E6..U+1F1FF).
    Bijv. 'be' -> 🇧🇪, 'fr' -> 🇫🇷. Geeft None bij ongeldige invoer."""
    iso2 = iso2.strip().lower()
    if len(iso2) != 2 or not iso2.isalpha():
        return None
    basis = 0x1F1E6  # regional indicator symbol 'A'
    return "".join(chr(basis + (ord(c) - ord("a"))) for c in iso2)


def vraag(tekst, toegestaan=None, leeg_ok=False):
    """Vraag input, herhaal tot geldig."""
    while True:
        antwoord = input(tekst).strip()
        if not antwoord and leeg_ok:
            return ""
        if not antwoord:
            print("  ⚠️  Voer iets in.")
            continue
        if toegestaan and antwoord.lower() not in toegestaan:
            print(f"  ⚠️  Kies uit: {', '.join(toegestaan)}")
            continue
        return antwoord


def maak_slug(naam):
    """Zet een naam om naar een URL-slug: kleine letters, streepjes, geen accenten."""
    s = naam.strip().lower()
    vervang = {
        "á":"a","à":"a","ä":"a","â":"a","ã":"a","å":"a",
        "é":"e","è":"e","ë":"e","ê":"e",
        "í":"i","ì":"i","ï":"i","î":"i",
        "ó":"o","ò":"o","ö":"o","ô":"o","õ":"o","ø":"o",
        "ú":"u","ù":"u","ü":"u","û":"u",
        "ñ":"n","ç":"c","ß":"ss",
        "æ":"ae",
    }
    for a, b in vervang.items():
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s)   # alles behalve letters/cijfers -> streepje
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def backup(pad: Path):
    """Maak een .bak kopie als die nog niet bestaat voor deze sessie."""
    bak = pad.with_suffix(pad.suffix + ".bak")
    bak.write_text(pad.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"     backup: {bak.name}")


def wacht_op_fotos(map_pad: Path):
    """Maak de fotomap en pauzeer zodat de gebruiker foto's kan plaatsen."""
    map_pad.mkdir(parents=True, exist_ok=True)
    print(f"\n📂 Fotomap klaargezet:\n     {map_pad}")
    print("   Zet nu je foto's in deze map (sleep ze erin via Verkenner).")
    input("   Druk op Enter zodra de foto's erin staan...")
    aantal = sum(1 for f in map_pad.iterdir()
                 if f.is_file() and f.suffix.lower() in {".jpg",".jpeg",".png",".webp",".gif"})
    if aantal == 0:
        print("   ⚠️  Er staan nog geen foto's in de map.")
        door = vraag("   Toch doorgaan? (ja/nee): ", toegestaan={"ja","nee"})
        if door == "nee":
            print("   Afgebroken. Er is niets gewijzigd behalve de (lege) fotomap.")
            sys.exit(0)
    else:
        print(f"   ✅ {aantal} foto('s) gevonden.")
    return aantal


def draai_script(naam):
    """Draai een van de bestaande generatorscripts en toon de uitvoer."""
    pad = WEBSITE_MAP / naam
    if not pad.exists():
        print(f"   ⚠️  {naam} niet gevonden — overgeslagen.")
        return
    print(f"\n▶  {naam} draaien...")
    # We sturen een Enter mee voor de 'Druk op Enter'-prompt aan het eind
    subprocess.run([PY, str(pad)], input="\n", text=True, cwd=str(WEBSITE_MAP))


# ── maak_paginas.py aanpassen ─────────────────────────────────

def voeg_nl_stad_toe_aan_generator(slug):
    """Voeg een stad toe aan NEDERLAND_STEDEN in maak_paginas.py (alfabetisch)."""
    pad = WEBSITE_MAP / "maak_paginas.py"
    tekst = pad.read_text(encoding="utf-8")
    if re.search(rf'"{re.escape(slug)}"', tekst):
        print(f"   ℹ️  '{slug}' staat al in maak_paginas.py — overgeslagen.")
        return
    m = re.search(r"NEDERLAND_STEDEN\s*=\s*\[(.*?)\]", tekst, re.DOTALL)
    if not m:
        print("   ⚠️  NEDERLAND_STEDEN niet gevonden in maak_paginas.py.")
        return
    backup(pad)
    huidige = re.findall(r'"([^"]+)"', m.group(1))
    huidige.append(slug)
    huidige = sorted(set(huidige))
    # herformatteer als nette lijst, 5 per regel, ingesprongen
    regels = []
    for i in range(0, len(huidige), 5):
        groep = ", ".join(f'"{s}"' for s in huidige[i:i+5])
        regels.append("    " + groep)
    nieuw_blok = "NEDERLAND_STEDEN = [\n" + ",\n".join(regels) + "\n]"
    tekst = tekst[:m.start()] + nieuw_blok + tekst[m.end():]
    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ '{slug}' toegevoegd aan NEDERLAND_STEDEN.")


def voeg_europa_toe_aan_generator(land_slug, stad_slugs, nieuw_land, naam=None, vlag=None, iso2=None):
    """Werk EUROPA_LANDEN (+ evt. LAND_VLAGGEN/NAMEN/I18N) bij in maak_paginas.py."""
    pad = WEBSITE_MAP / "maak_paginas.py"
    tekst = pad.read_text(encoding="utf-8")
    backup(pad)

    # 1) EUROPA_LANDEN bijwerken
    m = re.search(r"EUROPA_LANDEN\s*=\s*\{(.*?)\n\}", tekst, re.DOTALL)
    if not m:
        print("   ⚠️  EUROPA_LANDEN niet gevonden.")
        return
    blok = m.group(1)
    # bestaande steden van dit land uitlezen (indien aanwezig)
    land_m = re.search(rf'"{re.escape(land_slug)}"\s*:\s*\[(.*?)\]', blok, re.DOTALL)
    bestaande = []
    if land_m:
        bestaande = re.findall(r'"([^"]+)"', land_m.group(1))
    alle_steden = sorted(set(bestaande) | set(stad_slugs))
    steden_str = ", ".join(f'"{s}"' for s in alle_steden)
    nieuwe_regel = f'    "{land_slug}": [{steden_str}],'

    if land_m:
        # vervang de bestaande land-regel
        start = blok.find(land_m.group(0))
        # vind volledige regel-grenzen
        regel_pat = re.compile(rf'\n\s*"{re.escape(land_slug)}"\s*:\s*\[.*?\],', re.DOTALL)
        blok_nieuw = regel_pat.sub("\n" + nieuwe_regel, blok, count=1)
    else:
        # voeg toe (alfabetisch is netjes maar niet vereist; achteraan is prima)
        blok_nieuw = blok.rstrip() + "\n" + nieuwe_regel + "\n"
    tekst = tekst[:m.start(1)] + blok_nieuw + tekst[m.end(1):]

    # 2) Bij nieuw land: vlag, naam, i18n toevoegen als ze ontbreken
    if nieuw_land:
        def voeg_in_dict(dictnaam, sleutel, waarde):
            nonlocal tekst
            if re.search(rf'"{re.escape(sleutel)}"\s*:', tekst.split(dictnaam,1)[1].split("}",1)[0]):
                return  # staat er al
            dm = re.search(rf"{dictnaam}\s*=\s*\{{(.*?)\n\}}", tekst, re.DOTALL)
            if not dm:
                print(f"   ⚠️  {dictnaam} niet gevonden.")
                return
            binnenkant = dm.group(1).rstrip()
            binnenkant += f'\n    "{sleutel}": "{waarde}",'
            tekst = tekst[:dm.start(1)] + binnenkant + tekst[dm.end(1):]

        voeg_in_dict("LAND_VLAGGEN", land_slug, vlag)
        voeg_in_dict("LAND_NAMEN",   land_slug, naam)
        voeg_in_dict("LAND_I18N",    land_slug, f"country.{iso2}")

    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ maak_paginas.py bijgewerkt voor land '{land_slug}'.")


def voeg_fabrikant_toe_aan_generator(slug):
    """Voeg een fabrikant toe aan FABRIKANTEN in maak_paginas.py."""
    pad = WEBSITE_MAP / "maak_paginas.py"
    tekst = pad.read_text(encoding="utf-8")
    m = re.search(r"FABRIKANTEN\s*=\s*\[(.*?)\]", tekst, re.DOTALL)
    if not m:
        print("   ⚠️  FABRIKANTEN niet gevonden.")
        return
    if re.search(rf'"{re.escape(slug)}"', m.group(1)):
        print(f"   ℹ️  '{slug}' staat al in FABRIKANTEN — overgeslagen.")
        return
    backup(pad)
    huidige = re.findall(r'"([^"]+)"', m.group(1))
    huidige.append(slug)
    huidige = sorted(set(huidige))
    regels = []
    for i in range(0, len(huidige), 5):
        groep = ", ".join(f'"{s}"' for s in huidige[i:i+5])
        regels.append("    " + groep)
    nieuw_blok = "FABRIKANTEN = [\n" + ",\n".join(regels) + "\n]"
    tekst = tekst[:m.start()] + nieuw_blok + tekst[m.end():]
    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ '{slug}' toegevoegd aan FABRIKANTEN.")


# ── Overzichtspagina's bijwerken ──────────────────────────────

def kaartje_html(href, land_label, vlag, stad_label, data_page):
    return (
        f'            <a href="{href}" class="location-card">\n'
        f'                <div class="card-img-placeholder"><span class="card-flag">{vlag}</span></div>\n'
        f'                <div class="card-body">\n'
        f'                    <span class="card-country">{land_label}</span>\n'
        f'                    <h3 class="card-city">{stad_label}</h3>\n'
        f'                    <span class="card-count photo-count" data-page="{data_page}"></span>\n'
        f'                </div>\n'
        f'            </a>\n'
    )


def voeg_kaartje_in(overzicht_bestand, nieuw_kaartje, href):
    """Voeg een kaartje in de cards-grid, vlak voor </div> die de grid sluit.
    Idempotent: doet niets als de href al voorkomt."""
    pad = WEBSITE_MAP / overzicht_bestand
    if not pad.exists():
        print(f"   ⚠️  {overzicht_bestand} niet gevonden.")
        return
    tekst = pad.read_text(encoding="utf-8")
    if f'href="{href}"' in tekst:
        print(f"   ℹ️  Kaartje voor {href} bestaat al — overgeslagen.")
        return
    backup(pad)

    # Zoek de openende <div class="cards-grid"> en vind de BIJBEHORENDE sluit-</div>
    # via depth-matching (open/dicht <div> tellen). Zo belandt het kaartje altijd
    # binnen de grid, ook al staan er verderop (footer) nog </a>/</div> tags.
    open_tag = '<div class="cards-grid">'
    start = tekst.find(open_tag)
    if start == -1:
        print(f"   ⚠️  cards-grid niet gevonden in {overzicht_bestand}.")
        return

    # begin te tellen vanaf ná de openende tag
    i = start + len(open_tag)
    depth = 1
    div_pat = re.compile(r"<div\b|</div>", re.IGNORECASE)
    grid_eind = -1
    for m in div_pat.finditer(tekst, i):
        if m.group(0).lower().startswith("<div"):
            depth += 1
        else:  # </div>
            depth -= 1
            if depth == 0:
                grid_eind = m.start()
                break

    if grid_eind == -1:
        print(f"   ⚠️  Einde van cards-grid (sluitende </div>) niet gevonden.")
        return

    # Bepaal de sorteersleutel van het nieuwe kaartje: laatste paddeel vóór .html
    # bijv. "nederland/teststad.html" -> "teststad", "europa/noorwegen/oslo.html" -> "oslo"
    nieuwe_slug = href.rsplit("/", 1)[-1].removesuffix(".html").lower()

    # Zoek binnen de grid (tussen start en grid_eind) alle bestaande kaartjes en
    # hun slug, om de alfabetische invoegplek te vinden.
    grid_inhoud = tekst[start:grid_eind]
    kaart_pat = re.compile(r'<a href="([^"]+?)\.html" class="location-card">')
    invoeg_pos = grid_eind  # standaard: aan het einde van de grid
    for m in kaart_pat.finditer(grid_inhoud):
        bestaande_slug = m.group(1).rsplit("/", 1)[-1].lower()
        if bestaande_slug > nieuwe_slug:
            # voeg in vóór dit kaartje (positie is relatief aan grid-begin -> +start)
            invoeg_pos = start + m.start()
            break

    tekst = tekst[:invoeg_pos] + nieuw_kaartje + tekst[invoeg_pos:]
    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ Kaartje toegevoegd op {overzicht_bestand} (alfabetisch geplaatst).")


def voeg_fabrikant_item_in(slug, weergavenaam):
    """Voeg een manufacturer-item toe op fabrikanten.html (alfabetisch)."""
    pad = WEBSITE_MAP / "fabrikanten.html"
    if not pad.exists():
        print("   ⚠️  fabrikanten.html niet gevonden.")
        return
    tekst = pad.read_text(encoding="utf-8")
    href = f"fabrikanten/{slug}.html"
    if f'href="{href}"' in tekst:
        print(f"   ℹ️  Item voor {slug} bestaat al — overgeslagen.")
        return
    backup(pad)
    nieuw = (f'            <a href="{href}" class="manufacturer-item">'
             f'<span class="manufacturer-name">{weergavenaam}</span>'
             f'<span class="manufacturer-arrow">→</span></a>\n')
    # voeg alfabetisch in: zoek eerste bestaand item dat 'groter' is
    items = list(re.finditer(r'( *<a href="fabrikanten/([^"]+)\.html" class="manufacturer-item">.*?</a>\n)', tekst))
    ingevoegd = False
    for it in items:
        if it.group(2) > slug:
            tekst = tekst[:it.start()] + nieuw + tekst[it.start():]
            ingevoegd = True
            break
    if not ingevoegd and items:
        # na het laatste item
        laatste = items[-1]
        tekst = tekst[:laatste.end()] + nieuw + tekst[laatste.end():]
        ingevoegd = True
    if not ingevoegd:
        print("   ⚠️  Geen bestaande fabrikant-items gevonden om tussen te voegen.")
        return
    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ '{weergavenaam}' toegevoegd op fabrikanten.html.")


# ── HOOFDSTROOM ───────────────────────────────────────────────

def keten_draaien():
    """De drie generatorscripts in de juiste volgorde."""
    draai_script("maak_fotolijsten.py")
    draai_script("maak_paginas.py")
    draai_script("voeg_fotosjs_toe.py")


def lees_land_gegevens(land_slug):
    """Lees vlag, weergavenaam en i18n-key van een bestaand land uit maak_paginas.py.
    Geeft (vlag, naam, i18n) terug, of (None, None, None) als het land niet bestaat."""
    pad = WEBSITE_MAP / "maak_paginas.py"
    tekst = pad.read_text(encoding="utf-8")
    vlag = naam = i18n = None
    mv = re.search(rf'"{re.escape(land_slug)}"\s*:\s*"([^"]+)"',
                   tekst[tekst.find("LAND_VLAGGEN"):tekst.find("LAND_NAMEN")])
    if mv:
        vlag = mv.group(1)
    mn = re.search(rf'"{re.escape(land_slug)}"\s*:\s*"([^"]+)"',
                   tekst[tekst.find("LAND_NAMEN"):tekst.find("LAND_I18N")])
    if mn:
        naam = mn.group(1)
    mi = re.search(rf'"{re.escape(land_slug)}"\s*:\s*"([^"]+)"',
                   tekst[tekst.find("LAND_I18N"):tekst.find("FABRIKANTEN")])
    if mi:
        i18n = mi.group(1)
    return vlag, naam, i18n


def voeg_stad_tegel_in_landpagina(land_slug, stad_slug, stad_naam, vlag, land_naam, i18n):
    """Voeg een stad-tegel toe aan europa/{land}.html op de alfabetische plek.
    Zo verschijnt de nieuwe stad direct op de landpagina, zonder maak_landpaginas.py."""
    pad = WEBSITE_MAP / "europa" / f"{land_slug}.html"
    if not pad.exists():
        print(f"   ⚠️  europa/{land_slug}.html niet gevonden — tegel niet toegevoegd.")
        print(f"      (Landpagina bestaat mogelijk nog niet; controleer handmatig.)")
        return
    tekst = pad.read_text(encoding="utf-8")
    href = f"/europa/{land_slug}/{stad_slug}.html"
    if f'href="{href}"' in tekst:
        print(f"   ℹ️  Tegel voor {stad_slug} bestaat al op de landpagina — overgeslagen.")
        return
    backup(pad)

    # Tegel-HTML in exact hetzelfde formaat als de bestaande tegels op de landpagina
    tegel = (
        f'            <a href="{href}" class="location-card">\n'
        f'                <div class="card-img-placeholder">\n'
        f'                    <span class="card-flag">{vlag}</span>\n'
        f'                </div>\n'
        f'                <div class="card-body">\n'
        f'                    <span class="card-country" data-i18n="{i18n}">{land_naam}</span>\n'
        f'                    <h3 class="card-city">{stad_naam}</h3>\n'
        f'                    <span class="card-count photo-count" data-page="europa/{land_slug}/{stad_slug}"></span>\n'
        f'                </div>\n'
        f'            </a>\n'
    )

    # Vind de cards-grid en de bijbehorende sluit-</div> via depth-matching
    open_tag = '<div class="cards-grid">'
    start = tekst.find(open_tag)
    if start == -1:
        print(f"   ⚠️  cards-grid niet gevonden in europa/{land_slug}.html.")
        return
    i = start + len(open_tag)
    depth = 1
    div_pat = re.compile(r"<div\b|</div>", re.IGNORECASE)
    grid_eind = -1
    for m in div_pat.finditer(tekst, i):
        if m.group(0).lower().startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                grid_eind = m.start()
                break
    if grid_eind == -1:
        print(f"   ⚠️  Einde van cards-grid niet gevonden.")
        return

    # Alfabetische invoegplek: vóór het eerste bestaande tegel-slug dat later komt
    grid_inhoud = tekst[start:grid_eind]
    kaart_pat = re.compile(r'<a href="/europa/[^/]+/([^"]+?)\.html" class="location-card">')
    invoeg_pos = grid_eind
    for m in kaart_pat.finditer(grid_inhoud):
        if m.group(1).lower() > stad_slug.lower():
            invoeg_pos = start + m.start()
            break

    tekst = tekst[:invoeg_pos] + tegel + tekst[invoeg_pos:]
    pad.write_text(tekst, encoding="utf-8")
    print(f"   ✅ Stad-tegel toegevoegd op europa/{land_slug}.html (alfabetisch).")


def flow_nederland_stad():
    naam = vraag("\nNaam van de stad (bijv. Utrecht): ")
    slug = maak_slug(naam)
    print(f"   URL-naam wordt: {slug}")
    wacht_op_fotos(FOTOS_MAP / "nederland" / slug)
    voeg_nl_stad_toe_aan_generator(slug)
    keten_draaien()
    kaart = kaartje_html(f"nederland/{slug}.html", "Nederland", "🇳🇱",
                         naam.strip().title(), f"nederland/{slug}")
    voeg_kaartje_in("nederland.html", kaart, f"nederland/{slug}.html")


def flow_europa():
    print("\nBestaand land of nieuw land?")
    print("  1) Stad toevoegen aan een BESTAAND land")
    print("  2) NIEUW land toevoegen")
    keuze = vraag("Keuze (1/2): ", toegestaan={"1","2"})

    if keuze == "1":
        land_slug = maak_slug(vraag("\nLand (slug, bijv. noorwegen): "))
        # Vlag, naam en i18n automatisch ophalen uit maak_paginas.py (land bestaat al)
        vlag, land_label, i18n = lees_land_gegevens(land_slug)
        if vlag is None:
            print(f"   ⚠️  Land '{land_slug}' niet gevonden in maak_paginas.py.")
            print("      Gebruik de slug (bijv. 'noorwegen', 'duitsland'), of kies optie 2 voor een NIEUW land.")
            return
        print(f"   Land herkend: {land_label} {vlag}")
        naam = vraag("Naam van de stad zoals getoond (bijv. Trondheim): ")
        stad_slug = maak_slug(naam)
        stad_naam = naam.strip()
        print(f"   URL-naam wordt: {stad_slug}")
        wacht_op_fotos(FOTOS_MAP / "europa" / land_slug / stad_slug)
        voeg_europa_toe_aan_generator(land_slug, [stad_slug], nieuw_land=False)
        keten_draaien()
        # Stad-tegel invoegen op de landpagina (europa/{land}.html), alfabetisch.
        # GEEN los kaartje op europa.html: een stad onder een land-met-steden
        # verschijnt als tegel op de landpagina, niet op het europa-overzicht.
        voeg_stad_tegel_in_landpagina(land_slug, stad_slug, stad_naam, vlag, land_label, i18n)
        return

    # NIEUW land
    naam = vraag("\nNaam van het land (bijv. Belgie): ")
    land_slug = maak_slug(naam)
    weergavenaam = vraag("Landnaam met juiste spelling (bijv. België): ")
    while True:
        iso2 = maak_slug(vraag("ISO-landcode, 2 letters (bijv. be voor België, fr voor Frankrijk): ")).replace("-","")
        vlag = iso_naar_vlag(iso2)
        if vlag is None:
            print("  ⚠️  Voer precies 2 letters in (bijv. be, fr, de).")
            continue
        print(f"   Vlag wordt: {vlag}  (uit ISO-code '{iso2}')")
        break
    print(f"   URL-naam wordt: {land_slug}")

    print("\nHeeft dit land meteen steden, of komen de foto's direct op de landpagina?")
    print("  1) Direct op de landpagina (geen steden, zoals Frankrijk)")
    print("  2) Met een of meer steden")
    steden_keuze = vraag("Keuze (1/2): ", toegestaan={"1","2"})

    if steden_keuze == "1":
        wacht_op_fotos(FOTOS_MAP / "europa" / land_slug)
        voeg_europa_toe_aan_generator(land_slug, [], nieuw_land=True,
                                      naam=weergavenaam, vlag=vlag, iso2=iso2)
        keten_draaien()
        kaart = kaartje_html(f"europa/{land_slug}.html", weergavenaam, vlag,
                             weergavenaam, f"europa/{land_slug}")
        voeg_kaartje_in("europa.html", kaart, f"europa/{land_slug}.html")
    else:
        stad_slugs = []
        stad_info = []  # (slug, weergavenaam)
        while True:
            snaam = vraag("\nNaam van een stad in dit land: ")
            sslug = maak_slug(snaam)
            wacht_op_fotos(FOTOS_MAP / "europa" / land_slug / sslug)
            stad_slugs.append(sslug)
            stad_info.append((sslug, snaam.strip().title()))
            nog = vraag("Nog een stad toevoegen? (ja/nee): ", toegestaan={"ja","nee"})
            if nog == "nee":
                break
        voeg_europa_toe_aan_generator(land_slug, stad_slugs, nieuw_land=True,
                                      naam=weergavenaam, vlag=vlag, iso2=iso2)
        keten_draaien()
        # kaartjes voor elke stad
        for sslug, slabel in stad_info:
            kaart = kaartje_html(f"europa/{land_slug}/{sslug}.html", weergavenaam, vlag,
                                 slabel, f"europa/{land_slug}/{sslug}")
            voeg_kaartje_in("europa.html", kaart, f"europa/{land_slug}/{sslug}.html")


def flow_fabrikant():
    naam = vraag("\nNaam van de fabrikant (bijv. Wavin): ")
    slug = maak_slug(naam)
    print(f"   URL-naam wordt: {slug}")
    # juiste fotomap kiezen: a-m of n-z op basis van eerste letter
    eerste = slug[0]
    submap = "fabrikanten-a-m" if eerste <= "m" else "fabrikanten-n-z"
    print(f"   Fotomap: {submap} (op basis van beginletter '{eerste}')")
    wacht_op_fotos(FOTOS_MAP / submap / slug)
    voeg_fabrikant_toe_aan_generator(slug)
    keten_draaien()
    voeg_fabrikant_item_in(slug, naam.strip())


def lees_bestaande_locaties(soort):
    """Geef een lijst (slug, weergavenaam, fotomap_pad) van bestaande locaties.
    soort is 'nederland', 'europa' of 'fabrikant'."""
    mp = WEBSITE_MAP / "maak_paginas.py"
    tekst = mp.read_text(encoding="utf-8")
    resultaat = []

    if soort == "nederland":
        m = re.search(r"NEDERLAND_STEDEN\s*=\s*\[(.*?)\]", tekst, re.DOTALL)
        slugs = re.findall(r'"([^"]+)"', m.group(1)) if m else []
        for s in slugs:
            naam = s.replace("-", " ").title()
            resultaat.append((s, naam, FOTOS_MAP / "nederland" / s))

    elif soort == "europa":
        # steden onder elk land + landen-zonder-steden
        m = re.search(r"EUROPA_LANDEN\s*=\s*\{(.*?)\n\}", tekst, re.DOTALL)
        blok = m.group(1) if m else ""
        for lm in re.finditer(r'"([^"]+)"\s*:\s*\[(.*?)\]', blok, re.DOTALL):
            land = lm.group(1)
            steden = re.findall(r'"([^"]+)"', lm.group(2))
            if steden:
                for st in steden:
                    naam = st.replace("-", " ").title()
                    resultaat.append((st, f"{naam} ({land.title()})",
                                      FOTOS_MAP / "europa" / land / st))
            else:
                # land zonder steden: foto's staan direct op landniveau
                resultaat.append((land, land.title(),
                                  FOTOS_MAP / "europa" / land))

    elif soort == "fabrikant":
        # mooie namen uit fabrikanten.html
        fab = WEBSITE_MAP / "fabrikanten.html"
        ftekst = fab.read_text(encoding="utf-8") if fab.exists() else ""
        for fm in re.finditer(
                r'fabrikanten/([^"]+)\.html" class="manufacturer-item">'
                r'<span class="manufacturer-name">([^<]+)</span>', ftekst):
            slug, naam = fm.group(1), fm.group(2)
            submap = "fabrikanten-a-m" if slug[0] <= "m" else "fabrikanten-n-z"
            resultaat.append((slug, naam, FOTOS_MAP / submap / slug))

    return resultaat


def kies_bestaande_locatie(soort):
    """Laat de gebruiker een bestaande locatie kiezen via typen-met-herkenning.
    Eén match -> bevestigen; meerdere -> genummerde lijst; geen -> opnieuw.
    Geeft (slug, naam, fotomap_pad) terug, of None bij afbreken."""
    locaties = lees_bestaande_locaties(soort)
    if not locaties:
        print("   ⚠️  Geen bestaande locaties gevonden.")
        return None

    while True:
        zoek = vraag("\nTyp (een deel van) de naam (of 'lijst' voor alles, 'stop' om te annuleren): ").lower()
        if zoek == "stop":
            return None
        if zoek == "lijst":
            treffers = locaties
        else:
            # match op slug én weergavenaam
            treffers = [loc for loc in locaties
                        if zoek in loc[0].lower() or zoek in loc[1].lower()]

        if not treffers:
            print(f"   Geen match voor '{zoek}'. Probeer opnieuw of typ 'lijst'.")
            continue

        if len(treffers) == 1:
            slug, naam, pad = treffers[0]
            ja = vraag(f"   Bedoel je '{naam}'? (ja/nee): ", toegestaan={"ja","nee"})
            if ja == "ja":
                return treffers[0]
            continue

        # meerdere treffers -> genummerde lijst
        print(f"\n   {len(treffers)} matches:")
        for i, (slug, naam, pad) in enumerate(treffers, 1):
            print(f"     {i}) {naam}")
        keuze = vraag("   Kies een nummer (of 'terug' om opnieuw te zoeken): ")
        if keuze == "terug":
            continue
        if keuze.isdigit() and 1 <= int(keuze) <= len(treffers):
            return treffers[int(keuze) - 1]
        print("   Ongeldige keuze.")


def flow_foto_toevoegen():
    """Voeg foto's toe aan een BESTAANDE locatie (stad, land of fabrikant).
    Vindt de bestaande map, jij zet foto's erin, en werkt alleen de tellers bij.
    Maakt GEEN nieuwe pagina en GEEN nieuw lijst-item (geen duplicaat-risico)."""
    print("\nAan welk type locatie wil je foto's toevoegen?")
    print("  1) Stad in Nederland")
    print("  2) Land of stad in Europa")
    print("  3) Fabrikant")
    t = vraag("Keuze (1/2/3): ", toegestaan={"1","2","3"})
    soort = {"1":"nederland","2":"europa","3":"fabrikant"}[t]

    keuze = kies_bestaande_locatie(soort)
    if keuze is None:
        print("   Geannuleerd.")
        return
    slug, naam, fotomap = keuze

    if not fotomap.exists():
        print(f"   ⚠️  Fotomap bestaat niet: {fotomap}")
        print("      Dit kan wijzen op een naam-mismatch. Afgebroken (niets gewijzigd).")
        return

    print(f"\n   Locatie: {naam}")
    print(f"   Bestaande fotomap: {fotomap}")
    wacht_op_fotos(fotomap)
    # Alleen de tellers/fotolijsten bijwerken — geen pagina's, geen lijst-items.
    draai_script("maak_fotolijsten.py")
    print(f"\n   ✅ Foto's toegevoegd aan {naam} en tellers bijgewerkt.")


def main():
    print("=" * 55)
    print("  STREETSTEEL — NIEUWE LOCATIE TOEVOEGEN")
    print("=" * 55)

    if not WEBSITE_MAP.exists():
        print(f"\n❌ Werkmap niet gevonden: {WEBSITE_MAP}")
        input("Druk op Enter om af te sluiten...")
        return

    print("\nWat wil je doen?")
    print("  1) NIEUWE stad in Nederland")
    print("  2) NIEUW land of stad in Europa")
    print("  3) NIEUWE fabrikant")
    print("  4) Foto's toevoegen aan een BESTAANDE locatie")
    keuze = vraag("Keuze (1/2/3/4): ", toegestaan={"1","2","3","4"})

    if keuze == "1":
        flow_nederland_stad()
    elif keuze == "2":
        flow_europa()
    elif keuze == "3":
        flow_fabrikant()
    else:
        flow_foto_toevoegen()

    print("\n" + "=" * 55)
    print("  KLAAR — lokaal toegevoegd.")
    print("=" * 55)
    print("Volgende stappen (zoals altijd):")
    print("  1. Test lokaal:   python -m http.server 8000")
    print("     en bekijk de nieuwe pagina('s) met Ctrl+F5.")
    print("  2. git status  -> controleer de gewijzigde bestanden")
    print("  3. Bij ~98% zekerheid: git add / commit / push")
    print("  4. Netlify: Trigger deploy -> Publish deploy")
    print("\nTip: de .bak-bestanden zijn backups; verwijderen mag zodra alles klopt.")
    input("\nDruk op Enter om af te sluiten...")


if __name__ == "__main__":
    main()
