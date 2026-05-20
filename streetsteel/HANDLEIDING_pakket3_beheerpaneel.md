# 📋 HANDLEIDING: Beheerpaneel (Pakket 3)
## StreetSteel.com — Decap CMS

---

## Wat is het beheerpaneel?

Het beheerpaneel is een website die je opent in je browser op:
**https://streetsteel.com/admin/**

Daar kun je zonder te programmeren:
- ✅ Foto's uploaden per stad of fabrikant
- ✅ Teksten schrijven en bewerken
- ✅ Nieuwe landen, steden en fabrikanten aanmaken
- ✅ Fabrikant-introducties invoeren (na AI-generatie)
- ✅ Site-instellingen beheren (PayPal, AdSense, over mij)

---

## Hoe werkt het technisch?

```
Jij typt in beheerpaneel
        ↓
Decap CMS slaat op in GitHub
        ↓
Netlify detecteert wijziging
        ↓
Website wordt automatisch bijgewerkt (±1 minuut)
```

Je hoeft dus **nooit** handmatig bestanden te uploaden naar Netlify.

---

## STAP 1 — GitHub account aanmaken

Het beheerpaneel slaat alles op via GitHub (gratis).

1. Ga naar **https://github.com**
2. Klik op **"Sign up"**
3. Kies een gebruikersnaam, e-mailadres en wachtwoord
4. Bevestig je e-mailadres
5. ✅ Klaar — onthoud je gebruikersnaam en wachtwoord

---

## STAP 2 — Websitebestanden uploaden naar GitHub

1. Log in op **https://github.com**
2. Klik op de groene knop **"New repository"**
3. Geef het de naam: `streetsteel`
4. Zet op **Public** (vereist voor gratis Netlify hosting)
5. Klik op **"Create repository"**

Nu upload je de websitebestanden:
1. Klik op **"uploading an existing file"**
2. Sleep de inhoud van `M:\Streetsteel.com\website\` naar het venster
3. Klik op **"Commit changes"**

---

## STAP 3 — Netlify koppelen aan GitHub

1. Ga naar **https://netlify.com**
2. Klik op **"Sign up"** → kies **"Sign up with GitHub"**
3. Geef Netlify toegang tot je GitHub account
4. Klik op **"Add new site"** → **"Import from Git"**
5. Kies **GitHub** → selecteer je `streetsteel` repository
6. Netlify detecteert automatisch de instellingen
7. Klik op **"Deploy site"**

Na ±1 minuut is je site live op een tijdelijk adres zoals:
`https://wonderful-cupcake-123456.netlify.app`

---

## STAP 4 — Netlify Identity activeren (voor beheerpaneel)

Het beheerpaneel heeft een inlogsysteem nodig:

1. Ga in Netlify naar je site → **"Site settings"**
2. Klik op **"Identity"** in het linkermenu
3. Klik op **"Enable Identity"**
4. Scroll naar beneden naar **"Git Gateway"**
5. Klik op **"Enable Git Gateway"**

Nu kun je jezelf uitnodigen als beheerder:
1. Ga naar **"Identity"** → **"Invite users"**
2. Vul je eigen e-mailadres in
3. Je ontvangt een e-mail — klik op de link en stel een wachtwoord in

---

## STAP 5 — Beheerpaneel openen

Ga naar: **https://jouw-netlify-adres.netlify.app/admin/**

1. Klik op **"Login with Netlify Identity"**
2. Vul je e-mailadres en wachtwoord in
3. ✅ Je bent nu in het beheerpaneel!

---

## Het beheerpaneel gebruiken

### Nieuwe stad toevoegen (Nederland)

1. Klik op **"🇳🇱 Nederland — Steden"** in het linkermenu
2. Klik op **"Nieuwe Stad"**
3. Vul in:
   - **Stadsnaam**: bijv. `Assen`
   - **URL-naam**: bijv. `assen`
   - **Omschrijving (NL)**: optionele tekst
