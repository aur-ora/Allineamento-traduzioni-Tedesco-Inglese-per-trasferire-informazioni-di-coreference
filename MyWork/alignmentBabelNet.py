import spacy
from spacy_babelnet import BabelnetAnnotator
from bs4 import BeautifulSoup
from pathlib import Path
import re

stopwordsEN = "".join(open("english-stop-words-large.txt", "r").readlines())  # carico il file delle stopword inglesi
stopwordsDE = "".join(open("german-stop-words.txt", "r").readlines())  # carico il file delle stopword tedesche

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(BabelnetAnnotator("en"))
nlp2 = spacy.load("de_core_news_lg")
nlp2.add_pipe(BabelnetAnnotator("de"))


# Il metodo create_set_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
# La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_en(enfile):
    sent_en = []  # inizializzo una lista che conterra' le frasi del testo inglese
    sent_en_3 = []  # inizializzo la lista che conterra' le frasi come oggetti span
    synset_en = []  # inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    doc = nlp(enfile.read())
    for s in doc.sents:  # Mi salvo ogni frase separatamente all'intero di una lista
        sent_en.append(s)

    # for i in sent_en:
    #     print(str(sent_en.index(i) + 1) + ". " + str(i))

    sent_en_2 = sentence_splitter(
        sent_en)  # richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for frase in sent_en_2:  # per ogni frase nella nuova lista
        sent_en_3.append(nlp(frase))  # la faccio diventare span

    for sent in sent_en_3:  # per ogni frase nel testo inglese
        set_en = set()  # creo un'insieme in cui si troveranno i synset
        for token in sent:  # per ogni parola nella frase
            if str(token) not in stopwordsEN:  # se non e' una stopword
                synsets = token._.babelnet.synsets()
                for synset in synsets:  # per ogni synset della parola
                    set_en.add(str(synset.getID()))  # aggiungo l'ID del synset nell'insieme
        synset_en.append(set_en)  # aggiungo l'insieme degli id dei synset della parola nella lista

    return sent_en_3, synset_en


# Il metodo create_set_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
# La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_de(defile):
    sent_de = []  # inizializzo una liste che conterra' le frasi del testo tedesco
    sent_de_3 = []  # inizializzo la lista che conterra' le frasi come oggetti span
    synset_de = []  # inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    doc = nlp2(defile.read())
    for s in doc.sents:  # Mi salvo ogni frase separatamente all'intero di una lista
        sent_de.append(s)

    sent_de_2 = sentence_splitter(
        sent_de)  # richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for frase in sent_de_2:  # per ogni frase nella nuova lista
        sent_de_3.append(nlp2(frase))  # la faccio diventare span

    for sent in sent_de_3:  # per ogni frase nel testo tedesco
        set_de = set()  # creo un'insieme in cui si troveranno i synset
        for token in sent:  # per ogni parola nella frase
            if str(token) not in stopwordsDE:  # se non e' una stopword
                synsets = token._.babelnet.synsets()
                for synset in synsets:  # per ogni synset della parola
                    set_de.add(str(synset.getID()))  # aggiungo l'ID del synset nell'insieme
        synset_de.append(set_de)  # aggiungo l'insieme degli id dei synset della parola nella lista

    return sent_de_3, synset_de


