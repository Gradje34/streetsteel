"""
StreetSteel — Fabrikant introductieteksten (databron)
======================================================
Per fabrikant-slug: introtekst (NL) en officiele website.
Feiten met bron gecontroleerd. Breid deze dict uit naarmate je
meer fabrikanten van tekst voorziet; draai daarna fabrikant_intro.py.

Laat 'website' leeg ("") als je (nog) geen officiele site wilt tonen.
"""

INTROS = {
    "wavin": {
        "tekst": (
            "Wavin werd in 1955 opgericht in Zwolle, voortgekomen uit de "
            "Waterleiding Maatschappij Overijssel. De naam is een samentrekking "
            "van 'water' en 'vinyl'. Het bedrijf groeide uit tot Europees "
            "marktleider in kunststof leidingsystemen voor drinkwater, riolering, "
            "afvoer en regenwaterbeheer. Sinds 2012 maakt Wavin deel uit van het "
            "Mexicaanse Orbia (voorheen Mexichem)."
        ),
        "website": "https://www.wavin.com/nl-nl",
    },
    "dyka": {
        "tekst": (
            "DYKA werd in 1957 opgericht in Steenwijk door loodgieter Albert van "
            "Dijk, die een lichter alternatief zocht voor lood, gres en gietijzer. "
            "Hij begon met het maken van kunststof hulpstukken voor PVC-buizen. "
            "De naam DYKA ontstond in 1984 voor de Amerikaanse markt. Sinds 1987 "
            "is het bedrijf onderdeel van de Limburgse Vinyl Maatschappij en "
            "produceert het leidingsystemen voor riolering, drinkwater, "
            "regenwaterbeheer en binnenklimaat."
        ),
        "website": "https://www.dyka.nl",
    },
    "avk": {
        "tekst": (
            "AVK werd in 1941 opgericht in het Deense Galten door Aage Valdemar "
            "Kjaer, wiens initialen de bedrijfsnaam vormen. Het begon als een "
            "lokale machinewerkplaats; vanaf 1970 ontwikkelde zoon Niels Aage "
            "Kjaer de eerste afsluiter, waarna de productie van afsluiters van "
            "start ging. AVK is uitgegroeid tot een van 's werelds grootste "
            "producenten van afsluiters, hydranten en toebehoren voor water, gas "
            "en brandbeveiliging."
        ),
        "website": "https://www.avkvalves.eu",
    },
    "pipelife": {
        "tekst": (
            "Pipelife werd in 1989 opgericht als joint venture van het Belgische "
            "Solvay en het Oostenrijkse Wienerberger, met het hoofdkantoor in "
            "Wenen. Sinds 2012 is het volledig in handen van Wienerberger. "
            "Pipelife produceert kunststof leidingsystemen in PE, PP en PVC voor "
            "drinkwater, riolering, regenwaterbeheer, gasdistributie en "
            "kabelbescherming, en is actief in tientallen landen."
        ),
        "website": "https://www.pipelife.com",
    },
    "hauraton": {
        "tekst": (
            "HAURATON werd in 1956 opgericht in het Duitse Rastatt door Karl "
            "Hauger, aanvankelijk onder de naam Hauger & Jaegel. De huidige naam "
            "komt van HAUger, RAstatt en beTON. Het familiebedrijf is "
            "gespecialiseerd in afwateringssystemen voor de openbare ruimte, "
            "waaronder lijnafwatering, infiltratie en waterzuivering, en is "
            "bekend van zijn FASERFIX-goten van vezelversterkt beton."
        ),
        "website": "https://www.hauraton.com",
    },
    "kessel": {
        "tekst": (
            "KESSEL werd in 1963 opgericht door Bernhard Kessel in een garage bij "
            "Ingolstadt, aanvankelijk als gereedschapsmakerij. Vanaf 1969 maakte "
            "het bedrijf zijn eerste afwateringsproducten. Met het hoofdkantoor "
            "in het Duitse Lenting is KESSEL uitgegroeid tot specialist in "
            "afwateringstechniek: terugslagkleppen, opvoerinstallaties, afvoeren, "
            "putten en afscheiders."
        ),
        "website": "https://www.kessel.com",
    },
    "pam": {
        "tekst": (
            "Saint-Gobain PAM gaat terug tot 1856, toen in het Franse "
            "Pont-a-Mousson een ijzergieterij werd opgericht. Het bedrijf "
            "specialiseerde zich in gietijzeren buizen voor watertransport en "
            "groeide uit tot wereldleider in leidingsystemen van nodulair "
            "gietijzer. Sinds 1970 maakt PAM deel uit van de Saint-Gobain-groep. "
            "Naast buizen levert PAM ook putdeksels, straatkolken, hydranten en "
            "afsluiters voor de openbare ruimte."
        ),
        "website": "https://www.pamline.com",
    },
    "stradus": {
        "tekst": (
            "Stradus is een fabrikant van prefab betonproducten voor de inrichting "
            "van de openbare ruimte, zoals bestrating, boordstenen, "
            "verkeerselementen en straatmeubilair. Het bedrijf is actief in de "
            "Benelux en maakt deel uit van het Ierse bouwmaterialenconcern CRH. "
            "De producten zijn gericht op een toegankelijke, veilige en "
            "klimaatbestendige buitenruimte."
        ),
        "website": "https://www.stradus.be/nl",
    },
    "nyloplast": {
        "tekst": (
            "Nyloplast (BT Nyloplast) is een Nederlandse producent van kunststof "
            "verbindingsstukken, putten en kolken voor drukloze ondergrondse "
            "leidingsystemen. Sinds de jaren tachtig zijn de straat- en "
            "trottoirkolken van Nyloplast een vertrouwd onderdeel van het "
            "straatbeeld; tegenwoordig worden ze grotendeels uit gerecycled PVC "
            "gemaakt. Het bedrijf maakt deel uit van de Tessenderlo Group."
        ),
        "website": "https://www.btnyloplast.com/nl",
    },
    "tbs": {
        "tekst": (
            "TBS Soest werd begin jaren dertig opgericht door O. Zimmerman als "
            "Technisch Bureau voor gietijzerproducten Soest. Aanvankelijk maakte "
            "het bedrijf kolken en putafdekkingen van gietijzer; later vormde de "
            "gepatenteerde combinatie van gietijzer en beton de basis van het "
            "succes. TBS is in Nederland bekend van de vele putdeksels met het "
            "TBS-logo en is marktleider in kolken, putafdekkingen, schuiven en "
            "terugslagkleppen."
        ),
        "website": "",
    },
    "landustrie": {
        "tekst": (
            "Landustrie uit Sneek ontstond rond 1913 uit de samenvoeging van "
            "handelsfirma 'Het Landbouwhuis' en machinefabriek 'Industria'. "
            "Aanvankelijk richtte het bedrijf zich op polderbemaling, later "
            "verschoof de nadruk naar afvalwaterzuivering. Landustrie ontwikkelt "
            "en produceert pompen, vijzels en zuiveringsapparatuur in eigen huis "
            "en levert wereldwijd."
        ),
        "website": "https://landustrie.nl",
    },
    "lovink": {
        "tekst": (
            "IJzergieterij Lovink werd in 1911 opgericht in Terborg, als laatste "
            "van de vele gieterijen langs de Oude IJssel. Het bedrijf maakte "
            "gevarieerd gietwerk, waaronder straatdeksels en kabelmoffen, en "
            "kreeg in 2011 bij zijn eeuwfeest het predicaat 'Koninklijke'. De "
            "gieterijtak sloot in 2020; onder de naam Lovink Enertech wordt de "
            "productie van kunststof kabelmoffen voortgezet."
        ),
        "website": "",
    },
    "norinco": {
        "tekst": (
            "Norinco is een van oorsprong Frans bedrijf, gespecialiseerd in "
            "putdeksels, straatkolken en toegangsluiken van nodulair gietijzer "
            "voor ondergrondse netwerken: riolering, water, telecom en "
            "industrie. Sinds 2004 maakt Norinco deel uit van het Amerikaanse EJ "
            "(East Jordan Iron Works), dat sinds 2012 wereldwijd onder de merknaam "
            "EJ opereert."
        ),
        "website": "https://www.ejco.com",
    },
    "martens": {
        "tekst": (
            "De Koninklijke Martens Groep werd in 1881 opgericht door Hein Martens "
            "in Oosterhout, aanvankelijk als aannemer en steenhouwerij. In de "
            "jaren dertig begon Martens met betonproductie, waaronder "
            "rioolbuizen en -putten, en vanaf 1967 ook met kunststof "
            "leidingsystemen. Het familiebedrijf is uitgegroeid tot een "
            "producent van beton, kunststof en keramiek voor de grond-, weg- en "
            "waterbouw."
        ),
        "website": "https://martensgroep.eu/nl",
    },
    "alphacan": {
        "tekst": (
            "Alphacan is een van oorsprong Franse producent van kunststof "
            "leidingsystemen, met name buizen en hulpstukken van PVC voor "
            "riolering, hemelwaterafvoer en drukleidingen. Het bedrijf is al meer "
            "dan vijftig jaar actief in deze markt en maakt deel uit van de Kem "
            "One Group, met productievestigingen in meerdere Europese landen."
        ),
        "website": "",
    },
    "draka-polva": {
        "tekst": (
            "Draka Polva ontstond uit Polva Nederland, dat vanaf 1947 als een van "
            "de eerste in Nederland PVC-leidingen vervaardigde, en de "
            "kunststoftak van kabelfabrikant Draka. Onder de naam Draka Polva "
            "werden beide in 1985 samengebracht. Het bedrijf is een belangrijke "
            "voorloper van het huidige Pipelife en stond aan de basis van de "
            "Nederlandse kunststof leidingindustrie."
        ),
        "website": "",
    },
    "ewe": {
        "tekst": (
            "EWE (EWE Armaturen) is een Duitse fabrikant van armaturen voor de "
            "drinkwaterdistributie. Het assortiment omvat ondergrondse "
            "afsluiters, aanboorarmaturen, inbouwgarnituren, brandkranen en "
            "watermeterputten. De producten worden gebruikt door waterbedrijven "
            "en aannemers bij de aanleg en het onderhoud van waterleidingnetten."
        ),
        "website": "https://www.ewe-armaturen.de",
    },
    "samson": {
        "tekst": (
            "Samson (Samson Urban Elements) is een Nederlandse leverancier van "
            "gietijzeren producten voor de openbare ruimte, waaronder putdeksels, "
            "straatkolken, roosters en boomroosters, naast afsluiters en "
            "leidingsystemen voor water- en afvalwaterbeheer. Sinds 2025 maakt "
            "Samson deel uit van GroundLevel."
        ),
        "website": "https://www.samson.nl",
    },
}