4. Klik op **"Foto's toevoegen"**
5. Upload foto's via de upload-knop
6. Koppel elke foto eventueel aan een fabrikant via het dropdown
7. Klik op **"Opslaan"**

De website wordt automatisch bijgewerkt! ✅

### Nieuwe fabrikant toevoegen

1. Klik op **"🏭 Fabrikanten"**
2. Klik op **"Nieuwe Fabrikant"**
3. Vul in:
   - **Naam**: bijv. `Rexnord`
   - **URL-naam**: bijv. `rexnord`
   - **Website**: bijv. `https://www.rexnord.com`
   - **Land van herkomst**: bijv. `Duitsland`
   - **Introductietekst (NL)**: plak hier de AI-gegenereerde tekst
4. Upload foto's
5. Klik op **"Opslaan"**

### AI-introductietekst genereren voor fabrikant

1. Open een nieuw Claude gesprek op **claude.ai**
2. Typ: *"Schrijf een korte introductie (3-4 zinnen) over putdeksel-fabrikant [NAAM]. Noem het land van herkomst, het soort producten en wat ze herkenbaar maakt in het straatbeeld."*
3. Controleer de tekst
4. Plak hem in het beheerpaneel bij de fabrikant

---

## Fototellers bijwerken

Na het uploaden van nieuwe foto's moet je de tellers bijwerken:

1. Zorg dat `update_tellers.py` op je bureaublad staat
2. Open een zwart venster (cmd)
3. Typ:
   ```
   cd %USERPROFILE%\Desktop
   python update_tellers.py
   ```
4. Het script telt alle foto's en schrijft de tellers weg
5. Upload de bijgewerkte `main.js` opnieuw via GitHub

---

## Eigen domein koppelen (streetsteel.com)

Dit doen we in **Pakket 4** — maar alvast weten:

1. Koop streetsteel.com bij **TransIP** (~€12/jaar)
2. Ga in Netlify naar **"Domain settings"**
3. Klik op **"Add custom domain"**
4. Vul in: `streetsteel.com`
5. Netlify geeft je DNS-instellingen
6. Stel die in bij TransIP
7. SSL certificaat wordt automatisch aangemaakt ✅

---

## Passief inkomen activeren

### PayPal ✅
Al ingebouwd — staat onderaan elke pagina en drijvend rechtsonder.
Aanpassen via: **Beheerpaneel → ⚙️ Site-instellingen → PayPal link**

### Ko-fi ✅
1. Maak account op **https://ko-fi.com**
2. Kies je paginanaam
3. Ga in beheerpaneel naar **Site-instellingen → Ko-fi link**
4. Vul je Ko-fi URL in

### Google AdSense
1. Ga naar **https://adsense.google.com**
2. Meld je aan met je Google account
3. Voer `streetsteel.com` in als website
4. Wacht op goedkeuring (duurt 1-4 weken)
5. Na goedkeuring krijg je een publisher ID (ca-pub-XXXXXXXX)
6. Ga in beheerpaneel naar **Site-instellingen → Google AdSense code**
7. Vul je publisher ID in

**Let op:** Google AdSense vereist minimaal 20-30 unieke pagina's met originele content. Streetsteel.com voldoet daar ruimschoots aan met 100+ pagina's.

---

## Veelgestelde vragen

**Hoe lang duurt het tot wijzigingen live zijn?**
Gemiddeld 30-60 seconden na het opslaan in het beheerpaneel.

**Kan ik het beheerpaneel ook op mijn mini-pc gebruiken?**
Ja! Het beheerpaneel is een website — open gewoon de URL in elke browser.

**Wat als ik een foto wil verwijderen?**
Open de stad of fabrikant in het beheerpaneel, klik op de foto en klik op het prullenbak-icoon.

**Kan ik een foto aan meerdere fabrikanten koppelen?**
Momenteel aan één fabrikant per foto. Voor meerdere koppelingen: upload dezelfde foto bij beide fabrikanten.

---

*Handleiding gemaakt door Claude voor Gerard — streetsteel.com project*
*Pakket 3 — Beheerpaneel*
