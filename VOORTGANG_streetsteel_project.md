# 🚀 Streetsteel.com — Project Voortgang
*Bewaar dit bestand op M:\Streetsteel.com\ zodat je het altijd terug kunt vinden*

---

## ✅ Wat er al besloten is

| Onderdeel | Keuze |
|---|---|
| Domeinnaam | streetsteel.com (~€12/jaar, nog aan te schaffen) |
| Hosting | Netlify (gratis) |
| Code opslag | GitHub |
| Lokale opslag | M:\Streetsteel.com\ (QNAP) |
| Stijl | Industrieel / donker thema |
| Standaardtaal | Nederlands |
| Taalkeuze | Per pagina: NL + EN altijd, + landstaal indien beschikbaar |
| Taalswitch | Pop-up als gekozen taal niet beschikbaar is op nieuwe pagina |
| Foto organisatie | Per stad/land ÉN per fabrikant (1x opgeslagen, 2x zichtbaar) |
| Fototeller | Automatisch per pagina |
| Fabrikanten | Introductietekst (AI-gegenereerd, Gerard controleert) + websitelink |
| Beheerpaneel | Decap CMS, via browser op laptop |
| Nieuwe content | Via dropdowns: land → stad + fabrikant koppelen |
| Passief inkomen | PayPal knop (onderaan elke pagina) + Google AdSense + Ko-fi |
| Doelgroep | Hobbyisten én professionals (gemeenten, aannemers, leveranciers) |

---

## 📂 Mappenstructuur op QNAP

```
M:\Streetsteel.com\
├── fotos\              ← gedownloade foto's van JouwWeb
├── website\            ← websitecode (Pakket 2, nog te bouwen)
└── beheer\             ← beheerpaneel configuratie (Pakket 3, nog te bouwen)
```

---

## 📦 Pakketten — status

| Pakket | Inhoud | Status |
|---|---|---|
| Pakket 1 | Python installatie + foto download script | 🔄 Bezig |
| Pakket 2 | Volledige websitecode | ⏳ Wacht op Pakket 1 |
| Pakket 3 | Beheerpaneel (Decap CMS) | ⏳ Wacht op Pakket 2 |
| Pakket 4 | Handleiding: GitHub → Netlify → domein koppelen | ⏳ Wacht op Pakket 3 |

---

## 🔄 Waar je gebleven bent (voor na de reboot)

**Python is zojuist geïnstalleerd op je laptop.**

Je hebt bij de vraag *"Update setting now? y/n"* voor **y** gekozen.
Windows heeft daarna gevraagd om een herstart.

### Na de reboot doe je dit:

**Stap 1 — Controleer of Python werkt:**
1. Druk op Windows-toets, typ `cmd`, druk Enter
2. Typ dit en druk Enter:
   ```
   python --version
   ```
3. Je moet zoiets zien als: `Python 3.12.0` ✅

**Stap 2 — Installeer de hulpprogramma's:**
Typ dit in hetzelfde zwarte venster en druk Enter:
```
pip install requests beautifulsoup4
```
Wacht tot je `Successfully installed` ziet. ✅

**Stap 3 — Zet het script klaar:**
- Zorg dat `download_straatstaal.py` op je bureaublad staat
- Zorg dat je QNAP aan is en M: zichtbaar is in Verkenner
- Maak de map `M:\Streetsteel.com\` aan als die nog niet bestaat

**Stap 4 — Draai het script:**
```
cd %USERPROFILE%\Desktop
python download_straatstaal.py
```

**Stap 5 — Wachten (15-30 minuten)**
Sluit het zwarte venster NIET.

**Stap 6 — Eindrapport naar Claude sturen**
Als het klaar is, stuur het eindrapport naar Claude (hoeveel foto's gedownload/mislukt).
Dan bouwen we **Pakket 2: de volledige website**! 🚀

---

## 📋 Bestanden in dit project

| Bestand | Omschrijving |
|---|---|
| `download_straatstaal.py` | Script om foto's van JouwWeb te downloaden |
| `HANDLEIDING_stap1_fotos_downloaden.md` | Volledige handleiding voor Pakket 1 |
| `VOORTGANG_streetsteel_project.md` | Dit bestand — projectoverzicht |

---

## 💡 Handige herinneringen

- **JouwWeb heeft geen export** — daarom gebruiken we het download script
- **Script hervatten**: als het script stopt, gewoon opnieuw draaien — al gedownloade foto's worden overgeslagen
- **Mini-pc**: installeer Python daar ook, zorg dat M: gekoppeld is, zelfde script werkt daar ook

---

*Project gestart: mei 2026 — Claude & Gerard*
