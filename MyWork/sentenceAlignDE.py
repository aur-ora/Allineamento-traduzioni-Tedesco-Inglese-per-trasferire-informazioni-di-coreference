'''
Allinamento tra le frasi di un testo inglese e un testo tedesco, serve per confrontarli e vedere quale frase inglese/tedesca è la traduzione
di un'altra frase tedesca/inglese.
I passaggi da fare sono:
-Bag of Synsets:
    1. Eliminazione delle stopwords
    2. Ricavare attraverso il modulo spacy-wordnet i lemmi e i synset dai token delle parole restanti (per entrambe le frasi)
    3. Confronto tra gli insiemi ottenuti per la lingua inglese e la lingua tedesca
'''

import spacy
import stanza
import de_core_news_sm
from spacy_stanza import StanzaLanguage
from nltk.corpus import wordnet as wn
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

#snlp = stanza.Pipeline(lang="de")
#nlp = StanzaLanguage(snlp)

nlp = de_core_news_sm.load()

stopwords = open("german-stop-words.txt", "r")
stopwords = stopwords.readlines()
stopwords = ('').join(stopwords)


'''
Il metodo sentencesen prende in input il file del testo tedesco e lo divide in frasi, restituendo una lista di stringhe (frasi)
'''


'''def sentencesde(defile):
    sent = []
    doc = nlp(defile.read())
    for i in doc.sents:
        sent.append(i)
    return sent
'''

'''
Il metodo createSynset prende in input il testo inglese e restituisce una lista di lista in cui la ogni lista interna corrisponde
a tutti i synset di tutte le parole in una frase, quindi per prendere l'insieme dei synset in una sola frase basta prendere l'indice della lista grande
(l'insieme della prima frase sarà all'indice 0, della seconda all'indice 1)
'''


def createSynsetDE(file):
    sent = []
    d = {}
    doc = nlp(file.read())
    for i in doc.sents:
        sent.append(i)

    synsets = []
    for sentence in sent:
        synset = []
        for token in sentence:
            if token.lemma_ not in stopwords:
                synset += ([wn.lemmas(token.lemma_, lang="deu")])
        synsets.append(synset)
    return synsets


