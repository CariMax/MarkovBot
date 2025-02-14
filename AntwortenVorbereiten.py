from datasets import load_dataset
from deep_translator import GoogleTranslator

# ConvAI2-Datensatz laden
# Beispiel für das Laden eines Teils des Datensatzes
dataset = load_dataset("conv_ai_2", split="train[:0.01%]")  # Nur 10% des Datensatzes laden
print("Dataset geloadet")

# Google Translator-Objekt erstellen
translator = GoogleTranslator(source="en", target="de")

# Alle Antworten übersetzen und in einer Liste speichern
antworten_liste = []
for entry in dataset:
    englische_antwort = entry["text"]
    deutsche_antwort = translator.translate(englische_antwort)  # Übersetzen
    antworten_liste.append(deutsche_antwort)  # In Liste speichern

# Übersetzte Antworten in einer Textdatei speichern (eine Antwort pro Zeile)
with open("uebersetzte_antworten.txt", "w", encoding="utf-8") as file:
    for antwort in antworten_liste:
        file.write(antwort.replace("\n", " ") + "\n")

print(f"✅ Übersetzung abgeschlossen! {len(antworten_liste)} Antworten gespeichert in 'uebersetzte_antworten.txt'.")
