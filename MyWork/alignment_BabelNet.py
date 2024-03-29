import spacy
import json
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

with open("dict_synset_en.json", "r") as d:
    dict_synset_en = json.load(d)

with open("dict_synset_de.json", "r") as d:
    dict_synset_de = json.load(d)


# Il metodo create_set_en crea una lista di insiemi che contengono i synset di ciascuna frase del testo inglese
# La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_en(enfile):
    sent_en = []  # inizializzo una lista che conterra' le frasi del testo inglese
    sent_en_3 = []  # inizializzo la lista che conterra' le frasi come oggetti span
    synset_en = []  # inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo inglese
    tok_syn_en = []  # inizializzo la lista che conterra' i dizionario dei sostantivi con i synset
    count_words = []  # lista di conteggio delle parola con synset per ciascuna frase
    doc = nlp(enfile.read())
    for s in doc.sents:  # Mi salvo ogni frase separatamente all'intero di una lista
        sent_en.append(s)

    sent_en_2 = sentence_splitter(sent_en)  # richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for frase in sent_en_2:  # per ogni frase nella nuova lista
        sent_en_3.append(nlp(frase))  # la faccio diventare span

    for sent in sent_en_3:  # per ogni frase nel testo inglese
        words = 0
        d = {}  # inizializzo il dizionario che avra' come chiave un sostantivo e come valore la lista dei suoi synset
        set_en = set()  # creo un'insieme in cui si troveranno i synset
        for token in sent:  # per ogni parola nella frase
            # print(token.text, token.dep_)
            if str(token).lower() not in stopwordsEN and str(token) != " ":  # se non e' una stopword
                if str(token).lower() not in dict_synset_en:
                    list_syn = []
                    synsets = token._.babelnet.synsets()

                    for synset in synsets:  # per ogni synset della parola
                        list_syn.append(str(synset.getID()))
                        # set_en.add(str(synset.getID()))  # aggiungo l'ID del synset nell'insieme

                    dict_synset_en[str(token).lower()] = list_syn
                else:
                    list_syn = dict_synset_en[str(token).lower()]

                if list_syn:  # se la lista dei synset non e' vuota
                    # print(token.text)
                    words += 1  # conta la parola

                if str(token.pos_) == "NOUN":  # se il token e' un sostantivo
                    d[str(token)] = list_syn  # aggiungilo al dizionario insieme alla lista dei synset

                set_en = set_en.union(set(list_syn))
                # for synset in synsets:  # per ogni synset della parola
                #     set_en.add(str(synset.getID()))  # aggiungo l'ID del synset nell'insieme
        synset_en.append(set_en)  # aggiungo l'insieme degli id dei synset della parola nella lista
        tok_syn_en.append(d)  # aggiungi il dizionario alla lista
        count_words.append(words)  # aggiungi il conteggio delle parole nella lista

        with open("dict_synset_en.json", "w") as dictionary:
            json.dump(dict_synset_en, dictionary)

    return sent_en_3, synset_en, tok_syn_en, count_words


# Il metodo create_set_de crea una lista di insiemi che contengono i synset di ciascuna frase del testo tedesco
# La prima frase avra' l'insieme dei synset delle sue parole all'indice 0 nella lista, la seconda all'indice 1 etc.
def create_set_de(defile):
    sent_de = []  # inizializzo una liste che conterra' le frasi del testo tedesco
    sent_de_3 = []  # inizializzo la lista che conterra' le frasi come oggetti span
    synset_de = []  # inizializzo le due liste che conterranno gli insieme dei synset di ogni frase del testo tedesco
    tok_syn_de = []  # inizializzo la lista che conterra' i dizionario dei sostantivi con i synset
    count_words = []  # lista di conteggio di parole con synset per ciascuna frase
    doc = nlp2(defile.read())
    for s in doc.sents:  # Mi salvo ogni frase separatamente all'intero di una lista
        sent_de.append(s)

    sent_de_2 = sentence_splitter(sent_de)  # richiamo il metodo che prende la lista delle frasi e ne restituisce un'altra spezzata correttamente

    for frase in sent_de_2:  # per ogni frase nella nuova lista
        sent_de_3.append(nlp2(frase))  # la faccio diventare span

    for sent in sent_de_3:  # per ogni frase nel testo tedesco
        d = {}  # inizializzo il dizionario che avra' come chiave un sostantivo e come valore la lista dei suoi synset
        set_de = set()  # creo un'insieme in cui si troveranno i synset
        words = 0
        for token in sent:  # per ogni parola nella frase
            # print(token.text, token.pos_)
            if str(token).lower() not in stopwordsDE and str(token) != " ":  # se non e' una stopword
                if str(token).lower() not in dict_synset_de:
                    list_syn = []
                    synsets = token._.babelnet.synsets()

                    for synset in synsets:  # per ogni synset della parola
                        list_syn.append(str(synset.getID()))
                        # set_de.add(str(synset.getID()))  # aggiungo l'ID del synset nell'insieme

                    dict_synset_de[str(token).lower()] = list_syn
                else:
                    list_syn = dict_synset_de[str(token).lower()]

                if list_syn:  # se la lista dei synset non e' vuota
                    words += 1  # conta la parola

                if str(token.pos_) == "NOUN":  # se il token e' un sostantivo
                    d[str(token)] = list_syn  # aggiungilo al dizionario insieme alla lista dei synset

                set_de = set_de.union(set(list_syn))
        synset_de.append(set_de)  # aggiungo l'insieme degli id dei synset della parola nella lista
        tok_syn_de.append(d)  # aggiungi il dizionario alla lista
        count_words.append(words)  # aggiungi il conteggio alla lista

        with open("dict_synset_de.json", "w") as dictionary:
            json.dump(dict_synset_de, dictionary)

    return sent_de_3, synset_de, tok_syn_de, count_words


