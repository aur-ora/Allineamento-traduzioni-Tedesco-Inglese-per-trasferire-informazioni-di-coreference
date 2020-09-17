import spacy
from spacy_babelnet import BabelnetAnnotator
from bs4 import BeautifulSoup
from pathlib import Path
import re

stopwordsEN = "".join(open("english-stop-words-large.txt", "r").readlines()) #carico il file delle stopword inglesi
stopwordsDE = "".join(open("german-stop-words.txt", "r").readlines()) #carico il file delle stopword tedesche

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(BabelnetAnnotator("en"))
nlp2 = spacy.load("de_core_news_lg")
nlp2.add_pipe(BabelnetAnnotator("de"))


#Il metodo createSet_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
#La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_en(enfile):
    sent_en = [] #inizializzo una lista che conterra' le frasi del testo inglese
    #sent_en_2 = [] #inizializzo la lista che conterra' le frasi di tipo stringa del testo inglese
    #sent_en_3 = [] #inizializzo la lista che conterra' le frasi di tipo span del testo inglese
    synset_en = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    doc = nlp(enfile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_en.append(s)

    sent_en_3 = sentence_splitter(sent_en) #richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for sent in sent_en_3: #per ogni frase nel testo inglese
        set_en = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsEN: #se non e' una stopword
                for synset in token._.babelnet.synsets(): #per ogni synset della parola
                    set_en.add(str(synset.getID())) #aggiungo l'ID del synset nell'insieme
        synset_en.append(set_en) #aggiungo l'insieme degli id dei synset della parola nella lista

    return sent_en_3, synset_en


#Il metodo createSet_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
#La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_de(defile):
    sent_de = [] #inizializzo una liste che conterra' le frasi del testo tedesco
    #sent_de_2 = [] #inizializzo la lista finale che conterra' le frasi del testo tedesco
    #sent_de_3 = [] #inizializzo la lista che conterra' le frasi di tipo span del testo tedesco
    synset_de = [] #inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc = nlp2(defile.read())
    for s in doc.sents: #Mi salvo ogni frase separatamente all'intero di una lista
        sent_de.append(s)

    sent_de_3 = sentence_splitter(sent_de) #richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for sent in sent_de_3: #per ogni frase nel testo tedesco
        set_de = set() #creo un'insieme in cui si troveranno i synset
        for token in sent: #per ogni parola nella frase
            if str(token) not in stopwordsDE: #se non e' una stopword
                for synset in token._.babelnet.synsets(): #per ogni synset della parola
                    set_de.add(str(synset.getID())) #aggiungo l'ID del synset nell'insieme
        synset_de.append(set_de) #aggiungo l'insieme degli id dei synset della parola nella lista

    return sent_de_3, synset_de


#Il metodo sameSentence ricava la percentuale di similarita' tra la frase inglese e tedesca dei testi dati in input
def same_sentence(enfile, defile):
    no_simil = []
    names = get_coreference(enfile.name)
    f = open((enfile.name)[:len(enfile.name) - 4] + ".pcr.txt", "r")
    percentuale = 0.21445344259078236
    sent_en, list_set_en = create_set_en(enfile) #creo la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de = create_set_de(defile) #creo la lista degli insiemi dei synset di ciascuna frase tedesca
    for i in range(min(len(list_set_de), len(list_set_en))): #prendo le frasi attraverso gli indici della lista
        dep_en = {}
        dep_de = {}
        common = list_set_en[i].intersection(list_set_de[i]) #ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimo = min(len(list_set_de[i]), len(list_set_en[i])) #prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi
        if minimo != 0:  # per evitare l'errore di divisione per zero
            if len(common) / minimo >= percentuale: #se la percentuale di somiglianza della frase e' maggiore o uguale a quella di riferimento
                doc = nlp(f.read())
                for token in doc:
                    if str(token.tag_) == "PRP" or str(token.tag_) == "PRP$" or str(token.pos_) == "PRON":
                        if token.nbor().text == "(":
                            token.i


        # if minimo != 0:  # per evitare l'errore di divisione per zero
        #     sentences.append(len(common) / minimo)  # aggiungo la percentuale di somiglianza tra le frasi
        # else: #se il denominatore e' 0
        #     sentences.append(0.0) #allora la percentuale e' 0


        # if minimo != 0: #per evitare l'errore di divisione per zero
        #     if len(common) / minimo >= percentuale: #se la percentuale di somiglianza della frase e' maggiore o uguale a quella di riferimento
        #         depen = tree2dict((to_nltk_tree(sent_en[i].root))) #ricavo il dizionario dall'albero del dependency parser inglese
        #         depde = tree2dict(to_nltk_tree(sent_de[i].root)) #ricavo il dizionario dall'albero del dependency parser tedesco
        #         print(depen)
        #         print(depde)
        #         for w in sent_en[i]: #per ogni parola nella frase inglese
        #             if w.dep_ in dep_en: #se il tag esiste già
        #                 dep_en[w.dep_].append(str(w)) #inserisci la parola con il tag come chiave
        #             else: #senno
        #                 dep_en[w.dep_] = [str(w)] #crea la chiave con quel tag e quella parola
        #         for w in sent_de[i]: #per ogni parola nella frase tedesca
        #             if w.dep_ in dep_de: #se il tag esiste già
        #                 dep_de[w.dep_].append(str(w)) #inserisci la parola con il tag come chiave
        #             else: #senno
        #                 dep_de[w.dep_] = [str(w)] #crea la chiave con quel tag e quella parola
        #     else: #se invece e' minore (quindi non e' la traduzione)
        #         no_simil.append((sent_en[i], sent_de[i])) #mi salvo in una lista la coppia di frasi
        # else:
        #     no_simil.append((sent_en[i], sent_de[i]))  # mi salvo in una lista la coppia di frasi
        # print(dep_en)
        # print(dep_de)
    return 0


#Il metodo getCoreference prende in input il nome (stringa) del file di interesse (testo inglese) e ricava il file .html
#che contiene le info sulle coreference del testo e lo salva in formato txt, e ritorna la lista di liste dei nomi ricavati applicando la coreference
def get_coreference(nameEnfile):
    nameEnfile = nameEnfile[:len(nameEnfile) - 4] #prendo solo il nome del file senza l'estensione txt
    data_folder = Path("../book-nlp-master/data/output/" + nameEnfile[:nameEnfile.index(".")] + "/" + nameEnfile + ".html") #mi salvo la directory dei file .html ricavati usando un comando di book nlp
    soup = BeautifulSoup(open(data_folder, "r"), features="html.parser") #uso beautiful soup per convertire da html a txt
    filePcr = nameEnfile + ".pcr.txt" #mi salvo il nome del nuovo file in una variabile
    file = open(filePcr, "w") #apro il nuovo file in scrittura
    file.write(soup.get_text()) #salvo il testo convertito nel file
    f = open(filePcr, "r") #riapro il lettura il file appena salvato
    lines = f.readlines() #creo una lista di stringhe che contiene le frasi del testo
    names = lines[0].replace("\t", "").replace("Characters", "").replace("\n", "") #ricavo i nomi dei personaggi trovati con la coreference, elimino le parentesi, il tab, l'accapo e la stringa "Characters" (introdotta con la coref)
    names = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", names).replace("()", "_") #elimino le parentesi con il contenuto e lo sostiuisco con _ per poi riconoscere gli alias
    names = list(set(re.sub("\d", ",", names).split(","))) #la faccio diventare una lista, ma prima elimino i numeri e i duplicati
    for i in range(len(names)): #elimino gli eventuali spazi
        if names[i].startswith(" "): #all'inizio del nome
            names[i] = names[i][1:] #sostituisco il nome con il nome senza spazi davanti
        if names[i].endswith(" _ "): #alla fine del nome
            names[i] = names[i][: len(names[i]) - 3] #sostituisco il nome con il nome senza spazi alla fine
        if "Text" in names[i]: #sostituisco direttamente la stringa che contiene "Text"
            names[i] = "" #con la stringa vuota (diversamente da "Characters", che potrebbe contenere un nome)
    for name in names: #per ogni nome
        if name == "": #se ho una stringa vuota
            names.remove(name) #la rimuovo
    for i in range(len(names)): #per ogni elementi nella lista dei nomi
        if "_" not in names[i]: #se non ci sono alias
            names[i] = [names[i]] #creo una lista con il nome
        else: #se ci sono gli alias
            names[i] = names[i].split(" _ ") #separiamoli
    lines[0] = lines[0][lines[0].index("Text") + 4:] #elimino la prima riga tranne la parte dopo "Text" (è stata creata dopo e non fa parte del testo iniziale)
    f1 = open(filePcr, "w") #apro lo stesso file in scrittura
    f1.write("".join(lines)) #risalvo il contenuto meno la prima riga nel file che contiene la coreference
    return names #ritorno la lista dei nomi individuati con la coreference


#Il metodo sentence_splitter prende in input una lista di frasi e sistema le frasi che sono state spezzate male (prima o dopo del dovuto)
def sentence_splitter(sent):
    sent_2 = [] #inizializzo la lista che conterra' le frasi come stringhe
    sent_3 = [] #inizializzo la lista che conterra' le frasi come oggetti span

    for sentence, i in zip(sent, range(len(sent))): #per ogni frase in sent
        if not re.match("^[a-zA-Z\S\s\d\n*]+[.?!](\"|\«)?\s*$", str(sentence)): #se la frase non finisce con ".", "?" o "!"
            if len(sent_2) != 0: #se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]): #e la frase non e' stata ancora aggiunta
                    s = str(sentence) + str(sent[i + 1]) #unisci la frase attuale con quella successiva
                    sent_2.append(s) #aggiungi le frasi unite nella lista
            else: #se la lista e' vuota
                s = str(sentence) + str(sent[i + 1]) #unisci la frase attuale con la successiva
                sent_2.append(s) #aggiungi le frasi unite nella lista

        else: #se invece finisce con ".", "?" o "!"
            if len(sent_2) != 0: #se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]): #e la frase non e' stata ancora aggiunta
                    if not re.match("^[a-zA-Z\S\s\d\n*]+[.?!](\"|\«)?\s*$", str(sent_2[len(sent_2) - 1])): #se l'ultima frase aggiunta alla lista non finisce con ".", "?" o "!"
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence) #unisci a quell'ultima frase la frase attuale
                    else: #se l'ultima frase finisce con ".", "?" o "!"
                        sent_2.append(str(sentence)) #aggiungi la frase attuale alla lista
            else: #se la lista e' vuota
                sent_2.append(str(sentence)) #aggiungi la frase alla lista

    for frase in sent_2: #per ogni frase nella nuova lista
        sent_3.append(nlp(frase)) #la faccio diventare span

    return sent_3 #restituisco la lista delle frasi


