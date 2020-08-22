import spacy
import de_core_news_sm
from nltk.corpus import wordnet as wn

stopwordsEN = "".join(open("english-stop-words-large.txt", "r").readlines()) #carico il file delle stopword inglesi
stopwordsDE = "".join(open("german-stop-words.txt", "r").readlines()) #carico il file delle stopword tedesche

nlp = spacy.load("en_core_web_sm") #carico i modelli inglesi di spacy
nlp2 = de_core_news_sm.load() #carico i modelli tedeschi di spacy


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
                t = [] #creo la lista in cui metto i synset che poi trasformerò in tupla
                lemmas = wn.lemmas(token)
                for lemma in lemmas: #per ogni lemma nella lista dei lemmi
                    t.append(lemma.synset()) #aggiungi il synset nella lista
                    print("ENG Lemma " + str(lemma) + " --> " + str(lemma.synset().hypernyms()))
                for synset in t: #per ogni synset nella lista
                    set_en.add(synset) #aggiungo il synset nel set dei synset di una singola frase
        synset_en.append(set_en) #aggiungo l'insieme dei synset in una lista
    return synset_en


#Il metodo createSet_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
def createSet_de(defile):
    sent_de = [] #inizializzo le due liste che conterranno le frasi del testo tedesco
    synset_de = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc = nlp2(defile.read())
    #Mi salvo ogni frase separatamente all'intero di una lista
    for s in doc.sents:
        sent_de.append(s)
    for sent in sent_de:#per ogni frase nel testo tedesco
        set_de = set() #creo un'insieme in cui si troveranno i synset
        for token in sent:
            token = str(token.lemma_).lower() #prendo il lemma lowercase di ogni parola
            if token not in stopwordsDE: #se il lemma della parola non è un stopword
                t = [] #creo la lista in cui metto i synset che poi trasformerò in tupla
                lemmas = wn.lemmas(token, lang="deu")
                for lemma in lemmas: #per ogni lemma nella lista dei lemmi
                    t.append(lemma.synset()) #aggiungi il synset nella lista
                    print("GER Lemma " + str(lemma) + " --> " + str(lemma.synset().hypernyms()))
                for synset in t: #per ogni synset nella lista
                    set_de.add(synset)  #aggiungo il synset nel set dei synset di una singola frase
        synset_de.append(set_de) #aggiungo l'insieme dei synset in una lista
    return synset_de


def sameSentence(enfile, defile):
    sentences = []
    list_set_en = createSet_en(enfile) #creo la lista degli insiemi dei synset di ciascuna frase inglese
    list_set_de = createSet_de(defile) #creo la lista degli insiemi dei synset di ciascuna frase tedesca
    for i in range(min(len(list_set_de), len(list_set_en))): #prendo le frasi attraverso gli indici della lista
        commonMeaning = list_set_en[i] & list_set_de[i] #ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        totalMeaning = list_set_en[i] | list_set_de[i] #ricavo l'unione della coppia di insiemi di synset (inglese e tedesco)
        print("FRASE " + str(i + 1) + ": " + "Significati comuni -> " + str(commonMeaning) + "  " + "Significati totali -> " + str(totalMeaning))
        if len(totalMeaning) != 0: #per evitare l'errore di divisione per zero
            sentences.append(len(commonMeaning) / len(totalMeaning)) #aggiungo la percentuale di somiglianza tra le frasi
        else:
            sentences.append(0)
    return sentences
