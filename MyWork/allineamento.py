import spacy
import de_core_news_sm
from nltk.corpus import wordnet as wn

#carico il file delle stopword inglesi
stopwordsEN = ("").join(open("english-stop-words-large.txt", "r").readlines())
'''stopwordsEN = open("english-stop-words-large.txt", "r")
stopwordsEN = stopwordsEN.readlines()
stopwordsEN = ("").join(stopwordsEN) #lo salvo come una lista di stringhe
'''#carico il file delle stopword tedesche
stopwordsDE = ("").join(open("german-stop-words.txt", "r").readlines())
'''stopwordsDE = open("german-stop-words.txt", "r")
stopwordsDE = stopwordsDE.readlines()
stopwordsDE = ("").join(stopwordsDE) #lo salvo come una lista di stringhe
'''#carico i modelli di spacy per le due lingue
nlp = spacy.load("en_core_web_sm")
nlp2 = de_core_news_sm.load()

#Il metodo createSet_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
def createSet_en(enfile):
    sent_en = [] #inizializzo le due liste che conterranno le frasi del testo inglese
    synset_en = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    doc = nlp(enfile.read())
    #Mi salvo ogni frase separatamente all'intero di una listA
    for s in doc.sents:
        sent_en.append(s)

    for sent in sent_en: #per ogni frase nel testo inglese
        set_en = set() #creo un'insieme in cui si troveranno i synset
        for token in sent:
            token = str(token.lemma_).lower() #prendo il lemma lowercase di ogni parola
            if token not in stopwordsEN: #se il lemma della parola non è un stopword
                set_en.add([wn.lemmas(token)]) #trovo l'insieme dei synset del lemma e  lo aggiungo all'insieme
        synset_en.append(set_en) #aggiungo l'insieme dei synset in una lista
    return synset_en

#Il metodo createSet_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
def createSet_de(defile):
    sent_de = [] #inizializzo le due liste che conterranno le frasi del testo tedesco
    synset_de = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc2 = nlp(defile.read())
    #Mi salvo ogni frase separatamente all'intero di una lista
    for s in doc2.sents:
        sent_de.append(s)

    for sent in sent_de:#per ogni frase nel testo tedesco
        set_de = set() #creo un'insieme in cui si troveranno i synset
        for token in sent:
            token = str(token.lemma_).lower() #prendo il lemma lowercase di ogni parola
            if token not in stopwordsEN: #se il lemma della parola non è un stopword
                set_de.add(wn.lemmas(token, lang="deu")) #trovo l'insieme dei synset del lemma e  lo aggiungo all'insieme
        synset_de.append(set_de) #aggiungo l'insieme dei synset in una lista
    return synset_de