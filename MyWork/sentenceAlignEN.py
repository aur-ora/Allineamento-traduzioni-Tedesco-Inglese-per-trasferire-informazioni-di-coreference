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
from spacy_stanza import StanzaLanguage
from nltk.corpus import wordnet as wn
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

#snlp = stanza.Pipeline(lang="en")
#nlp = StanzaLanguage(snlp)

nlp = spacy.load("en_core_web_sm")

stopwords = open("english-stop-words-large.txt", "r")
stopwords = stopwords.readlines()
stopwords = ('').join(stopwords)

'''
Il metodo sentencesen prende in input il file del testo inglese e lo divide in frasi, restituendo una lista di stringhe (frasi)
'''


'''def sentencesen(enfile):
    sent = []
    doc = nlp(enfile.read())
    for i in doc.sents:
        sent.append(i)
    return sent
'''

'''
Il metodo createSynset prende in input il testo inglese e restituisce una lista di lista in cui la ogni lista interna corrisponde
a tutti i synset di tutte le parole in una frase, quindi per prendere l'insieme dei synset in una sola frase basta prendere l'indice della lista grande
(l'insieme della prima frase sarà all'indice 0, della seconda all'indice 1)
'''


def createSynset(enfile):
    sent = []
    d = {}
    doc = nlp(enfile.read())
    for i in doc.sents:
        sent.append(i)

    synsets = [] #creo la lista che conterrà la lista dei synset
    for sentence in sent: #per ciascuna frase del testo
        synset = [] #creo la lista in cui ci saranno i synset per ciasuna parola in una frase
        for token in sentence:
            token = str(token.lemma_).lower() #prendo il lowercase di ogni parola
            if token not in stopwords:
                synset += ([wn.lemmas(token)])
                if token not in d:
                    d[token] = 1
                else:
                    d[token] += 1
        synsets.append(synset)
    return synsets
    #print(d)

