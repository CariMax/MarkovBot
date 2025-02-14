text = """
Künstliche Intelligenz (KI) ist eine der bedeutendsten technologischen Entwicklungen der modernen Zeit.<[DONE]> Sie hat das Potenzial, zahlreiche Bereiche unseres Lebens zu verändern.<[DONE]> Von der Automatisierung bis hin zur kreativen Unterstützung – KI ist heute allgegenwärtig.<[DONE]>  Die Ursprünge der Künstlichen Intelligenz reichen bis in die Mitte des 20. Jahrhunderts zurück.<[DONE]> In den 1950er-Jahren begannen Wissenschaftler, die Grundlagen für maschinelles Lernen und intelligente Systeme zu legen.<[DONE]> Einer der ersten bedeutenden Meilensteine war die Entwicklung des Turing-Tests durch Alan Turing.<[DONE]>  In den darauffolgenden Jahrzehnten gab es immer wieder Höhen und Tiefen in der KI-Forschung.<[DONE]> Während in den 1970er- und 1980er-Jahren der sogenannte „KI-Winter“ herrschte, erlebte die Technologie in den letzten zwei Jahrzehnten einen enormen Aufschwung.<[DONE]> Fortschritte in der Rechenleistung, große Datenmengen und neue Algorithmen haben zur heutigen KI-Revolution beigetragen.<[DONE]>  Eine der wichtigsten Technologien hinter moderner KI ist das maschinelle Lernen.<[DONE]> Dabei handelt es sich um Methoden, mit denen Computer eigenständig aus Daten lernen können.<[DONE]> Besonders leistungsfähig ist das sogenannte Deep Learning, das auf künstlichen neuronalen Netzen basiert.<[DONE]> Diese Netze sind inspiriert vom menschlichen Gehirn und können komplexe Muster in Daten erkennen.<[DONE]>KI wird heute in vielen Branchen eingesetzt.<[DONE]> In der Medizin hilft sie bei der Diagnose von Krankheiten.<[DONE]> In der Industrie optimiert sie Produktionsprozesse.<[DONE]> Im Finanzsektor analysiert sie Markttrends und unterstützt bei Investitionsentscheidungen.<[DONE]>  Sprachverarbeitung ist ein weiteres wichtiges Anwendungsgebiet.<[DONE]> Systeme wie Chatbots und Sprachassistenten basieren auf KI-Technologien.<[DONE]> Sie können Texte verstehen, Fragen beantworten und sogar kreative Inhalte generieren.<[DONE]>  Auch im Bereich der Bildverarbeitung leistet KI Erstaunliches.<[DONE]> Sie kann Gesichter erkennen, Objekte identifizieren und sogar Bilder generieren.<[DONE]> Anwendungen reichen von Sicherheitsmaßnahmen bis hin zur Kunst.<[DONE]>  Trotz all dieser Fortschritte gibt es auch Herausforderungen und ethische Fragen.<[DONE]> Eine der größten Sorgen ist der Einfluss von KI auf den Arbeitsmarkt.<[DONE]> Viele Berufe könnten durch Automatisierung ersetzt werden.<[DONE]> Gleichzeitig entstehen jedoch neue Berufsfelder, die mit KI-Technologie arbeiten.<[DONE]>  Ein weiteres Problem ist die Frage der Fairness.<[DONE]> KI-Systeme können Vorurteile enthalten, wenn sie mit voreingenommenen Daten trainiert werden.<[DONE]> Dies kann zu diskriminierenden Entscheidungen führen.<[DONE]> Daher ist es wichtig, dass KI verantwortungsbewusst entwickelt wird.<[DONE]>  Auch die Transparenz ist ein kritisches Thema.<[DONE]> Viele moderne KI-Modelle sind sogenannte „Black Boxes“.<[DONE]> Das bedeutet, dass ihre Entscheidungen schwer nachzuvollziehen sind.<[DONE]> Wissenschaftler arbeiten daran, KI-Systeme erklärbarer zu machen.<[DONE]>  Ein weiteres ethisches Thema betrifft den Datenschutz.<[DONE]> KI-Systeme benötigen oft große Mengen an Daten, um effektiv zu funktionieren.<[DONE]> Dies wirft Fragen darüber auf, wie persönliche Informationen geschützt werden können.<[DONE]>  Trotz dieser Herausforderungen überwiegen die Chancen.<[DONE]> KI hat das Potenzial, viele gesellschaftliche Probleme zu lösen.<[DONE]> Sie kann in der Medizin neue Behandlungsmethoden ermöglichen.<[DONE]> Sie kann in der Umwelttechnik helfen, den Klimawandel zu bekämpfen.<[DONE]>  Die Zukunft der Künstlichen Intelligenz ist vielversprechend.<[DONE]> Forscher arbeiten an immer leistungsfähigeren Modellen.<[DONE]> Gleichzeitig wird an ethischen Richtlinien gearbeitet, um einen verantwortungsvollen Einsatz sicherzustellen.<[DONE]> Insgesamt ist KI eine der spannendsten Entwicklungen unserer Zeit.<[DONE]> Sie wird unser Leben in vielerlei Hinsicht beeinflussen.<[DONE]> Dabei ist es wichtig, die Chancen und Risiken gleichermaßen im Blick zu behalten.<[DONE]>
"""
import prepData
import difflib
import pprint
import difflib

