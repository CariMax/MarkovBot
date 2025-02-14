import json
import OpenThesaurus
def load_synonyms(file_path):
    """
    Lädt die Synonymdaten aus einer JSON-Datei.
    """
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return json.load(file)

def find_synonyms(word, synonyms_data):
    """
    Findet Synonyme für ein gegebenes Wort aus den geladenen Synonymdaten.
    """
    for entry in synonyms_data:
        if entry[0].lower() == word.lower():
            return entry[1]  # Liste der Synonyme zurückgeben
        elif word in entry[1]:
            return entry[1]
        else:
            #return OpenThesaurus.find_synonyms(word)
            pass
    return []  # Falls keine Synonyme gefunden wurden

# Beispielverwendung:
synonyms_data = load_synonyms("synonyme.json")
word = "Hallo"
synonyms = find_synonyms(word, synonyms_data)

print(synonyms)