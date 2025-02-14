import requests
import re

def filter_synonyme(synonyme_liste):
    gefiltert = []
    for wort in synonyme_liste:
        # Nur Wörter mit maximal zwei Wörtern zulassen (keine Sätze oder Phrasen)
        if re.match(r"^[a-zA-ZäöüÄÖÜß\-]+( [a-zA-ZäöüÄÖÜß\-]+)?$", wort):
            gefiltert.append(wort)
    return gefiltert

def find_synonyms(wort):
    # Wort für die Suche


    # OpenThesaurus API aufrufen
    url = f"https://www.openthesaurus.de/synonyme/search?q={wort}&format=application/json"
    response = requests.get(url)
    daten = response.json()

    # Synonyme extrahieren
    synonyme = []
    for synset in daten.get("synsets", []):
        for term in synset.get("terms", []):
            synonyme.append(term["term"])
    #print(synonyme)
    return filter_synonyme(list(set(synonyme)))

#print(find_synonyms("Hallo"))