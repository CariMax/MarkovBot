import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Notwendige NLTK-Ressourcen laden
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def get_keywords(segment, num):
    """
    Extrahiert aus einem Segment (String) mithilfe von NLTK bis zu 'num'
    Schlüsselwörtern. Dabei werden Satzzeichen entfernt und Stopwörter (mit
    Ausnahme von "ich") herausgefiltert.
    """
    tokens = word_tokenize(segment, language="german")
    # Satzzeichen entfernen
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens_lower = [t.lower() for t in tokens]
    
    # Stopwörter laden und "ich" aus der Liste entfernen, damit es als Keyword auftaucht
    sw = set(stopwords.words("german"))
    if "ich" in sw:
        sw.remove("ich")
    
    # Filtere Stopwörter heraus
    filtered = [t for t in tokens_lower if t not in sw]
    
    freq = nltk.FreqDist(filtered)
    # Nimm die 'num' häufigsten Wörter
    keywords = [word for word, count in freq.most_common(num)]
    
    # Um möglichst die ursprüngliche Groß-/Kleinschreibung zu erhalten, 
    # wird für jedes gefundene Keyword das erste Vorkommen im Originaltext herangezogen.
    result = []
    for kw in keywords:
        for t in tokens:
            if t.lower() == kw:
                result.append(t)
                break
    return result

def make_the_list(window, delimiter, text):
    """
    Teilt den Text in Segmente (getrennt durch den delimiter) und erstellt für jedes
    Vorkommnis eines Wortes einen Kontext, der aus Informationen aus bis zu 'window'
    Segmenten zusammengesetzt wird.
    
    Vorgehen (am Beispiel window==3):
      - Wenn nur ein Vorgängersegment existiert (z.B. Segment1), werden aus dem
        einzigen Vorgängersegment 2 Schlüsselwörter (mit NLTK) verwendet.
      - Bei zwei Vorgängersegmenten (volles Fenster, z.B. Segment2):
           * Aus dem ältesten Segment (Segment0) wird 1 Schlüsselwort (das erste) entnommen.
           * Aus dem unmittelbar vorangehenden Segment (Segment1) werden 2 Schlüsselwörter entnommen.
      - Bei einem vollen Fenster (z.B. Segment3):
           * Aus dem ältesten Segment des Fensters (hier Segment1) wird nicht das erste,
             sondern _das letzte_ der extrahierten Schlüsselwörter verwendet.
           * Aus dem mittleren Segment (Segment2) werden 2 Schlüsselwörter verwendet.
      - Anschließend werden die Wörter aus dem aktuellen Segment, _vor_ der Stelle des Vorkommnisses,
        angehängt.
    
    Das Ergebnis ist ein Dictionary, in dem jeder Schlüssel (in Kleinbuchstaben) eine Liste
    von Kontextlisten enthält.
    """
    # Text in Segmente zerlegen und Leerzeichen entfernen
    segments = [seg.strip() for seg in text.split(delimiter) if seg.strip()]
    
    # Für jedes Segment werden Schlüsselwörter vorab extrahiert.
    # Die maximale Anzahl, die wir benötigen, ist: max(2, window-1)
    max_needed = max(2, window - 1)
    segment_keywords = []
    for seg in segments:
        kw = get_keywords(seg, max_needed)
        segment_keywords.append(kw)
    
    result = {}
    
    # Gehe alle Segmente durch
    for i, seg in enumerate(segments):
        tokens = word_tokenize(seg, language="german")
        # Für jede Position im Segment, also jedes Vorkommnis eines Wortes:
        for pos, word in enumerate(tokens):
            key = word.strip(".,!?").lower()  # als Schlüssel in Kleinbuchstaben
            # Wenn es im allerersten Segment vorkommt, gibt es keinen Kontext → überspringen
            if i == 0:
                continue
            
            context = []
            # Bestimme das Fenster, das wir betrachten:
            # Wenn noch nicht 'window' Segmente verfügbar sind, nehmen wir alle bisherigen Segmente;
            # ansonsten verwenden wir nur die letzten 'window' Segmente.
            start_idx = 0 if i < window else i - window + 1
            # Vorgängersegmente (ohne das aktuelle) 
            prev_indices = list(range(start_idx, i))
            n_prev = len(prev_indices)
            
            # Für die Vorgängersegmente: 
            # - Ist nur ein Segment vorhanden, so nehmen wir 2 Schlüsselwörter.
            # - Andernfalls: Für das j-te (0-indexiert) Segment im Fenster:
            #     * Wenn das Fenster voll ist (i >= window) und es das älteste Segment ist (j==0),
            #       nehmen wir _das letzte_ Schlüsselwort dieses Segments.
            #     * Für alle anderen nehmen wir (j+1) Schlüsselwörter (von Anfang der Liste).
            for j, seg_idx in enumerate(prev_indices):
                if n_prev == 1:
                    kws = segment_keywords[seg_idx][:2]
                else:
                    if i >= window and j == 0:
                        # Im vollen Fenster: Ältestes Segment → letztes Keyword nehmen
                        kws = segment_keywords[seg_idx][-1:]
                    else:
                        num_kw = j + 1
                        kws = segment_keywords[seg_idx][:num_kw]
                context.extend(kws)
            
            # Füge nun die Wörter aus dem aktuellen Segment _vor_ dem Vorkommnis hinzu
            current_context = tokens[:pos]
            current_context = [w for w in current_context if w not in string.punctuation]
            context.extend(current_context)
            
            # Den Kontext zur Ergebnisliste für das Wort (Schlüssel) hinzufügen
            if key not in result:
                result[key] = []
            result[key].append(context)
    return result