def find_most_similar_word(data, input_list):
    def similarity_score(group, input_list):
        word_score = 0
        matched_words = []

        # Wort-für-Wort Ähnlichkeit prüfen
        for word in input_list:
            matches = difflib.get_close_matches(word, group, n=1, cutoff=0.6)
            if matches:
                best_match = matches[0]
                word_score += difflib.SequenceMatcher(None, word, best_match).ratio()
                matched_words.append(best_match)

        # Reihenfolgebewertung (Sequenzähnlichkeit)
        seq_score = difflib.SequenceMatcher(None, group, matched_words).ratio()
        
        # Gesamtpunktzahl gewichten
        return (word_score * 0.7) + (seq_score * 0.3)

    best_match = None
    highest_score = 0

    for key, groups in data.items():
        for group in groups:
            if isinstance(group, str):  # Falls ein einzelner String als Liste verarbeitet werden muss
                group = [group]

            score = similarity_score(group, input_list)
            print(f"{key}: Score {score}")  # Debug-Ausgabe für Analyse
            
            if score > highest_score:
                highest_score = score
                best_match = key

    print("Best match:", best_match)
    return best_match



contexts = prepData.make_the_list(3, "<[DONE]>", text)
#print(contexts)
start_text = """
Künstliche Intelligenz (KI) ist eine der bedeutendsten technologischen Entwicklungen der modernen Zeit.<[DONE]> Sie hat das Potenzial, zahlreiche Bereiche unseres Lebens zu verändern.<[DONE]> Von der Automatisierung bis hin zur kreativen Unterstützung – KI ist heute allgegenwärtig.<[DONE]>  Die Ursprünge der Künstlichen Intelligenz reichen bis in die Mitte des 20. Jahrhunderts zurück.<[DONE]> In den 1950er-Jahren begannen Wissenschaftler, die Grundlagen für maschinelles Lernen und intelligente Systeme zu legen.<[DONE]> Einer der ersten bedeutenden Meilensteine war die Entwicklung des Turing-Tests durch Alan Turing.<[DONE]>  In den darauffolgenden Jahrzehnten gab es immer wieder Höhen und Tiefen in der KI-Forschung.<[DONE]> Während in den 1970er- und 1980er-Jahren der sogenannte „KI-Winter“ herrschte, erlebte die Technologie in den letzten zwei Jahrzehnten einen enormen Aufschwung.
"""
print(start_text, "\n\n\n\n")
contexts_start_text = prepData.make_the_list(3, "<[DONE]>", start_text)
print(contexts_start_text.keys())
#print(contexts_start_text)
context_start_text = contexts_start_text["aufschwung"][-1]
print(context_start_text)

for i in range(5):
    next_word = find_most_similar_word(contexts, context_start_text)
    print("Netx Word:", next_word)
    start_text += " " + next_word
    context_start_text = prepData.make_tail_area(3, "<[DONE]>", start_text)
    if next_word.endswith("."):
        break
print(start_text)