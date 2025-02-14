import Synonyms
import random
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stops = list(set(stopwords.words('german')))
text = """
Ein Abenteurer ist jemand, der den Mut hat, das Unbekannte zu erforschen und sich in unbekannte Gefilde zu wagen. Er lebt nicht nach den gewohnten Regeln der Gesellschaft, sondern folgt seiner eigenen Intuition und Neugier. Sein Leben ist von ständigem Aufbruch und Entdeckung geprägt, stets auf der Suche nach neuen Horizonten und unerforschten Gebieten.
Für den Abenteurer sind Herausforderungen keine Hindernisse, sondern Chancen, sich zu beweisen. Ob er sich durch dichte Dschungel schlägt, unentdeckte Gebirgspässe überquert oder die tiefsten Ozeane durchquert – sein Ziel ist es immer, die Grenzen des Möglichen zu verschieben und neue Erfahrungen zu sammeln. Der Abenteurer fühlt sich frei, wenn er fernab der Zivilisation in der Wildnis lebt, doch auch in Städten, die er auf seinen Reisen besucht, spürt er den Puls der Welt und das Drängen nach neuen Erlebnissen.
Seine Geschichte ist eine Sammlung von Begegnungen mit fremden Kulturen, wilden Tieren und atemberaubenden Landschaften. Doch der wahre Schatz, den er auf seinen Reisen findet, ist oft nicht in Gold und Edelsteinen zu messen, sondern in den Geschichten, die er erlebt, den Lektionen, die er lernt, und den Erinnerungen, die er in seinem Herzen trägt.
Ein Abenteurer ist nicht nur ein Entdecker im physischen Sinne, sondern auch ein Entdecker seiner selbst. Jede Reise, jede Herausforderung, jede Begegnung bringt ihn näher zu dem, was er wirklich ist. Denn für einen wahren Abenteurer ist der wahre Schatz die Reise selbst, das stetige Streben nach Wissen und die Freude daran, das Leben in all seiner Vielfalt zu erleben.
"""

words = text.split(" ")
result = ""
i = 1
syn_data = Synonyms.load_synonyms("synonyme.json")
for word in words:
    syn = Synonyms.find_synonyms(word, syn_data)
    #print(syn)
    if syn == []:
        nw = word
    elif not word in stops:
        nw = random.choice(syn)
    else:
        nw = word
    result += nw + " "
    print(str(i) + "/", len(words), end='\r')
    i += 1
print(result)