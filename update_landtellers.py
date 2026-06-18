"""
StreetSteel — Landtotalen toevoegen aan tellers.json
=====================================================
Telt per Europees land de foto's van alle steden op en schrijft
een landsleutel (bijv. "europa/duitsland": 119) terug naar tellers.json.

Landen zonder steden hebben hun landsleutel al (bijv. "europa/frankrijk": 46);
die laat dit script ongemoeid.

Veilig om meermaals te draaien.
Gebruik: python update_landtellers.py
"""

import json
from pathlib import Path

TELLERS = Path(r"C:\streetsteel\data\tellers.json")


def main():
    if not TELLERS.exists():
        print(f"FOUT: {TELLERS} niet gevonden.")
        return

    tellers = json.loads(TELLERS.read_text(encoding="utf-8"))

    # Som per land op basis van stadssleutels "europa/<land>/<stad>"
    land_totalen = {}
    for sleutel, aantal in tellers.items():
        if not sleutel.startswith("europa/"):
            continue
        rest = sleutel[len("europa/"):]
        if "/" in rest:                       # het is een stad
            land = rest.split("/")[0]
            land_totalen[land] = land_totalen.get(land, 0) + aantal

    # Schrijf landsleutels terug (alleen voor landen MET steden)
    gewijzigd = 0
    for land, totaal in sorted(land_totalen.items()):
        sleutel = f"europa/{land}"
        if tellers.get(sleutel) != totaal:
            tellers[sleutel] = totaal
            gewijzigd += 1
        print(f"  {sleutel} = {totaal}")

    TELLERS.write_text(
        json.dumps(tellers, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nKlaar. {gewijzigd} landsleutel(s) toegevoegd/bijgewerkt.")
    print("Landen zonder steden (Frankrijk, Portugal, etc.) hadden hun sleutel al.")


if __name__ == "__main__":
    main()