# Il metodo coref_da_intero prende in input la porzione di testo di cui si vuole prendere la coreference
# quindi genera in output un file identico a enfile_parte ma con le coreference, prendendo il testo completo con lo stesso nome
# il testo completo e' quello che esce dopo aver runnato save_sent_coref(enfile), in cui enfile e' il file con coreference non spezzato bene
def prendi_coref_da_testo(enfile):
    enfile_intero = open(enfile.name[:len(enfile.name) - 8] + "en.sent.coref.txt", "r").readlines()  # prendo il testo completo che corrisponde al testo in input
    with open("sent_en_" + enfile.name[:len(enfile.name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)
    enf = diz_en["sent"]
    regex = re.compile(r'[\n\r\t]')
    r = re.compile(r" {2,}")

    frasi_coref = []  # lista che conterra' solo le frasi con coreference che ci interessano

    i = 0  # indice per testo parziale
    j = 0  # indice per testo completo
    while i < len(enf) and j < len(enfile_intero):  # finche' non finisce la lista di frasi del testo corto o del testo completo
        if re.sub(r, " ", re.sub(r"\([a-zA-Z ]+\)", "", enfile_intero[j])).replace("’", "'").replace("   ", " ").replace("- ", "-").replace(" - ", "-") \
                .replace(" -", "-").replace(" — ", "—").replace("— ", "—").replace(" —", "—").replace("--", "—").replace(" ;", ";").replace(" :", ":") \
                .replace("``", "\"").replace("''", "\"").replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!").replace("  ", " ").strip() \
                == re.sub(r, " ", re.sub(r"\([a-zA-Z ]+\)", "", enf[i])).replace("   ", " ").replace("- ", "-").replace(" - ", "-").replace(" -", "-") \
                .replace(" — ", "—").replace("— ", "—").replace(" —", "—").replace("--", "—").replace("’", "'").replace(" ;", ";").replace(" :", ":") \
                .replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!").replace("  ", " ").strip():  # se le due frasi senza corefernce (e altri aspetti) sono uguali
            frasi_coref.append(enfile_intero[j])  # aggiungi la frase nella lista
            i += 1  # vai avanti con l'indice nella parte di testo
            j += 1  # vai avanti con l'indice nel testo completo
        else:  # se sono diversi
            j += 1  # vai avanti con l'indice nel testo completo

    f = open(enfile.name[:len(enfile.name) - 4] + ".sent.coref.txt", "w")
    for i in frasi_coref:
        f.write(i)
    f.close()
    return 1


# Il metodo same_sentence ricava la percentuale di similarita' tra la frase inglese e tedesca dei testi dati in input, e se la similarita' e' maggiore della percentuale
# allora, se l'originale e' tedesco, ricaviamo le info sulla coreference dal testo tradotto in inglese e le trasferiamo al testo tedesco
# se l'originale e' inglese, ricaviamo le info sul numero e genere delle parole tedesche,
# se la similarita' e' minore, controlliamo se unendo k frasi prima e/o dopo la frase la similitarita' e' maggiore


# il metodo save_sent_coref salva le frasi spezzate correttamente del testo con coreference in un file
def save_sent_coref(enfile):
    sent = []  # inizializzo lista che conterra' le frasi del testo inglese con le coreference
    f = open(enfile.name[:len(enfile.name) - 4] + ".pcr.txt", "r")  # apro il file appena creato
    doc = nlp(f.read())
    for s in doc.sents:  # divido il testo in frasi
        sent.append(s)  # e le salvo in una lista

    sent_ = sentence_splitter_coref(sent)  # richiamo il metodo che mi ridivide in modo corretto le frasi

    file = open(enfile.name[:len(enfile.name) - 4] + ".sent.coref.txt", "w")

    for frase in sent_:
        file.write(str(frase) + "\n")
    file.close()

    return 1


# il metodo my_coreference per ora calcola solo le coreference a partire dai testi inglese e tedesco in cui vengono prese solo in considerazione
# le frasi che sono state individuate dall'allineamento come veri positivi
def my_coreference(enfile, defile, analysis):
    # sent = []  # inizializzo lista che conterra' le frasi del testo inglese con le coreference
    sent_core = []  # inizializzo lista che conterra' le frasi del testo inglese con le coreference dopo aver sistemato le frasi
    sent_de = []

    with open("pronouns.json") as f:
        pron = json.load(f)  # apro il file che contiene il dizionario con le info sui pronomi dal inglese al tedesco

    with open("pronouns_all.json") as f:
        pron_all = json.load(f)

    names = open("names_pcr." + enfile.name[:len(enfile.name) - 8] + "en.txt", "r").readlines()
    for name in names:
        names[names.index(name)] = name.replace("\n", "")

    sent_ = open(enfile.name[:len(enfile.name) - 4] + ".sent.coref.txt", "r").readlines()

    enfile_name = enfile.name
    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    sent_de_ = diz_de["sent"]

    corr_right = open("align.perf." + enfile_name[:len(enfile_name) - 7] + ".txt", "r").readlines()  # carico il file che ha l'allineamento perfetto
    corr_right = "".join(corr_right).replace("\n", "").split(", ")
    '''
    ADATTA AI 2 CASI MIGLIORI
    '''
    # analysis = open("list_analysis." + enfile_name[:len(enfile_name) - 7] + ".txt", "r").readlines()  # stringa di vp, vn, fp, fn del testo in input uscito dall'algoritmo di allineamento
    analysis_ = analysis.readlines()
    analysis_ = "".join(analysis_).split("||")

    ind_ted = []  # inizializzo la lista che conterra' gli indici tedeschi
    ind_ing_coref = []  # inizializzo la lista che conterra' gli indici inglesi
    for coppia in corr_right:  # per ogni coppia di indici ted->ing
        ind_ted.append(coppia.split(":")[0])  # aggiungo la lista di indici alla lista tedesca
        ind_ing_coref.append(coppia.split(":")[1])  # aggiungo la lista di indici alla lista inglese

    frasi_ted = []  # la lista che conterra' la lista di frasi tedesche
    for indici in ind_ted:  # per gli indici in ind_ted
        indici = [indici[1:len(indici) - 1]]  # la trasformo in lista
        s = ""  # lista che conterra' le singole frasi
        for ind in indici:  # per ogni indice nella lista di indici
            j = ind.split(",")  # separo gli indici (se più di uno)
            for i in j:  # per ogni indice negli indici
                s += sent_de_[int(i)]  # aggiungo la frasi all'indice i nella lista
        frasi_ted.append(s)  # aggiungo la lista alla lista

    frasi_ing = []  # la lista che conterra' la lista di frasi inglesi
    for indici in ind_ing_coref:  # per gli indici in ind_ing
        indici = [indici[1:len(indici) - 1]]  #  la trasformo in lista
        s = ""  # lista che conterra' le singole frasi
        for ind in indici:  # per ogni indice nella lista di indici
            j = ind.split(",")  # separo gli indici (se più di uno)
            for i in j:  # per ogni indice negli indici
                s += sent_[int(i)]  # aggiungo la frasi all'indice i nella lista
        frasi_ing.append(s)  # aggiungo la lista alla lista

    indici_p = []
    for v in analysis_:  # per ogni elemento in analysis
        if v == "VP" or v == "FP":  # se e' un vero positivo
            indici_p.append(analysis_.index(v))  # prendo l'indice
            analysis_[analysis_.index(v)] = "preso"

    for frase in frasi_ing:  # per ogni frase nella nuova lista
        sent_core.append(nlp(frase))  # la faccio diventare doc

    for frase in frasi_ted:  # per ogni frase nella nuova lista
        sent_de.append(nlp2(frase))

    sent_core_de = []  # lista che conterra' le frasi che hanno la coreference
    sent_core_de_all = []  # lista che conterra' le frasi che hanno la coreference
    for i in indici_p:  # prendo le frasi attraverso gli indici delle frasi che sono veri positivi (considero solo quelli)
        if str(defile.name).startswith("de"):
            coref = coreferences(i, sent_de, sent_core, pron, names)  # richiamo il metodo che si occupa di aggiungere le coref al testo tedesco con pronomi pers e poss
            coref_all = coreferences(i, sent_de, sent_core, pron_all, names)  # richiamo il metodo che si occupa di aggiungere le coref al testo tedesco con pers poss e rel
            sent_core_de.append(coref)  # aggiungo la frase con pronomi possessivi e personali alla lista
            sent_core_de_all.append(coref_all)  # aggiungo la frase con pronomi possessivi e personali e relativi alla lista

    defile_name = defile.name
    f2 = open(defile_name[:len(defile_name) - 4] + "." + analysis.name.split(".")[1] + ".my.pcr.txt", "w")  # apro un file con il nome del file + pcr che corrisponde a pronominal coreference
    for riga in sent_core_de:
        f2.write(riga + "\n" + "\n")
    f2.close()

    defile_name = defile.name
    f2 = open(defile_name[:len(defile_name) - 4] + "." + analysis.name.split(".")[1] + ".my.all.pcr.txt", "w")  # apro un file con il nome del file + pcr che corrisponde a pronominal coreference
    for riga in sent_core_de_all:
        f2.write(riga + "\n" + "\n")
    f2.close()

    return 1


# il metodo perfect_coreference per ora calcola solo le coreference a partire dai testi inglese e tedesco
# per il caso perfetto di allinemento
def perfect_coreference(enfile, defile):
    sent_core = []  # inizializzo lista che conterra' le frasi del testo inglese con le coreference dopo aver sistemato le frasi
    sent_de = []

    with open("pronouns.json") as f:
        pron = json.load(f)  # apro il file che contiene il dizionario con le info sui pronomi dal inglese al tedesco

    with open("pronouns_all.json") as f:
        pron_all = json.load(f)

    namess = open("names_pcr." + enfile.name[:len(enfile.name) - 8] + "en.txt", "r").readlines()
    names = []
    for name in namess:
        for n in name.split(","):
            names.append(n.replace("\n", ""))

    sent_ = open(enfile.name[:len(enfile.name) - 4] + ".sent.coref.txt", "r").readlines()

    enfile_name = enfile.name
    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    sent_de_ = diz_de["sent"]

    corr_right = open("align.perf." + enfile_name[:len(enfile_name) - 7] + ".txt", "r").readlines()  # carico il file che ha l'allineamento perfetto
    corr_right = "".join(corr_right).replace("\n", "").split(", ")

    ind_ted = []  # inizializzo la lista che conterra' gli indici tedeschi
    ind_ing_coref = []  # inizializzo la lista che conterra' gli indici inglesi
    for coppia in corr_right:  # per ogni coppia di indici ted->ing
        ind_ted.append(coppia.split(":")[0])  # aggiungo la lista di indici alla lista tedesca
        ind_ing_coref.append(coppia.split(":")[1])  # aggiungo la lista di indici alla lista inglese

    frasi_ted = []  # la lista che conterra' la lista di frasi tedesche
    for indici in ind_ted:  # per gli indici in ind_ted
        indici = [indici[1:len(indici) - 1]]  # la trasformo in lista
        s = ""  # lista che conterra' le singole frasi
        for ind in indici:  # per ogni indice nella lista di indici
            j = ind.split(",")  # separo gli indici (se più di uno)
            for i in j:  # per ogni indice negli indici
                s += sent_de_[int(i)]  # aggiungo la frasi all'indice i nella lista
        frasi_ted.append(s)  # aggiungo la lista alla lista

    frasi_ing = []  # la lista che conterra' la lista di frasi inglesi
    for indici in ind_ing_coref:  # per gli indici in ind_ing
        indici = [indici[1:len(indici) - 1]]  #  la trasformo in lista
        s = ""  # lista che conterra' le singole frasi
        for ind in indici:  # per ogni indice nella lista di indici
            j = ind.split(",")  # separo gli indici (se più di uno)
            for i in j:  # per ogni indice negli indici
                s += sent_[int(i)]  # aggiungo la frasi all'indice i nella lista
        frasi_ing.append(s)  # aggiungo la lista alla lista

    for frase in frasi_ing:  # per ogni frase nella nuova lista
        sent_core.append(nlp(frase))  # la faccio diventare doc

    for frase in frasi_ted:  # per ogni frase nella nuova lista
        sent_de.append(nlp2(frase))

    sent_core_de = []  # lista che conterra' le frasi che hanno la coreference
    sent_core_de_all = []  # lista che conterra' le frasi che hanno la coreference
    for i in range(min(len(frasi_ing), len(frasi_ted))):  # prendo le frasi attraverso gli indici della lista
        if str(defile.name).startswith("de"):
            coref = coreferences(i, sent_de, sent_core, pron, names)  # richiamo il metodo che si occupa di aggiungere le coref al testo tedesco con pronomi pers e poss
            coref_all = coreferences(i, sent_de, sent_core, pron_all, names)  # richiamo il metodo che si occupa di aggiungere le coref al testo tedesco con pers poss e rel
            sent_core_de.append(coref)  # aggiungo la frase con pronomi possessivi e personali alla lista
            sent_core_de_all.append(coref_all)  # aggiungo la frase con pronomi possessivi e personali e relativi alla lista

    defile_name = defile.name
    f2 = open(defile_name[:len(defile_name) - 4] + ".pcr.txt", "w")  # apro un file con il nome del file + pcr che corrisponde a pronominal coreference
    for riga in sent_core_de:
        f2.write(riga + "\n" + "\n")
    f2.close()

    defile_name = defile.name
    f2 = open(defile_name[:len(defile_name) - 4] + ".all.pcr.txt", "w")  # apro un file con il nome del file + pcr che corrisponde a pronominal coreference
    for riga in sent_core_de_all:
        f2.write(riga + "\n" + "\n")
    f2.close()

    return 1


# Il metodo coreferences aggiunge ai pronomi tedeschi la persona a cui si riferiscono (pronominal coreference) in base al testo inglese con le coreference
# prende in input la singola frase
def coreferences(i, sent_de, sent_core, pron, names):
    pro_en = []  # lista che conterra' una tripla (pronome inglese, indice, parola)
    pro_de = []  # lista che conterra' la tupla (pronome tedesco, indice)
    s_de = []  # lista che conterra' tutte le parole del testo insieme ad eventuali info sulle coreference

    for token_de in sent_de[i]:  # per ogni frase nella frase tedesca di indice i
        s_de.append(token_de.text)  # aggiungo la parola alla lista
        if (str(token_de.tag_) == "PPER" or str(token_de.tag_) == "PPOSAT" or str(token_de.tag_) == "PPOSS" or str(
                token_de.tag_) == "PRF") or str(token_de.pos_) == "PRON":  # se la parola e' un pronome
            pro_de.append((token_de.text, token_de.i))  # lo aggiungo alla lista di tuple insieme all'indice

    for token in sent_core[i]:  # per ogni parola nella frase inglese con coreference di indice i
        if (str(token.tag_) == "PRP" or str(token.tag_) == "PRP$" or str(
                token.pos_) == "PRON") and token.nbor().text == "(":  # se la parola e' un pronome personale, possessivo ed e' seguito da una parentesi
            part_sent = str(sent_core[i][token.i:])  # prendo tutta la frase a partire dal pronome corrente e la salvo
            parola = part_sent[part_sent.index("(") + 1: part_sent.index(")")]  # prendo la parola tra parentesi alla destra del pronome e la salvo
            if parola in names or parola[0].isupper():
                pro_en.append((token.text, token.i, "(" + parola + ")"))  # aggiungo alla lista la tripla di pronome indice e parola
            else:
                pro_en.append((token.text, token.i, ""))

    y = 0  # un contatore che serve per posizione in modo corretto le parole vicino ai pronomi
    c = 0  # contatore per prendere il pronome giusto dalla lista
    while c < (min(len(pro_en), len(pro_de))):
        if len(pro_en) == len(pro_de):  # se i pronomi sono di quantita' uguale
            if pro_de[c][0].lower() in pron[pro_en[c][0].lower()]:  # controllo se il pronome tedesco e' la traduzione inglese
                s_de.insert(pro_de[c][1] + y + 1,
                            pro_en[c][2])  # inserisco la parola tra parentesi dopo il pronome tedesco
                y += 1  # aumento il contatore
                c += 1  # aumento il contatore
            else:  # se non sono una la traduzione dell'altro
                # c += 1  # aumento il contatore, quindi vado avanti nella lista
                pro_de.remove(pro_de[c])  # elimino il pronome che non ha la traduzione
        elif len(pro_en) > len(pro_de) != 0 and len(pro_en) != 0 and len(
                pro_de) > c:  # se ci sono piu' pronomi inglesi di quelli tedeschi
            if pro_de[c][0].lower() in pron[pro_en[c][0].lower()]:  # controllo se il pronome tedesco e' la traduzione inglese
                s_de.insert(pro_de[c][1] + y + 1, pro_en[c][2])  # inserisco la parola tra parentesi dopo il pronome tedesco
                y += 1  # aumento il contatore
                c += 1  # aumento il contatore
            else:  # se non sono una la traduzione dell'altro
                pro_en.remove(pro_en[c])  # elimino il pronome che non ha la traduzione
        elif 0 != len(pro_de) > len(pro_en) > c and len(
                pro_en) != 0:  # se ci sono meno pronomi inglesi di quelli tedeschi
            if pro_de[c][0].lower() in pron[pro_en[c][0].lower()]:  # controllo se il pronome tedesco e' la traduzione inglese
                s_de.insert(pro_de[c][1] + y + 1, pro_en[c][2])  # inserisco la parola tra parentesi dopo il pronome tedesco
                y += 1  # aumento il contatore
                c += 1  # aumento il contatore
            else:  # se non sono una la traduzione dell'altro
                pro_de.remove(pro_de[c])  # elimino il pronome che non ha la traduzione

    s_de = " ".join(s_de).replace(" ,", ",").replace(" .", ".")  # aggiungo alla lista la stringa contenente la coreference

    return s_de


# Il metodo get_coreference prende in input il nome (stringa) del file di interesse (testo inglese) e ricava il file .html
# che contiene le info sulle coreference del testo e lo salva in formato txt, e ritorna la lista di liste dei nomi ricavati applicando la coreference
# Quindi mi crea un file con il testo inglese insieme alle coreference
def get_coreference(enfile):
    name_enfile = enfile.name[:len(enfile.name) - 4]  # prendo solo il nome del file senza l'estensione txt
    data_folder = Path("../book-nlp-master/data/output/" + name_enfile[3:name_enfile[3:].index(".") + 3] + "/" + name_enfile + ".html")  # mi salvo la directory dei file .html ricavati usando un comando di book nlp
    soup = BeautifulSoup(open(data_folder, "r"), features="html.parser")  # uso beautiful soup per convertire da html a txt
    file_pcr = name_enfile + ".pcr.txt"  # mi salvo il nome del nuovo file in una variabile
    file = open(file_pcr, "w")  # apro il nuovo file in scrittura
    file.write(soup.get_text())  # salvo il testo convertito nel file
    file.close()
    f = open(file_pcr, "r")  # riapro il lettura il file appena salvato
    lines = f.readlines()  # creo una lista di stringhe che contiene le frasi del testo
    names = lines[0][:lines[0].index("Text")].replace("\t", "").replace("Characters", "").replace("\n", "")  # ricavo i nomi dei personaggi trovati con la coreference, elimino le parentesi, il tab, l'accapo e la stringa "Characters" (introdotta con la coref)
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
    lines[0] = lines[0][lines[0].index("Text") + 4:]  # elimino la prima riga tranne la parte dopo "Text" (e' stata creata dopo e non fa parte del testo iniziale)
    f1 = open(file_pcr, "w")  # apro lo stesso file in scrittura
    f1.write("".join(lines))  # risalvo il contenuto meno la prima riga nel file che contiene la coreference
    f1.close()
    f.close()

    f2 = open("names_pcr." + enfile.name, "w")
    for name in names:
        for n in name:
            f2.write(n + "\n")
    f2.close()

    return 1  # ritorno la lista dei nomi individuati con la coreference


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
        # print("eccolo")
        # print(sentence)
        if re.match("^(\s|\`|\"|\'|\»|\«|\-|\_|\–|\‘|\“|\„|\‚)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\»|\”|\’|\’’|\-*|\“|\'*)?\s*$)", str(sentence)):  # frase completa - caso 3
            # print("caso 3")
            # Caso 3 -- Frase completa (inizia con maiuscola e termina col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in sent_2[len(sent_2) - 1]:  # se non sta nella frase precedente
                    sent_2.append(str(sentence))  # aggiungi la frase alla lista
            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase nella lista

        elif re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\–|\“|\'|\`|\‚|\‘|\„|\"|\»|\«)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\«\»\”\’\—\’’\“ ]$", str(sentence)):  # se la frase inizia con la maiuscola non finisce con ".", "?", "!" o "…" - caso 1
            # print("caso 1")
            # Caso 1 -- Inizio frase (inizia con maiuscola ma non finisce col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in sent_2[len(sent_2) - 1]:  # se non sta nella frase precedente
                    if i + 1 < len(sent):  # controllo per non avere errore
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2.append(str(sentence) + " " + str(s))  # aggiungo alla frase prima la frase dopo
                    else:  # se non c'e' la successiva
                        sent_2.append(str(sentence))  # aggiungi alla lista
            else:  # se la lista e' vuota
                if i + 1 < len(sent):  # controllo per non avere errore
                    s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                    sent_2.append(str(sentence) + " " + str(s))  # aggiungo alla frase prima la frase dopo
                else:  # se non c'e' la successiva
                    sent_2.append(str(sentence))  # aggiungi alla lista

        elif re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\–|\`|\"|\'|\'|\“|\‚|\‘|\„|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\»|\“|\”|\’’|\‚|\’|\‘|\-*|\„|\“|\'*)?\s*$)", str(sentence)):  # la fine di una frase - caso 4
            # print("caso 4")
            # Caso 4 -- Fine di una frase (inizia con minuscola e termina col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # se non sta nella frase prima
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence)  # aggiungo alla frase la frase dopo
            else:  # se e' vuota
                sent_2.append(str(sentence))  # aggiungo la frase

        elif re.match("^(\s|\;|\:|\(|\,|\[|\{|\_|\-|\–|\`|\"|\'|\'|\“|\‚|\‘|\„|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\—\`\«\»\“\”\’’\‚\’\‘\„\“ ]$", str(sentence)):  # se e' in mezzo  - caso 2
            # print("caso 2")
            # Caso 2 -- Se e' una frase intermedia ( inizia con minuscola, non finisce col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # e la frase non e' stata ancora aggiunta
                    if i + 1 < len(sent):
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence) + " " + str(s)  # aggiungo la frase attuale a quella precedente
                    else:
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence)
                else:
                    if i + 1 < len(sent):
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(s)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista e' vuota
                if i + 1 < len(sent):
                    s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                    sent_2.append(str(sentence) + " " + str(s))  # aggiungo la frase con la frase dopo
                else:
                    sent_2.append(str(sentence))  # aggiungi la frase alla lista
        else:  # se non rientra in nessuno dei casi
            # print("caso 5")
            if len(sent_2) != 0:  # se la lista non e' vuota
                sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(sentence)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase alla lista

    # for i in range(len(sent_2)):
    #     print(str(i + 1) + " " + sent_2[i])
    return sent_2


# Il metodo sentence_splitter_coref e' uguale al metodo sentence_splitter tranne che viene applicato al file che contiene le coreference
# che ha parole tra parentesi nel testo, quindi viene trattato in modo differente, per spezzare allo stesso modo di sentence_splitter e fare in modo
# che le due liste siano divise allo stesso modo (lista delle frasi inglesi e lista delle frasi inglesi con coreference)
def sentence_splitter_coref(sent):
    sent_2 = []  # inizializzo la lista che conterra' le frasi come stringhe
    for sentence, i in zip(sent, range(len(sent))):  # per ogni frase in sent e per ogni indice
        sentence = str(sentence).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
        # print("eccolo")
        # print(sentence)
        if re.match("^(\s|\`|\"|\'|\((.*?)\)|\»|\«|\-|\_|\–|\‘|\“|\„|\‚)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]+([.?!…]\s*$|[.?!…](\"|\`|\«|\»|\”|\’|\’’|\-*|\“|\'*)?\s*$)", str(sentence)):  # frase completa - caso 3
            # print("caso 3")
            # Caso 3 -- Frase completa (inizia con maiuscola e termina col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in sent_2[len(sent_2) - 1]:  # se non sta nella frase precedente
                    sent_2.append(str(sentence))  # aggiungi la frase alla lista
            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase nella lista

        elif re.match("^(\s|\;|\:|\(|\((.*?)\)|\,|\[|\{|\_|\-|\–|\“|\'|\`|\‚|\‘|\„|\"|\»|\«)*[A-ZÄÖÜ][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\—\«\»\”\’\’’\“ ]$", str(sentence)):  # se la frase inizia con la maiuscola non finisce con ".", "?", "!" o "…" - caso 1
            # print("caso 1")
            # Caso 1 -- Inizio frase (inizia con maiuscola ma non finisce col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in sent_2[len(sent_2) - 1]:  # se non sta nella frase precedente
                    if i + 1 < len(sent):  # controllo per non avere errore
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2.append(str(sentence) + " " + str(s))  # aggiungo alla frase prima la frase dopo
                    else:  # se non c'e' la successiva
                        sent_2.append(str(sentence))  # aggiungi alla lista
            else:  # se la lista e' vuota
                if i + 1 < len(sent):  # controllo per non avere errore
                    s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                    sent_2.append(str(sentence) + " " + str(s))  # aggiungo alla frase prima la frase dopo
                else:  # se non c'e' la successiva
                    sent_2.append(str(sentence))  # aggiungi alla lista

        elif re.match("^(\s|\;|\:|\(|\,|\[|\((.*?)\)|\{|\_|\-|\–|\`|\"|\'|\'|\“|\‚|\‘|\„|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*([.?!…]\s*$|[.?!…](\"|\`|\«|\»|\“|\”|\’’|\‚|\’|\‘|\-*|\„|\“|\'*)?\s*$)", str(sentence)):  # la fine di una frase - caso 4
            # print("caso 4")
            # Caso 4 -- Fine di una frase (inizia con minuscola e termina col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # se non sta nella frase prima
                    sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence)  # aggiungo alla frase la frase dopo
            else:  # se e' vuota
                sent_2.append(str(sentence))  # aggiungo la frase

        elif re.match("^(\s|\;|\:|\(|\,|\[|\((.*?)\)|\{|\_|\-|\–|\`|\"|\'|\'|\“|\‚|\‘|\„|\»|\«)*[a-zäöü][a-zA-ZäöüÄÖÜß\s\S\d ]*[A-Za-z0-9,:;\]\)\}\-_\"\'\`\—\«\»\“\”\’’\‚\’\‘\„\“ ]$", str(sentence)):  # se e' in mezzo  - caso 2
            # print("caso 2")
            # Caso 2 -- Se e' una frase intermedia ( inizia con minuscola, non finisce col punto)
            if len(sent_2) != 0:  # se la lista non e' vuota
                if str(sentence) not in str(sent_2[len(sent_2) - 1]):  # e la frase non e' stata ancora aggiunta
                    if i + 1 < len(sent):
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence) + " " + str(s)  # aggiungo la frase attuale a quella precedente
                    else:
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(sentence)
                else:
                    if i + 1 < len(sent):
                        s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                        sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + " " + str(s)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista e' vuota
                if i + 1 < len(sent):
                    s = str(sent[i + 1]).replace("\n", " ").replace("\t", " ").replace("\r", " ").replace("\v", " ").replace("\f", " ")  # elimino i caratteri di escape
                    sent_2.append(str(sentence) + " " + str(s))  # aggiungo la frase con la frase dopo
                else:
                    sent_2.append(str(sentence))  # aggiungi la frase alla lista
        else:  # se non rientra in nessuno dei casi
            # print("caso 5")
            if len(sent_2) != 0:  # se la lista non e' vuota
                sent_2[len(sent_2) - 1] = str(sent_2[len(sent_2) - 1]) + str(
                    sentence)  # aggiungo la frase attuale a quella precedente
            else:  # se la lista e' vuota
                sent_2.append(str(sentence))  # aggiungi la frase alla lista

    # for i in range(len(sent_2)):
    #     print(str(i + 1) + " " + sent_2[i])
    return sent_2


# Il metodo direct_speech prende il testo separato in frasi e sistema il discorso diretto
def direct_speech(sent):
    sent_2 = []  # lista finale con frasi giuste
    fusion = ""  # fusione di una frase con la successiva
    virgolette = {"»", "«", "“", "”", "„", "“", "\""}  # insieme di virgolette usate nel discorso diretto
    count = 0  # contatore che mi conta quante virgolette ci sono nel testo
    for s in sent:  # per ogni frase nella lista
        fusion += s  # unisco la frase con la successiva
        for v in virgolette:  # per ogni virgoletta nella lista
            count += s.count(v)  # aumenta il contatore con il numero di virgolette
        if count % 2 == 0:  # se il numero e' pari
            sent_2.append(fusion)  # aggiungo la frase sistemata nella lista
            fusion = ""  # pulisco la stringa
            count = 0  # azzero il contatore
    # for i in range(len(sent_2)):
    #     print(str(i + 1) + " " + sent_2[i])
    return sent_2


# Il metodo bio_gender prende una frase e da' un genere biologico al sostantivo inglese, in base alle regole della grammatica tedesca
def bio_gender(sent_de, tok_syn_en, tok_syn_de, i):
    m = ["ling", "ich", "ig", "ant", "ent", "eur", "ist", "ismus", "or"]  # alcuni sostantivi maschili terminano cosi'
    f = ["schaft", "tät", "taet", "ik", "ung", "ion", "heit", "keit", "ei", "kunft", "falt", "t", "ade", "age", "anz", "ur"]  # alcuni sostantivi femminili terminano cosi'
    n = ["chen", "lein", "ment", "um", "ma", "o", "nis"]  # alcuni sostantivi neutrali terminano cosi'
    p = ["en", "e", "n", "s", "er"]  # alcuni sostantivi in plurale terminano cosi'

    maskulin = "".join(open("maskulin.txt", "r").readlines())  # salvo in una lista alcuni sostantivi maschili
    feminin = "".join(open("feminin.txt", "r").readlines())  # salvo in una lista alcuni sostantivi femminili
    neutrum = "".join(open("neutrum.txt", "r").readlines())  # salvo in una lista alcuni sostantivi neutrali
    plural = "".join(open("plural.txt", "r").readlines())  # salvo in una lista alcuni sostantivi che esistono solo in plurale o che sono uguali al singolare

    en_info = {}  # dizionario che conterra' le info sul genere collegate alla parola inglese

    for token in sent_de[i]:  # per ogni parola tedesca nella frase
        if str(token.pos_) == "NOUN":  # se la parola e' un sostantivo
            translation = ""  # inizializzo la stringa della traduzione
            syns = tok_syn_de[i][str(token)]  # ricavo la lista dei synset della parola tedesca
            for syn in syns:  # per ogni synset
                for key, value in tok_syn_en[i].items():  # per ogni parola e ogni lista di synset del dizionario inglese
                    if syn in value:  # se il synset della parola tedesca si trova in una lista di synset delle parole inglesi
                        translation = key  # prendi la parola inglese

            if str(token) in plural or str(token).endswith(tuple(p)) and str(token) != str(token.lemma_):  # se sta nella lista dei plurai oppure finisce in un certo modo e il lemma e' diverso (il lemma sara' il singolare)
                if translation != "":  # se c'e' la traduzione
                    en_info[translation] = ["plural"]  # allora aggiungi al dizionario l'informazione del plurale

            if str(token.lemma_).endswith(tuple(m)) or str(token.lemma_) in maskulin:  # se finisce con qualcosa in m o sta nella lista dei maschili
                if translation != "":  # se c'e' la traduzione
                    if translation in en_info.keys():  # se c'e' gia' la parola (cioe' e' plurale)
                        en_info[translation].append("biologically male")  # aggiungi alla lista che e' biologicamente maschile
                    else:  # se non c'e' gia' nel dizionario (non e' plurale)
                        en_info[translation] = ["biologically male"]  # aggiungi la parola al dizionario con l'info che e' biologicamente maschile
                    en_info[translation].append(gram_gender(sent_de, i, token, en_info, translation))  # aggiungo alla lista della info il genere grammaticale richiamando il metodo gram_gender

            elif str(token.lemma_).endswith(tuple(f)) or str(token.lemma_) in feminin:  # se finisce con qualcosa in f o sta nella lista dei femminili
                if translation != "":  # se c'e' la traduzione
                    if translation in en_info.keys():  # se c'e' gia' la parola (cioe' e' plurale)
                        en_info[translation].append("biologically female")  # aggiungi alla lista che e' biologicamente femminile
                    else:  # se non c'e' gia' nel dizionario (non e' plurale)
                        en_info[translation] = ["biologically female"]  # aggiungi la parola al dizionario con l'info che e' biologicamente femminile
                    en_info[translation].append(gram_gender(sent_de, i, token, en_info, translation))  # aggiungo alla lista della info il genere grammaticale richiamando il metodo gram_gender

            elif str(token.lemma_).endswith(tuple(n)) or str(token.lemma_) in neutrum:  # se e' un sostantivo neutro
                if translation != "":  # se c'e' la traduzione
                    if translation in en_info.keys():  # se c'e' gia' la parola (cioe' e' plurale)
                        en_info[translation].append("biologically undetermined")  # aggiungi alla lista che e' biologicamente indeterminato
                    else:  # se non c'e' gia' nel dizionario (non e' plurale)
                        en_info[translation] = ["biologically undetermined"]  # aggiungi la parola al dizionario con l'info che e' biologicamente indeterminato
                    en_info[translation].append(gram_gender(sent_de, i, token, en_info, translation))  # aggiungo alla lista della info il genere grammaticale richiamando il metodo gram_gender

            else:  # se non rientra in nessuno dei casi sopra
                if translation != "":  # se c'e' la traduzione
                    if translation in en_info.keys():  # se c'e' gia' la parola (cioe' e' plurale)
                        en_info[translation].append("biologically unknown")  # aggiungi alla lista che e' biologicamente sconosciuto
                    else:  # se non c'e' gia' nel dizionario (non e' plurale)
                        en_info[translation] = ["biologically unknown"]  # aggiungi la parola al dizionario con l'info che e' biologicamente sconosciuto
                    en_info[translation].append(gram_gender(sent_de, i, token, en_info, translation))  # aggiungo alla lista della info il genere grammaticale richiamando il metodo gram_gender
    return en_info


# Il metodo gram_gender da' al sostantivo un genere grammaticale in base all'articolo dal quale e' preceduto
def gram_gender(sent_de, i, token, en_info, translation):
    art_m = ["der", "des", "dem", "den", "ein", "eines", "einem", "einen", "jeder"]  # articoli per i sostantivi maschili
    art_f = ["die", "der", "eine", "einer", "jede"]  # articoli per i sostantivi femminili
    art_n = ["das", "des", "dem", "das", "ein", "eines", "einem", "jedes"]  # articoli per i sostantivi neutri
    art_p = ["die", "der", "den", "die"]  # articoli per il plurale

    if str(sent_de[i][token.i - 1]).lower() in list(set(art_m) & set(art_n)) or str(sent_de[i][token.i - 2]).lower() in list(set(art_m) & set(art_n)):  # ci sono alcuni articoli in comune quindi
        if en_info[translation][0].split(" ")[1] == "male":  # se la parola e' biologicamente maschile
            return "grammatical masculine"  # allora lo e' anche grammaticalmente
        elif en_info[translation][0].split(" ")[1] == "undetermined":  # se la parola e' biologicamente indefinita
            return "grammatically neutral"  # allora e' grammaticalmente neutro

    if str(sent_de[i][token.i - 1]).lower() in list(set(art_m) & set(art_f)) or str(sent_de[i][token.i - 2]).lower() in list(set(art_m) & set(art_f)):  # ci sono alcuni articoli in comune quindi
        if en_info[translation][0].split(" ")[1] == "male":  # se la parola e' biologicamente maschile
            return "grammatical masculine"  # allora lo e' anche grammaticalmente
        elif en_info[translation][0].split(" ")[1] == "female":  # se la parola e' biologicamente femminile
            return "grammatically feminine"  # allora lo e' anche grammaticalmente

    if en_info[translation][0] == "plural" and (str(sent_de[i][token.i - 1]).lower() in art_p or str(sent_de[i][token.i - 2]).lower() in art_p):  # se la parola e' plurale ed e' preceduta da un atricolo in art_p
        if en_info[translation][1].split(" ")[1] == "male":  # se e' biologicamente maschile
            return "grammatical masculine"  # allora e' grammaticalmente maschile (poiche' l'articolo e' diverso tra plurale e singolare)
        elif en_info[translation][1].split(" ")[1] == "undetermined":  # se e' biologicamente indeterminato
            return "grammatically neutral"  # allora e' grammaticalmente neutrale (poiche' l'articolo e' diverso tra plurale e singolare)
        elif en_info[translation][1].split(" ")[1] == "female":  # se e' biologicamente femminile
            return "grammatically feminine"  # allora e' grammaticalmente femminile (poiche' l'articolo e' diverso tra plurale e singolare)
        else:  # se e' biologicamente sconosciuto
            return "grammatically unknown"  # allora e' grammaticalmente sconosciuto (poiche' l'articolo e' diverso tra plurale e singolare)

    if str(sent_de[i][token.i - 1]).lower() in art_f or str(sent_de[i][token.i - 2]).lower() in art_f:  # se l'articolo prima si trova in art_f
        return "grammatical feminine"  # allora e' grammaticalmente femminile

    elif str(sent_de[i][token.i - 1]).lower() in art_m or str(sent_de[i][token.i - 2]).lower() in art_m:  # se l'articolo prima si trova in art_m
        return "grammatical masculine"  # allora e' grammaticalmente maschile

    elif str(sent_de[i][token.i - 1]).lower() in art_n or str(sent_de[i][token.i - 2]).lower() in art_n:  # se l'articolo prima si trova in art_n
        return "grammatically neutral"  # allora e' grammaticalmente neutrale
    else:  # se non c'e'
        return "grammatically unknown"  # allora e' grammaticalmente sconosciuto


# Il metodo join_sentences controlla le frasi che sono state spezzate, e le unisce per allinearsi con la propria traduzione
def join_sentences(sent_en, sent_de, i):
    return 1