# Il metodo same_sentence ricava la percentuale di similarita' tra la frase inglese e tedesca dei testi dati in input
def same_sentence(enfile, defile):
    #sentences = []
    sent = []
    sent_core = []
    # names = get_coreference(enfile.name)  # richiamo il metodo che mi crea il file con le coreference e che mi restituisce la lista dei nomi dei personaggi
    # names = [['Campagna'], ['Leontodon'], ['Prince'], ['Braquemart'], ['Koppels-Bleek'], ['Belovar'], ['Lampusa', 'LAMPUSA'], ['Pulverkopf'], ['Biedenhorn'], ['Chiffon Rouge'], ['Nigromontanus'], ['Otho', 'Brother Otho'], ['Linnreus'], ['La Picousiere'], ['Ehrhardt'], ['Silvia'], ['Ansgar'], ['Erio'], ['Vesta'], ['Deodat'], ['Lampros'], ['Fortunio']]
    names = [['Samana'], ['Vasudeva'], ['Sansara'], ['Siddhartha'], ['Atman'], ['Buddha'], ['Brahman'], ['Kamaswami'],
             ['Govinda'], ['Gotama'], ['Kamala'], ['Samanas']]
    f = open(enfile.name[:len(enfile.name) - 4] + ".pcr.txt", "r")  # apro il file appena creato
    doc = nlp(f.read())
    for s in doc.sents:  # divido il testo in frasi
        sent.append(s)  # e le salvo in una lista

    sent_ = sentence_splitter_coref(sent)  # richiamo il metodo che mi ridivide in modo corretto le frasi

    for frase in sent_:  # per ogni frase nella nuova lista
        sent_core.append(nlp(frase))  # la faccio diventare span

    percentuale = 0.21445344259078236  # la percentuale di riferimento calcolata precedentemente
    perc = 0.28898147455983053  # la percentuale di riferimento calcolata precedentemente -> dopo aver ricalcolato le percentuali
    sent_en, list_set_en = create_set_en(enfile)  # creo la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de = create_set_de(defile)  # creo la lista degli insiemi dei synset di ciascuna frase tedesca

    # print("sent_core")
    # for i in range(len(sent_core)):
    #     print(str(i + 1) + ")" + str(sent_core[i]))
    #
    # print("sent_en")
    # for i in range(len(sent_en)):
    #     print(str(i + 1) + ")" + str(sent_en[i]))
    #
    # print("sent_de")
    # for i in range(len(sent_de)):
    #     print(str(i + 1) + ")" + str(sent_de[i]))

    for i in range(min(len(list_set_de), len(list_set_en))):  # prendo le frasi attraverso gli indici della lista
        common = list_set_en[i].intersection(list_set_de[i])  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimo = min(len(list_set_de[i]), len(list_set_en[i]))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

        if minimo != 0:  # per evitare l'errore di divisione per zero
            if len(common) / minimo >= perc:  # se la percentuale di somiglianza della frase e' maggiore o uguale a quella di riferimento
                for token in sent_core[i]:
                    if (str(token.tag_) == "PRP" or str(token.tag_) == "PRP$" or str(token.pos_) == "PRON") and token.nbor().text == "(":
                        # print("ECCOLO " + token.text)
                        parola = str(sent_core[i])[str(sent_core[i]).index(token.nbor().text) + 1: str(sent_core[i]).index(")")]
                        for token_de in sent_de[i]:
                            if (str(token_de.tag_) == "PPER" or str(token_de.tag_) == "PPOSAT" or str(token_de.tag_) == "PPOSS" or str(token_de.tag_) == "PRF") and (str(token_de.pos_) == "PRON" or str(token_de.pos_) == "DET"):
                                print("GERMAN PRONOUN")
                                print(token_de, token_de.tag_)
                        for lista in names:
                            if parola in lista:
                                print("Dovremmo ricavare prima il pronome corrispondente e se coincide, metto il nome tra parentesi accanto")
                            else:
                                print("Dovremmo ricavare prima il pronome corrispondente e poi cercare il synset della parola e trovare quello tedesco corrispondente")
                        # print(re.match("^\([a-zA-Z\s]+\)$", sent_core[i]))

            # else:  # se la percentuale di somiglianza della frase e' minore di quella di riferimento
            #     print("Unire e spezzare le frasi")
        else:
            print("Non sono la traduzione")
    return 1


