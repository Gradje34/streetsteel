# 📘 HANDLEIDING: Foto's downloaden van straat-staal.jouwweb.nl
## Voor Windows — geen programmeerkennis vereist

---

## 📂 Mappenstructuur op je QNAP (M:\)

Alle bestanden worden opgeslagen op je QNAP schijf M:, zo:

```
M:\Streetsteel.com\
│
├── fotos\                        ← alle gedownloade foto's
│   ├── nederland\
│   │   ├── amsterdam\
│   │   ├── groningen\
│   │   ├── veendam\
│   │   └── ... (alle steden)
│   ├── europa\
│   │   ├── duitsland\
│   │   │   ├── berlijn\
│   │   │   └── ... (alle steden)
│   │   ├── noorwegen\
│   │   │   ├── oslo\
│   │   │   └── ... (alle steden)
│   │   └── ... (alle landen)
│   ├── fabrikanten-a-m\
│   │   ├── wavin\
│   │   ├── dyka\
│   │   └── ... (alle fabrikanten)
│   ├── fabrikanten-n-z\
│   │   └── ... (alle fabrikanten)
│   └── download_log.txt          ← overzicht van alle downloads
│
├── website\                      ← straks: de websitecode (Pakket 2)
│   ├── src\
│   ├── public\
│   └── ...
│
└── beheer\                       ← straks: beheerpaneel configuratie
    └── ...
```

---

## ⚠️ Vereiste: QNAP moet verbonden zijn

Voordat je begint, controleer in **Verkenner** of je schijf **M:** zichtbaar is.
- Zo ja: ✅ je kunt verder
- Zo nee: zet je QNAP aan en wacht tot M: verschijnt

**Werken vanaf je mini-pc?** Zorg dat je QNAP ook daar als M: is gekoppeld.
Dan werkt alles precies hetzelfde — het script zoekt altijd naar `M:\Streetsteel.com`.

---

## STAP 1 — Python installeren

*(Doe dit op elke computer waarop je het script wilt draaien)*

1. Ga naar: **https://www.python.org/downloads/**
2. Klik op de grote gele knop **"Download Python 3.x.x"**
3. Open het gedownloade bestand (bijv. `python-3.x.x-amd64.exe`)
4. ⚠️ **BELANGRIJK:** Zet een vinkje bij **"Add Python to PATH"** (onderaan het venster!)
5. Klik op **"Install Now"**
6. Wacht tot de installatie klaar is, klik dan op **"Close"**

---

## STAP 2 — Controleren of Python werkt

1. Druk op de **Windows-toets** op je toetsenbord
2. Typ: `cmd` en druk op **Enter**
3. Er opent een zwart venster (de "opdrachtprompt")
4. Typ het volgende en druk op **Enter**:
   ```
   python --version
   ```
5. Je zou zoiets moeten zien als: `Python 3.12.0`
   - Zie je dat? ✅ Dan werkt Python!
   - Zie je een foutmelding? Herinstalleer Python en zorg voor het vinkje bij stap 1.4

---

## STAP 3 — Benodigde hulpprogramma's installeren

In hetzelfde zwarte venster (opdrachtprompt), typ het volgende en druk op **Enter**:

```
pip install requests beautifulsoup4
```

Je ziet tekst voorbij scrollen. Wacht tot het klaar is.
Als je aan het einde `Successfully installed` ziet staan: ✅ klaar!

---

## STAP 4 — Het download-script klaarzetten

1. Maak deze map aan als die nog niet bestaat:
   ```
   M:\Streetsteel.com\
   ```
2. Zet het bestand **`download_straatstaal.py`** op je bureaublad
   (of ergens op je C:-schijf — het script schrijft alles naar M: zelf)

---

## STAP 5 — Het script uitvoeren

1. Open de **opdrachtprompt** (Windows-toets → typ `cmd` → Enter)

2. Navigeer naar de plek waar je het script hebt gezet. Bijvoorbeeld bureaublad:
   ```
   cd %USERPROFILE%\Desktop
   ```

3. Start het download-script:
   ```
   python download_straatstaal.py
   ```

4. Het script controleert eerst of je QNAP bereikbaar is:
   ```
   ✅ QNAP bereikbaar: M:\Streetsteel.com
   📁 Foto's worden opgeslagen in: M:\Streetsteel.com\fotos
   🌐 Aantal pagina's te doorzoeken: 107
   Start over 3 seconden...
   ```

5. Daarna begint het scrapen en downloaden:
   ```
   FASE 1: Pagina's doorzoeken...
     📄 Pagina ophalen: https://straat-staal.jouwweb.nl/nederland/groningen
     ✅ 12 foto(s) gevonden op /nederland/groningen
   ...
   FASE 2: Foto's downloaden...
     [1/1042] putdeksel_groningen_01.jpg    ✅ gedownload
     [2/1042] putdeksel_groningen_02.jpg    ✅ gedownload
   ...
   ```

---

## STAP 6 — Wachten

⏳ Het script doorzoekt alle pagina's en downloadt alle foto's.
Bij 1000+ foto's kan dit **15 tot 30 minuten** duren.
Sluit het zwarte venster **NIET** — laat het gewoon draaien.

---

## STAP 7 — Klaar!

Als het script klaar is, zie je:
```
============================================================
  KLAAR! EINDRAPPORT
============================================================
  📸 Totaal gevonden:     1042
  ✅ Gedownload:          1038
  ⏭️  Al aanwezig:           0
  ❌ Mislukt:                4

  📁 Foto's staan in:    M:\Streetsteel.com\fotos\
  📋 Log bestand:        M:\Streetsteel.com\fotos\download_log.txt
```

---

## ❓ Veelvoorkomende problemen

### Probleem: `M:\Streetsteel.com is niet bereikbaar`
**Oplossing:** Controleer in Verkenner of schijf M: zichtbaar is. Zo niet: zet je QNAP aan.

### Probleem: `python` wordt niet herkend
**Oplossing:** Herinstalleer Python en zet het vinkje bij **"Add Python to PATH"**

### Probleem: `pip install` geeft een foutmelding
**Oplossing:** Typ in plaats daarvan:
```
python -m pip install requests beautifulsoup4
```

### Probleem: Sommige foto's zijn mislukt (❌)
**Oplossing:** Draai het script gewoon opnieuw. Al gedownloade foto's worden overgeslagen,
alleen de mislukte worden opnieuw geprobeerd.

### Probleem: Script draaien vanaf mini-pc
**Oplossing:** Installeer Python ook op de mini-pc (stap 1-3), zet het script op die pc,
en zorg dat M: ook daar gekoppeld is. Dan werkt alles identiek.

---

## 📋 Na het downloaden

Stuur Claude een bericht met:
- Hoeveel foto's er gedownload zijn (zie het eindrapport)
- Of er veel mislukte downloads waren (❌)

Dan gaan we door met **Pakket 2: de volledige website bouwen!** 🚀

---

*Handleiding gemaakt door Claude voor Gerard — streetsteel.com project*
