import spacy
from spacy_babelnet import BabelnetAnnotator

stopwordsEN = "".join(open("english-stop-words-large.txt", "r").readlines()) #carico il file delle stopword inglesi
stopwordsDE = "".join(open("german-stop-words.txt", "r").readlines()) #carico il file delle stopword tedesche

nlp = spacy.load("en")
nlp.add_pipe(BabelnetAnnotator("en"))
nlp2 = spacy.load("de")
nlp2.add_pipe(BabelnetAnnotator("de"))


#Il metodo createSet_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
def createSet_en(enfile):
    sent_en = [] #inizializzo le due liste che conterranno le frasi del testo inglese
    synset_en = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    doc = nlp(enfile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_en.append(s)
    for sent in sent_en: #per ogni frase nel testo inglese
        set_en = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsEN: #se non è una stopword
                for synset in token._.babelnet.synsets(): #per ogni synset della parola
                    set_en.add(str(synset.getID())) #aggiungo l'ID nell'insieme
        synset_en.append(set_en) #aggiungo l'insieme degli id dei synset della parola nella lista
    return synset_en


#Il metodo createSet_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
def createSet_de(defile):
    sent_de = [] #inizializzo le due liste che conterranno le frasi del testo tedesco
    synset_de = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc = nlp2(defile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_de.append(s)
    for sent in sent_de: #per ogni frase nel testo tedesco
        set_de = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsDE: #se non è una stopword
                for synset in token._.babelnet.synsets(): #per ogni synset della parola
                    set_de.add(str(synset.getID())) #aggiungo l'ID nell'insieme
        synset_de.append(set_de) #aggiungo l'insieme degli id dei synset della parola nella lista
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


def sameSentenceEN(enfile, defile):
    sentences = []
    list_set_en = createSet_de(enfile) #creo la lista degli insiemi dei synset di ciascuna frase inglese
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

def main():
    englishTXT = open("sentences.txt", "r")
    germanTXT = open("sätze.txt", "r")
    en = open("one.txt", "r")
    en1 = open("one.txt", "r")
    de = open("ein.txt", "r")
    de1 = open("ein.txt", "r")
    print(sameSentence(englishTXT, germanTXT))
    #print(createSet_en(englishTXT))
    #print(createSet_de(germanTXT))
if __name__ == "__main__":
      main()