# --- Beispielaufruf ---
#if __name__ == '__main__':
if False:
    text = ("Ein Hund geht schlafen[DONE]"
            "ich gehe auch schlafen[DONE]"
            "ich wache wieder auf[DONE]"
            "Eingekackt habe ich.")
    
    ergebnis = make_the_list(3, "[DONE]", text)
    
    import pprint
    pprint.pprint(ergebnis)
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Notwendige NLTK-Ressourcen laden
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def get_keywords(segment, num):
    """
    Extrahiert mithilfe von NLTK bis zu 'num' Schlüsselwörter aus einem Segment.
    Dabei werden Satzzeichen entfernt und Stopwörter (mit Ausnahme von "ich") gefiltert.
    """
    tokens = word_tokenize(segment, language="german")
    # Entferne Satzzeichen
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens_lower = [t.lower() for t in tokens]
    
    sw = set(stopwords.words("german"))
    # Damit "ich" als Schlüsselwort auftaucht, entfernen wir es aus der Stopwortliste
    if "ich" in sw:
        sw.remove("ich")
    
    filtered = [t for t in tokens_lower if t not in sw]
    freq = nltk.FreqDist(filtered)
    # Nimm die 'num' häufigsten Wörter
    keywords = [word for word, count in freq.most_common(num)]
    
    # Um möglichst die ursprüngliche Groß-/Kleinschreibung beizubehalten,
    # wird für jedes gefundene Keyword das erste Vorkommnis im Originalsegment herangezogen.
    result = []
    for kw in keywords:
        for t in tokens:
            if t.lower() == kw:
                result.append(t)
                break
    return result

def make_tail_area(window, delimiter, text):
    """
    Diese Funktion verarbeitet **nur das Ende** eines Textes.
    
    Vorgehen:
      - Der Text wird anhand des Delimiters in Segmente (z. B. "[DONE]") aufgeteilt.
      - Es werden nur die letzten 'window' Segmente betrachtet (falls weniger vorhanden, werden alle verwendet).
      - Für jedes Vorkommnis in dem **letzten Segment** wird ein Kontext erstellt,
        der aus folgenden Teilen besteht:
         1. Den Schlüsselwörtern aus den vorangehenden Segmenten (innerhalb des Tail-Fensters):
            - Ist nur ein Vorgänger vorhanden, werden z. B. 2 Schlüsselwörter genutzt.
            - Bei einem vollen Fenster (z. B. 3 Segmente) wird aus dem ältesten Segment (im Tail)
              statt des ersten – das letzte der extrahierten Schlüsselwörter – verwendet, und
              aus den folgenden Segmenten jeweils eine zunehmende Anzahl an Schlüsselwörtern.
         2. Den Wörtern im aktuellen Segment, die **vor** dem Vorkommnis stehen.
      - Das Ergebnis ist ein Dictionary, in dem für jeden Schlüssel (Wort in Kleinbuchstaben)
        – ähnlich wie in deinem Beispiel „dict.ich[0]“ – **eine einzige Kontextliste** abgelegt wird.
    """
    # Den Text in Segmente zerlegen und überflüssige Leerzeichen entfernen
    segments = [seg.strip() for seg in text.split(delimiter) if seg.strip()]
    
    # Nimm die letzten 'window' Segmente (oder alle, falls es weniger gibt)
    tail_segments = segments if len(segments) < window else segments[-window:]
    
    # Für jedes Segment im Tail werden Schlüsselwörter extrahiert.
    # Wir benötigen maximal max(2, window-1) Schlüsselwörter.
    max_needed = max(2, window - 1)
    tail_keywords = []
    for seg in tail_segments:
        kws = get_keywords(seg, max_needed)
        tail_keywords.append(kws)
    
    result = {}
    # Das letzte Segment im Tail ist das aktuelle Segment
    current_seg = tail_segments[-1]
    tokens = word_tokenize(current_seg, language="german")
    
    tail_len = len(tail_segments)  # Anzahl der Segmente im Tail
    # Wir verarbeiten jedes Vorkommnis im letzten Segment
    for pos, word in enumerate(tokens):
        key = word.strip(".,!?").lower()  # Schlüssel in Kleinbuchstaben
        context = []
        
        # Kontext aus den vorangehenden Segmenten des Tail:
        # Alle Segmente außer dem letzten werden als Vorgänger betrachtet.
        n_prev = tail_len - 1  # Anzahl der vorangehenden Segmente
        for j in range(n_prev):
            # Falls nur ein Segment vorhanden ist, nehmen wir 2 Schlüsselwörter
            if n_prev == 1:
                kws = tail_keywords[j][:2]
            else:
                # Bei vollem Fenster (also wenn tail_len == window) verwenden wir:
                # Für das älteste Segment (j==0) das letzte Schlüsselwort,
                # ansonsten für das j-te Segment die ersten (j+1) Schlüsselwörter.
                if tail_len == window and j == 0:
                    kws = tail_keywords[j][-1:]
                else:
                    num_kw = j + 1
                    kws = tail_keywords[j][:num_kw]
            context.extend(kws)
        
        # Kontext aus dem aktuellen Segment: alle Wörter vor dem Vorkommnis
        current_context = tokens[:pos]
        current_context = [t for t in current_context if t not in string.punctuation]
        context.extend(current_context)
        
        # Wir speichern nur den Kontext des **ersten Vorkommnisses** eines jeden Wortes
        if key not in result:
            result[key] = context
    return result

# --- Beispielaufruf ---

if False:
    text = ("Ein Hund geht schlafen[DONE]"
            "ich gehe auch schlafen[DONE]"
            "ich wache wieder auf[DONE]"
            "Eingekackt habe ich.")
    
    tail_area = make_tail_area(3, "[DONE]", text)
    
    import pprint
    print("Tail Area (nur das Ende des Textes):")
    pprint.pprint(tail_area)
