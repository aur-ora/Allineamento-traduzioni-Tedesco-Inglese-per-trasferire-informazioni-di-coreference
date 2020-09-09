import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

stopwordsEN = "".join(open("english-stop-words-large.txt", "r").readlines()) #carico il file delle stopword inglesi
stopwordsDE = "".join(open("german-stop-words.txt", "r").readlines()) #carico il file delle stopword tedesche

nlp = spacy.load("en_core_web_lg") #carico i modelli inglesi di spacy
nlp.add_pipe(WordnetAnnotator(nlp.lang))
nlp2 = spacy.load("de_core_news_lg") #carico i modelli tedeschi di spacy
nlp2.add_pipe(WordnetAnnotator(nlp2.lang))


#Il metodo createSet_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
#La prima frase avrà l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def createSet_en(enfile):
    sent_en = [] #inizializzo le due liste che conterranno le frasi del testo inglese
    synset_en = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    doc = nlp(enfile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_en.append(s)
    for sent in sent_en: #per ogni frase nel testo inglese
        set_en = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsEN: #se la parola non è un stopword
                synsets = token._.wordnet.synsets() #prendo l'insieme dei synset
                for synset in synsets: #per ogni synset nella lista
                    set_en.add(synset) #aggiungo il synset nel set dei synset di una singola frase
        synset_en.append(set_en) #aggiungo l'insieme dei synset in una lista
    return sent_en, synset_en


#Il metodo createSet_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
#La prima frase avrà l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def createSet_de(defile):
    sent_de = [] #inizializzo le due liste che conterranno le frasi del testo tedesco
    synset_de = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc = nlp2(defile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_de.append(s)
    for sent in sent_de:#per ogni frase nel testo tedesco
        set_de = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsDE: #se la parola non è un stopword
                synsets = token._.wordnet.synsets() #prendo l'insieme dei synset
                for synset in synsets: #per ogni synset nella lista
                    set_de.add(synset)  #aggiungo il synset nel set dei synset di una singola frase
        synset_de.append(set_de) #aggiungo l'insieme dei synset in una lista
    return sent_de, synset_de


#Il metodo sameSentence ricava la percentuale di similarità tra la frase inglese e tedesca dei testi dati in input
def sameSentence(enfile, defile):
    sentences = []
    percentuale = 0.25214495649278257
    sent_en, list_set_en = createSet_en(enfile) #creo la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de = createSet_de(defile) #creo la lista degli insiemi dei synset di ciascuna frase tedesca
    print(sent_en[0])
    print(list_set_en[0])
    for i in range(min(len(list_set_de), len(list_set_en))): #prendo le frasi attraverso gli indici della lista
        common = list_set_en[i].intersection(list_set_de[i]) #ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimo = min(len(list_set_de[i]), len(list_set_en[i])) #prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi
        if minimo != 0:  # per evitare l'errore di divisione per zero
            sentences.append(len(common) / minimo)  # aggiungo la percentuale di somiglianza tra le frasi
        else: #se il denominatore è 0
            sentences.append(0.0) #allora la percentuale è 0
    return sentences