# Il metodo get_coreference prende in input il nome (stringa) del file di interesse (testo inglese) e ricava il file .html
# che contiene le info sulle coreference del testo e lo salva in formato txt, e ritorna la lista di liste dei nomi ricavati applicando la coreference
def get_coreference(name_enfile):
    name_enfile = name_enfile[:len(name_enfile) - 4]  # prendo solo il nome del file senza l'estensione txt
    data_folder = Path("../book-nlp-master/data/output/" + name_enfile[:name_enfile.index(".")] + "/" + name_enfile + ".html")  # mi salvo la directory dei file .html ricavati usando un comando di book nlp
    soup = BeautifulSoup(open(data_folder, "r"), features="html.parser")  # uso beautiful soup per convertire da html a txt
    file_pcr = name_enfile + ".pcr.txt"  # mi salvo il nome del nuovo file in una variabile
    file = open(file_pcr, "w")  # apro il nuovo file in scrittura
    file.write(soup.get_text())  # salvo il testo convertito nel file
    f = open(file_pcr, "r")  # riapro il lettura il file appena salvato
    lines = f.readlines()  # creo una lista di stringhe che contiene le frasi del testo
    names = lines[0].replace("\t", "").replace("Characters", "").replace("\n", "")  # ricavo i nomi dei personaggi trovati con la coreference, elimino le parentesi, il tab, l'accapo e la stringa "Characters" (introdotta con la coref)
    names = re.sub("([\(\[]).*?([\)\]])", "\g<1>\g<2>", names).replace("()", "_")  # elimino le parentesi con il contenuto e lo sostiuisco con _ per poi riconoscere gli alias
    names = list(set(re.sub("\d", ",", names).split(",")))  # la faccio diventare una lista, ma prima elimino i numeri e i duplicati
    for i in range(len(names)):  # elimino gli eventuali spazi
        if names[i].startswith(" "):  # all'inizio del nome
            names[i] = names[i][1:]  # sostituisco il nome con il nome senza spazi davanti
        if names[i].endswith(" _ "):  # alla fine del nome
            names[i] = names[i][: len(names[i]) - 3]  # sostituisco il nome con il nome senza spazi alla fine
        if "Text" in names[i]:  # sostituisco direttamente la stringa che contiene "Text"
            names[i] = ""  # con la stringa vuota (diversamente da "Characters", che potrebbe contenere un nome)
    for name in names:  # per ogni nome
        if name == "":  # se ho una stringa vuota
            names.remove(name)  # la rimuovo
    for i in range(len(names)):  # per ogni elementi nella lista dei nomi
        if "_" not in names[i]:  # se non ci sono alias
            names[i] = [names[i]]  # creo una lista con il nome
        else:  # se ci sono gli alias
            names[i] = names[i].split(" _ ")  # separiamoli
    lines[0] = lines[0][lines[0].index("Text") + 4:]  # elimino la prima riga tranne la parte dopo "Text" (è stata creata dopo e non fa parte del testo iniziale)
    f1 = open(file_pcr, "w")  # apro lo stesso file in scrittura
    f1.write("".join(lines))  # risalvo il contenuto meno la prima riga nel file che contiene la coreference
    return names  # ritorno la lista dei nomi individuati con la coreference


# "\"(.*?)\"|\'(.*?)\'|\»(.*?)\«|\`(.*?)\`" per il discorso diretto

# "^[a-zA-Z\S\s\d ]+[.?!…](\"|\«|\'*)?\s*$" per la frase

# (?<=^|(\.|!|\?) |\n|\t|\r|\r\n) *\(?[A-Z][^.!?]*((\.|!|\?)(?! |\n|\r|\r\n)[^.!?]*)*(\.|!|\?)(?= |\n|\r|\r\n)

# ^(\((.*?)\)|\s|\`|\"|\'|\«)*[A-Z][a-zA-Z\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$) coref

# Abbiamo 4 casi di frase:
# 1) "Hello," --> inizio di una frase, ma non la fine --> ^[A-Z][a-zA-Z\s\S\d ]*[A-Za-z0-9,:;\])}\-_\"\' ]$
# 2) "hello" --> in mezzo alla frase --> ^[a-z][a-zA-Z\s\S\d ]*[A-Za-z0-9,:;\])}\-_\"\' ]$
# 3) "Hello!" --> frase completa regex --> ^(\s|\`|\"|\'|\»)*[A-Z][a-zA-Z\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)
# 4) "hello." --> fine di una frase --> ^[a-z][a-zA-Z\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)

# Il metodo sentence_splitter prende in input una lista di frasi e sistema le frasi che sono state spezzate male (prima o dopo del dovuto)
def sentence_splitter(sent):
    sent_2 = []  # inizializzo la lista che conterra' le frasi come stringhe
    for sentence, i in zip(sent, range(len(sent))):  # per ogni frase in sent e per ogni indice
        sentence = str(sentence).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
        if re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\« ]$", str(sentence)):  # se la frase inizia con la maiuscola non finisce con ".", "?", "!" o "…" - caso 1
            if len(sent_2) != 0:  # se la lista non è vuota
                if re.match("^(\s|\`|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]) \
                        or re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]):  # se quella prima finisce con ., ?, ! etc.
                    sent_2.append(str(sentence))  # aggiungo solo la frase attuale
                else:  # se la frase prima non finisce con ., ?, ! etc.
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista è vuota
                sent_2.append(str(sentence))  # aggiungo direttamente la frase

        elif re.match("^(\s|\`|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", str(sentence)):  # caso 3 -> frase completa
            sent_2.append(str(sentence))  # aggiungo direttamente la frase

        elif re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\« ]$", str(sentence)) \
                or re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", str(sentence)):  # se è in mezzo o la fine di una frase - caso 2 e 3
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # e la frase non e' stata ancora aggiunta
                    # if re.match("^(\s|\`|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]) \
                    #         or re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]):  # se quella prima finisce con il punto
                    #     sent_2.append(str(sentence))  # aggiungi la frase attuale alla lista
                    # else:
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence)  # aggiungo la frase attuale a quella precedente

            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase alla lista

    return sent_2  # restituisco la lista delle frasi


# Il metodo sentence_splitter_coref è uguale al metodo sentence_splitter tranne che viene applicato al file che contiene le coreference
# che ha parole tra parentesi nel testo, quindi viene trattato in modo differente, per spezzare allo stesso modo di sentence_splitter e fare in modo
# che le due liste siano divise allo stesso modo (lista delle frasi inglesi e lista delle frasi inglesi con coreference)
def sentence_splitter_coref(sent):
    sent_2 = []  # inizializzo la lista che conterra' le frasi come stringhe
    for sentence, i in zip(sent, range(len(sent))):  # per ogni frase in sent e per ogni indice
        sentence = str(sentence).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
        if re.match("^(\s|\;|\((.*?)\)|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\« ]$", str(sentence)):  # se la frase inizia con la maiuscola non finisce con ".", "?", "!" o "…" - caso 1
            if len(sent_2) != 0:  # se la lista non è vuota
                if re.match("^(\s|\`|\((.*?)\)|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]) \
                        or re.match("^(\s|\;|\:|\((.*?)\)|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]):  # se quella prima finisce con ., ?, ! etc.
                    sent_2.append(str(sentence))  # aggiungo solo la frase attuale
                else:  # se la frase prima non finisce con ., ?, ! etc.
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista è vuota
                sent_2.append(str(sentence))  # aggiungo direttamente la frase

        elif re.match("^(\s|\`|\((.*?)\)|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", str(sentence)):  # caso 3 -> frase completa
            sent_2.append(str(sentence))  #  aggiungo direttamente la frase

        elif re.match("^(\s|\;|\:|\((.*?)\)|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\`\«\"\' ]$", str(sentence)) \
                or re.match("^(\s|\;|\((.*?)\)|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", str(sentence)):  # se è in mezzo o la fine di una frase - caso 2 e 3
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # e la frase non e' stata ancora aggiunta
                    # if re.match("^(\s|\`|\"|\'|\»)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]) \
                    #         or re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\`|\"|\'|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\'*)?\s*$)", sent_2[len(sent_2) - 1]):  # se quella prima finisce con il punto
                    #     sent_2.append(str(sentence))  # aggiungi la frase attuale alla lista
                    # else:
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase alla lista

    return sent_2  # restituisco la lista delle frasi


# Calcolare la percentuale
# if minimo != 0:  # per evitare l'errore di divisione per zero
#     sentences.append(len(common) / minimo)  # aggiungo la percentuale di somiglianza tra le frasi
# else:  # se il denominatore e' 0
#     sentences.append(0.0)  # allora la percentuale e' 0