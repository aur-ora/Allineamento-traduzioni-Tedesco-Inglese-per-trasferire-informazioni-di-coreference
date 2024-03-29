from .alignment_BabelNet import create_set_en, create_set_de
import json


# il metodo transform_in_file prende i due testi e salva la divisione delle frasi, gli insiemi dei synset e il numero di parole in un dizionario per ciascuna lingua
def transform_in_file(enfile, defile):
    sent_en, list_set_en, tok_en, words_en = create_set_en(enfile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de, tok_de, words_de = create_set_de(defile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase tedesca

    info_en = {}  # dizionario info testo inglese
    info_de = {}  # dizionario info testo tedesco

    list_en = []  # lista che conterra' le frasi inglesi
    list_de = []  # lista che conterra' le frasi tedesche
    l_set_en = []  # lista che conterra' la lista dei synset per ogni frase inglese
    l_set_de = []  # lista che conterra' la lista dei synset per ogni frase tedesca

    for i in sent_en:  # per ogni frase nella lista delle frasi inglesi
        list_en.append(str(i))  # trasformo la frase da doc a stringa

    for i in sent_de:  # per ogni frase nella lista delle frasi tedesche
        list_de.append(str(i))  # trasformo la frase da doc a stringa

    for se in list_set_en:  # per ogni insieme nella lista degli insiemi di synset inglesi
        li = []  # inizializzo la lista che conterra' i synset
        for b in se:  # per ogni synset nell'insieme
            li.append(b)  # aggiungi il synset alla lista
        l_set_en.append(li)  # aggiungi la lista alla lista che conterra' le lista di synset per ogni frase inglese, salvo gli insiemi come lista (perche' gli insiemi non sono JSON serializable)

    for se in list_set_de:  # per ogni insieme nella lista degli insiemi di synset tedeschi
        li = []  # inizializzo la lista che conterra' i synset
        for b in se:  # per ogni synset nell'insieme
            li.append(b)  # aggiungi il synset alla lista
        l_set_de.append(li)  # aggiungi la lista alla lista che conterra' le lista di synset per ogni frase tedesca, salvo gli insiemi come lista (perche' gli insiemi non sono JSON serializable)

    info_en["sent"] = list_en  # aggiungo la lista di frasi inglesi al dizionario con chiave "sent"
    info_en["list_set"] = l_set_en  # aggiungo la lista di liste di synset al dizionario con chiave "list_set"
    info_en["words"] = words_en  # aggiungo il numero di parole con synset per ciascuna frase al dizionario con chiave

    info_de["sent"] = list_de  # aggiungo la lista di frasi inglesi al dizionario con chiave "sent"
    info_de["list_set"] = l_set_de  # aggiungo la lista di liste di synset al dizionario con chiave "list_set"
    info_de["words"] = words_de  # aggiungo il numero di parole con synset per ciascuna frase al dizionario con chiave

    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "w") as fp:
        json.dump(info_en, fp)  # salvo il dizionario per le frasi inglesi in un file json che chiamo "sent_en_" + il nome del file inglese

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "w") as f:
        json.dump(info_de, f)  # salvo il dizionario per le frasi tedesche in un file json che chiamo "sent_en_" + il nome del file tedesco

    return 1


# calcolare la similarita' per calcolare la percentuali per i 6 casi definiti (lo uso per avere le percentuali di riferimento)
def calculate_percentage(enfile, defile):
    # sent_en, list_set_en, tok_en, words_en = create_set_en(enfile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase inglese
    # sent_de, list_set_de, tok_de, words_de = create_set_de(defile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase tedesca
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    list_set_en = diz_en["list_set"]  # ricavo la lista delle liste di synset delle frasi inglesi
    list_set_de = diz_de["list_set"]  # ricavo la lista delle liste di synset delle frasi tedesche
    words_en = diz_en["words"]  # ricavo la lista di numero di parole inglesi con synset
    words_de = diz_de["words"]  # ricavo la lista di numero di parole tedesche con synset

    min_length = []  # lista che contiene tutte le percentuali per il caso 1
    max_length = []  # lista che contiene tutte le percentuali per il caso 2
    union_set = []  # lista che contiene tutte le percentuali per il caso 3
    max_w = []   # lista che contiene tutte le percentuali per il caso 4
    min_w = []   # lista che contiene tutte le percentuali per il caso 5
    sum_w = []   # lista che contiene tutte le percentuali per il caso 6

    # Caso 1 -> denominatore come minimo di lunghezza dei due insiemi di synset
    for i in range(min(len(list_set_de), len(list_set_en))):  # prendo le frasi attraverso gli indici della lista
        common = len(set(list_set_en[i]).intersection(set(list_set_de[i])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimum = min(len(set(list_set_de[i])), len(set(list_set_en[i])))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

        if minimum != 0:  # per evitare errore di divisione per 0
            min_length.append(common/minimum)  # aggiungo alla lista la percentuale che esce dalla divisione
        else:  # se e' uguale a 0 il denominatore
            min_length.append(0.0)  # aggiungo alla lista 0.0

    # Caso 2 -> denominatore come massimo di lunghezza dei due insiemi di synset
        maximum = max(len(set(list_set_en[i])), len(set(list_set_de[i])))  # prendo il massimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

        if maximum != 0:  # per evitare errore di divisione per 0
            max_length.append(common/maximum)   # aggiungo alla lista la percentuale che esce dalla divisione
        else:
            max_length.append(0.0)

    # Caso 3 -> denominatore come unione dei due insiemi
        union = len(set(list_set_en[i]).union(set(list_set_de[i])))

        if union != 0:  # per evitare errore di divisione per 0
            union_set.append(common/union)   # aggiungo alla lista la percentuale che esce dalla divisione
        else:
            union_set.append(0.0)

    # Caso 4 -> denominatore come massimo tra il numero di parole inglesi e tedesche
        max_words = max(words_en[i], words_de[i])

        if max_words != 0:  # per evitare errore di divisione per 0
            max_w.append(common/max_words)   # aggiungo alla lista la percentuale che esce dalla divisione
        else:
            max_w.append(0.0)

    # Caso 5 -> denominatore come minimo tra il numero di parole inglesi e tedesche
        min_words = min(words_en[i], words_de[i])

        if min_words != 0:  # per evitare errore di divisione per 0
            min_w.append(common/min_words)   # aggiungo alla lista la percentuale che esce dalla divisione
        else:
            min_w.append(0.0)

    # Caso 6 -> denominatore come somma di numero di parole inglesi e tedesche
        sum_words = words_en[i] + words_de[i]

        if sum_words != 0:  # per evitare errore di divisione per 0
            sum_w.append(common/sum_words)   # aggiungo alla lista la percentuale che esce dalla divisione
        else:
            sum_w.append(0.0)

    perc_case = {}  # dizionario che contiene il nome del caso e la media che esce da quel caso

    som_1 = 0
    for i in min_length:
        som_1 += i
    if len(min_length) != 0:
        perc_case["min_length"] = som_1 / len(min_length)
    else:
        perc_case["min_length"] = 0.0

    som_2 = 0
    for i in max_length:
        som_2 += i
    if len(max_length) != 0:
        perc_case["max_length"] = som_2 / len(max_length)
    else:
        perc_case["max_length"] = 0.0

    som_3 = 0
    for i in union_set:
        som_3 += i
    if len(union_set) != 0:
        perc_case["union"] = som_3/len(union_set)
    else:
        perc_case["union"] = 0.0

    som_4 = 0
    for i in max_w:
        som_4 += i
    if len(max_w) != 0:
        perc_case["max_#_words"] = som_4 / len(max_w)
    else:
        perc_case["max_#_words"] = 0.0

    som_5 = 0
    for i in min_w:
        som_5 += i
    if len(min_w) != 0:
        perc_case["min_#_words"] = som_5 / len(min_w)
    else:
        perc_case["min_#_words"] = 0.0

    som_6 = 0
    for i in sum_w:
        som_6 += i
    if len(sum_w) != 0:
        perc_case["sum_#_words"] = som_6 / len(sum_w)
    else:
        perc_case["sum_#_words"] = 0.0

    return perc_case


# calcolo la media aritmetica sia per il caso in cui le frasi sono traduzioni e il caso in cui non lo sono per tutti e sei i casi e salvare le medie in un dizionario
def media_arit():
    right_en = open("sent_perc_en.txt", "r")  # file che contiene le frasi inglesi
    right_de = open("sent_perc_de.txt", "r")  # file che contiene le frasi tedesche con traduzione corrispondente
    wrong_en = open("wrong_sent_perc_en.txt", "r")  # file che contiene le frasi inglesi (in posizione diverse rispetto a right_en)
    wrong_de = open("wrong_sent_perc_de.txt", "r")  # file che cotiene le frasi tedesche senza traduzione corrispondente
    right_perc_case = calculate_percentage(right_en, right_de)
    wrong_perc_case = calculate_percentage(wrong_en, wrong_de)

    print("right_perc_case")
    print(right_perc_case)
    print("wrong_perc_case")
    print(wrong_perc_case)

    mean = {}  # dizionario che contiene la media delle due medie (traduzione giusta e sbagliata) per ciascuno dei 6 casi

    for type_cal_perc in right_perc_case:  # per ciascuno dei 6 casi
        mean[type_cal_perc] = (right_perc_case[type_cal_perc] + wrong_perc_case[type_cal_perc]) / 2  # Media tra percentuali tra frasi con trad giusta e sbagliata

    with open('media_casi_arit.json', 'w') as fp:
        json.dump(mean, fp)

    return 1


# mi calcola la precision, la recall, l'f1 e tutto altro, considerando entrambi i versi e quindi fondendo i risultati
def precision_recall_f1(enfile, caso, k,  file_ing, file_ted):
    enfile_name = enfile.name
    file_ing = file_ing.readlines()
    file_ing = "".join(file_ing)
    file_ing = file_ing.split("_______________________________________________________________________________________________________________________________________________\n")
    ing = []
    for el in file_ing:
        if el.split("\n") != ['']:
            ing.append(el.split("\n"))

    file_ted = file_ted.readlines()
    file_ted = "".join(file_ted)
    file_ted = file_ted.split("_______________________________________________________________________________________________________________________________________________\n")
    ted = []

    for el in file_ted:
        if el.split("\n") != ['']:
            ted.append(el.split("\n"))

    for lista in ing:
        for el in lista:
            if el == "":
                lista.remove(el)

        if lista[0].split("-")[0] == caso and int(lista[0].split("-")[1]) == k:  # prendo il caso e la k giusti
            frasi_ing = int(lista[1].split(" = ")[1])
            vp_ing = int(lista[2].split(" = ")[1])
            vn_ing = int(lista[3].split(" = ")[1])
            fp_ing = int(lista[4].split(" = ")[1])
            fn_ing = int(lista[5].split(" = ")[1])
            precision_ing = float(lista[6].split(" = ")[1])
            recall_ing = float(lista[7].split(" = ")[1])
            f1_ing = float(lista[8].split(" = ")[1])

    for lista in ted:
        for el in lista:
            if el == "":
                lista.remove(el)

        if lista[0].split("-")[0] == caso and int(lista[0].split("-")[1]) == k:    # prendo il caso e la k giusti
            frasi_ted = int(lista[1].split(" = ")[1])
            vp_ted = int(lista[2].split(" = ")[1])
            vn_ted = int(lista[3].split(" = ")[1])
            fp_ted = int(lista[4].split(" = ")[1])
            fn_ted = int(lista[5].split(" = ")[1])
            precision_ted = float(lista[6].split(" = ")[1])
            recall_ted = float(lista[7].split(" = ")[1])
            f1_ted = float(lista[8].split(" = ")[1])

    frasi_tot = (frasi_ing + frasi_ted)
    vp_tot = (vp_ted + vp_ing) / frasi_tot
    fp_tot = (fp_ted + fp_ing) / frasi_tot
    fn_tot = (fn_ted + fn_ing) / frasi_tot
    vn_tot = (vn_ted + vn_ing) / frasi_tot

    perc_fp = fp_tot * 100
    perc_fn = fn_tot * 100

    recall = vp_tot/(vp_tot + fn_tot)
    precision = vp_tot/(vp_tot + fp_tot)
    if recall == 0 and precision == 0:
        f1 = 0.0
    elif recall == 0:
        f1 = 2 / (1 / precision)
    elif precision == 0:
        f1 = 2 / (1 / recall)
    else:
        f1 = 2 / ((1/precision) + (1/recall))

    file = open("analysis_final." + enfile_name[:len(enfile_name) - 7] + ".txt", "a")
    file.write("_______________________________________________________________________________________________________________________________________________\n")
    file.write("_______________________________________________________________________________________________________________________________________________\n")
    file.write("\n")
    file.write("CASO - " + caso + " con k = " + str(k) + "\n")
    file.write("\n")
    file.write("ANALISI CONSIDERANDO UNA AD UNA LE FRASI INGLESI E K VOLTE QUELLE TEDESCHE \n")
    file.write("\n")
    file.write("# frasi ing->ted = " + str(frasi_ing) + "\n")
    file.write("\n")
    file.write("# VERI POSITIVI ing->ted = " + str(vp_ing) + "\n")
    file.write("\n")
    file.write("# VERI NEGATIVI ing->ted = " + str(vn_ing) + "\n")
    file.write("\n")
    file.write("# FALSI POSITIVI ing->ted = " + str(fp_ing) + "\n")
    file.write("\n")
    file.write("# FALSI NEGATIVI ing->ted = " + str(fn_ing) + "\n")
    file.write("\n")
    file.write("PRECISION ing->ted = " + str(precision_ing) + "\n")
    file.write("\n")
    file.write("RECALL ing->ted = " + str(recall_ing) + "\n")
    file.write("\n")
    file.write("F1 ing->ted = " + str(f1_ing) + "\n")
    file.write("\n")
    file.write("ANALISI CONSIDERANDO UNA AD UNA LE FRASI TEDESCHE E K VOLTE QUELLE INGLESE \n")
    file.write("\n")
    file.write("# frasi ted->ing = " + str(frasi_ted) + "\n")
    file.write("\n")
    file.write("# VERI POSITIVI ted->ing = " + str(vp_ted) + "\n")
    file.write("\n")
    file.write("# VERI NEGATIVI ted->ing = " + str(vn_ted) + "\n")
    file.write("\n")
    file.write("# FALSI POSITIVI ted->ing = " + str(fp_ted) + "\n")
    file.write("\n")
    file.write("# FALSI NEGATIVI ted->ing = " + str(fn_ted) + "\n")
    file.write("\n")
    file.write("PRECISION ted->ing = " + str(precision_ted) + "\n")
    file.write("\n")
    file.write("RECALL ted->ing = " + str(recall_ted) + "\n")
    file.write("\n")
    file.write("F1 ted->ing = " + str(f1_ted) + "\n")
    file.write("\n")
    file.write("\n")
    file.write("# frasi totali = " + str(frasi_tot) + "\n")
    file.write("\n")
    file.write("# VERI POSITIVI = " + str(vp_tot) + "\n")
    file.write("\n")
    file.write("# VERI NEGATIVI = " + str(vn_tot) + "\n")
    file.write("\n")
    file.write("# FALSI POSITIVI = " + str(fp_tot) + "\n")
    file.write("\n")
    file.write("# FALSI NEGATIVI = " + str(fn_tot) + "\n")
    file.write("\n")
    file.write("PERCENTUALE DI VERI POSITIVI = " + str(vp_tot * 100) + " %" + "\n")
    file.write("\n")
    file.write("PERCENTUALE DI VERI NEGATIVI = " + str(vn_tot * 100) + " %" + "\n")
    file.write("\n")
    file.write("PERCENTUALE DI FALSI POSITIVI = " + str(perc_fp) + " %" + "\n")
    file.write("\n")
    file.write("PERCENTUALE DI FALSI NEGATIVI = " + str(perc_fn) + " %" + "\n")
    file.write("\n")
    file.write("PRECISION = " + str(precision) + "\n")
    file.write("\n")
    file.write("RECALL = " + str(recall) + "\n")
    file.write("\n")
    file.write("% PRECISION = " + str(precision * 100) + " %" + "\n")
    file.write("\n")
    file.write("% RECALL = " + str(recall * 100) + " %" + "\n")
    file.write("\n")
    file.write("F1 = " + str(f1) + "\n")
    file.write("\n")
    file.write("% F1 = " + str(f1 * 100) + " %" + "\n")
    file.write("\n")
    file.write("_______________________________________________________________________________________________________________________________________________\n")
    file.write("_______________________________________________________________________________________________________________________________________________\n")
    file.close()

    return 1


# il metodo auto_analysis dovrebbe analizzare i veri positivi, i falsi postivi, i veri negativi e i falsi negativi in modo autonomo, prende il input i due testi, il caso, una stringa, che specifica
# quale dei 6 casi viene usato e il numero k (# di frasi che si considerano per l'analisi)
def auto_analysis(enfile, caso, k, lingua):
    enfile_name = enfile.name
    corr_found = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_" + caso + ".corr.txt", "r").readlines()
    corr_right = open("str." + lingua + ".fu." + enfile_name[:len(enfile_name) - 7] + ".right.corr.txt", "r").readlines()

    corr_found.remove(corr_found[0])

    analisi = []  # conterra' una stringa che indica se le corrispondenze sono veri positivi/negativi e falsi positivi/negativi

    corr_found = "".join(corr_found).split(", ")  # prendo il file con le info sulle corrispondenze trovate e lo trasformo in lista
    corr_right = "".join(corr_right).replace("\n", "").split(", ")  # prendo il file con le info sulle corrispondenze giuste e lo trasformo in lista

    i = 0  # indice per le corrispondenze trovate
    j = 0  # indice per le corrispondenze corrette
    while i < len(corr_found) and j < len(corr_right):  # finche' il contatore non arriva alla lunghezza della lista di coppie di corrispondenze
        if corr_right[j] == corr_found[i][:-6]:  # se gli elementi ad indice uguale sono uguali
            if corr_found[i].split(":")[2] == "[neg]":  # allora se non ha corrispondenza (neg)
                if corr_found[i].split(":")[1] == "[-1]":  # se c'e' un -1 (in questo caso da entrambi perche' sono uguali le coppie)
                    analisi.append("VN")  # significa che non ha corrispondenza
                    i += 1  # aumento il contatore delle trovate
                    j += 1  # aumento il contatore delle corrette
                else:  # se non c'e' un -1, significa che avrebbe dovuto esserci, ma non l'ha trovata quindi
                    analisi.append("FN")  # e' un falso negativo
                    i += 1  # aumento il contatore delle trovate
                    j += 1  # aumento il contatore delle corrette
            else:  # se ha corrispondenza (pos) significa che
                analisi.append("VP")  # e' un vero positivo, in quanto le due coppie confrontate sono uguali
                i += 1  # aumento il contatore delle trovate
                j += 1  # aumento il contatore delle corrette
        else:  # se gli elementi ad indice uguale sono diversi
            if corr_found[i].split(":")[0] == corr_right[j].split(":")[0]:  # se il primo elemento della coppia e' uguale (quindi non abbiamo più indici a sinistra)
                if corr_found[i].split(":")[1] == "[-1]":
                    analisi.append("FN")  # e' un falso negativo
                    i += 1  # aumento il contatore delle trovate
                    j += 1  # aumento il contatore delle corrette
                elif corr_right[j].split(":")[1] == "[-1]":
                    if corr_found[i].split(":")[2] == "[neg]":
                        analisi.append("VN")  # e' un vero negativo
                        i += 1  # aumento il contatore delle trovate
                        j += 1  # aumento il contatore delle corrette
                    else:
                        analisi.append("FP")  # e' un falso positivo
                        i += 1  # aumento il contatore delle trovate
                        j += 1  # aumento il contatore delle corrette
                else:
                    if corr_found[i].split(":")[2] == "[neg]":
                        analisi.append("FN")  # e' un falso negativo
                        i += 1  # aumento il contatore delle trovate
                        j += 1  # aumento il contatore delle corrette
                    else:
                        analisi.append("FP")  # e' un falso positivo
                        i += 1  # aumento il contatore delle trovate
                        j += 1  # aumento il contatore delle corrette
            else:  # se il primo elemento della coppia e' diverso tra le found e right (abbiamo più indici a sinistra)
                lun = len(corr_right[j].split(":")[0][1:-1].split(","))  # prendo la lunghezza della lista di indici a sinistra

                for ll in range(lun):  # per la lunghezza della lista
                    if corr_found[i].split(":")[1] == "[-1]":
                        analisi.append("FN")  # e' un falso negativo
                        i += 1  # aumento il contatore delle trovate
                    elif corr_right[j].split(":")[1] == "[-1]":
                        if corr_found[i].split(":")[2] == "[neg]":
                            analisi.append("VN")  # e' un vero negativo
                            i += 1  # aumento il contatore delle trovate
                        else:
                            analisi.append("FP")  # e' un falso positivo
                            i += 1  # aumento il contatore delle trovate
                    else:
                        if corr_found[i].split(":")[2] == "[neg]":
                            analisi.append("FN")  # e' un falso negativo
                            i += 1  # aumento il contatore delle trovate
                        else:
                            analisi.append("FP")  # e' un falso positivo
                            i += 1  # aumento il contatore delle trovate
                j += 1  # aumento il contatore delle corrette

    frasi_tot = len(corr_found)
    vp_tot = analisi.count("VP")
    vn_tot = analisi.count("VN")
    fp_tot = analisi.count("FP")
    fn_tot = analisi.count("FN")
    recall = vp_tot/(vp_tot + fn_tot)
    precision = vp_tot/(vp_tot + fp_tot)
    if recall == 0 and precision == 0:
        f1 = 0.0
    elif recall == 0:
        f1 = 2 / (1 / precision)
    elif precision == 0:
        f1 = 2 / (1 / recall)
    else:
        f1 = 2 / ((1/precision) + (1/recall))

    file = open("analysis_" + lingua + "." + enfile_name[:len(enfile_name) - 7] + ".txt", "a")
    file.write(caso + "-" + str(k) + "\n")
    file.write("\n")
    file.write("frasi_tot = " + str(frasi_tot) + "\n")
    file.write("\n")
    file.write("vp_tot = " + str(vp_tot) + "\n")
    file.write("\n")
    file.write("vn_tot = " + str(vn_tot) + "\n")
    file.write("\n")
    file.write("fp_tot = " + str(fp_tot) + "\n")
    file.write("\n")
    file.write("fn_tot = " + str(fn_tot) + "\n")
    file.write("\n")
    file.write("precision = " + str(precision) + "\n")
    file.write("\n")
    file.write("recall = " + str(recall) + "\n")
    file.write("\n")
    file.write("f1 = " + str(f1) + "\n")
    file.write("_______________________________________________________________________________________________________________________________________________\n")
    file.close()

    if enfile_name.startswith("de") and lingua == "ted":  # se e' un originale tedesco nel verso ted->ing
        f = open("list_analysis." + caso + "." + str(k) + "." + enfile_name[:len(enfile_name) - 7] + ".txt", "w")
        s = ""
        for el in analisi:
            s += el + "||"  # salvo la lista dei veri/falsi positivi/negativi, da poter usare per cercare le coreference
        f.write(s[:-2])
        f.close()

    return 1


# il metodo similarity_k_min_length prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_min_length(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)
    # file = open("casi_perc_" + enfile_name[3:len(enfile_name) - 7] + ".txt", "w")  # file che conterra' i 6 dizionari con le info sulle traduzioni di un solo testo

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco

    first = ""  # stringa che indica quale indice considerare prima quando costriusco la stringa degli indici

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            minimum = min(len(set(set_one[index_one])), len(set(set_two[j])))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

            if minimum != 0:  # per evitare errore di divisione per zero
                if common/minimum >= mean["min_length"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common/minimum, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append((common/minimum, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                minimum = min(len(set(set_one[index_one])), len(ff))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

                if minimum != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / minimum, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["min_length"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_min_length.corr.txt", "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1


# il metodo similarity_k_max_length prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_max_length(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            maximum = max(len(set(set_one[index_one])), len(set(set_two[j])))  # prendo il massimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

            if maximum != 0:  # per evitare errore di divisione per zero
                if common / maximum >= mean["max_length"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common / maximum, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append((common / maximum, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                maximum = max(len(set(set_one[index_one])), len(ff))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

                if maximum != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / maximum, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["max_length"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(
                ([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(
            c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_max_length.corr.txt",
             "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1


# il metodo similarity_k_union prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_union(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            union = len(set(set_one[index_one]).union((set(set_two[j]))))  # prendo la lunghezza dell'insieme che esce dall'unione degli insiemi

            if union != 0:  # per evitare errore di divisione per zero
                if common/union >= mean["union"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common/union, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append((common / union, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                union = len(set(set_one[index_one]).union(ff))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

                if union != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / union, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["union"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_union.corr.txt", "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1


# il metodo similarity_k_max_words prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_max_words(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco
    words_en = diz_en["words"]  # ricavo la lista del numero di parole con synset per frase inglese
    words_de = diz_de["words"]  # ricavo la lista del numero di parole con synset per frase tedesca

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta
        words_one = words_de  # considero la lista delle parole tedesche come la principale
        words_two = words_en  # considero la lista delle parole inglesi come la secondaria

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta
        words_one = words_en  # considero la lista delle parole inglesi come la principale
        words_two = words_de  # considero la lista delle parole tedesche come la secondaria

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            max_w = max(words_one[index_one], words_two[j])  # prendo il numero massimo di parole con synset tra il tedesco e l'inglese

            if max_w != 0:  # per evitare errore di divisione per zero
                if common / max_w >= mean["max_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common / max_w, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append((common / max_w, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                words_two_tot = 0
                for w in ind:
                    words_two_tot += words_two[w]
                max_w = max(words_one[index_one], words_two_tot)  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

                if max_w != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / max_w, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["max_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_max_w.corr.txt", "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1


# il metodo similarity_k_min_words prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_min_words(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)
    # file = open("casi_perc_" + enfile_name[3:len(enfile_name) - 7] + ".txt", "w")  # file che conterra' i 6 dizionari con le info sulle traduzioni di un solo testo

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco
    words_en = diz_en["words"]  # ricavo la lista del numero di parole con synset per frase inglese
    words_de = diz_de["words"]  # ricavo la lista del numero di parole con synset per frase tedesca

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta
        words_one = words_de  # considero la lista delle parole tedesche come la principale
        words_two = words_en  # considero la lista delle parole inglesi come la secondaria

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta
        words_one = words_en  # considero la lista delle parole inglesi come la principale
        words_two = words_de  # considero la lista delle parole tedesche come la secondaria

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            min_w = min(words_one[index_one], words_two[j])  # prendo il numero minimo di parole con synset tra il tedesco e l'inglese

            if min_w != 0:  # per evitare errore di divisione per zero
                if common/min_w >= mean["min_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common/min_w, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append(
                        (common / min_w, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                words_two_tot = 0
                for w in ind:
                    words_two_tot += words_two[w]
                min_w = min(words_one[index_one], words_two_tot)  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

                if min_w != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / min_w, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["min_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_min_w.corr.txt", "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1


# il metodo similarity_k_sum_words prendera' come input il testo inglese, il testo tedesco, un numero k e calcolera' la similarita' tra una frase inglese/tedesca e k frasi tedesche/inglesi
# considerando l'ultimo match trovato nelle k frasi
def similarity_k_sum_words(enfile, defile, k, lingua):
    # carico i due file che contengono le info sulle frasi del testo inglese e del testo tedesco
    enfile_name = enfile.name
    with open("sent_en_" + enfile_name[:len(enfile_name) - 4] + ".json", "r") as f:
        diz_en = json.load(f)

    defile_name = defile.name
    with open("sent_de_" + defile_name[:len(defile_name) - 4] + ".json", "r") as f:
        diz_de = json.load(f)

    # carica la media che uso come identificatore di riferimento
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)
    # file = open("casi_perc_" + enfile_name[3:len(enfile_name) - 7] + ".txt", "w")  # file che conterra' i 6 dizionari con le info sulle traduzioni di un solo testo

    list_set_en = diz_en["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per l'inglese
    list_set_de = diz_de["list_set"]  # ricavo la lista di liste dei synset dal dizionario nel file per il tedesco
    words_en = diz_en["words"]  # ricavo la lista del numero di parole con synset per frase inglese
    words_de = diz_de["words"]  # ricavo la lista del numero di parole con synset per frase tedesca

    if lingua == "ted":
        set_one = list_set_de  # considero le liste di synset tedesche una ad uno
        set_two = list_set_en  # considero le liste di synset inglesi k alla volta
        words_one = words_de  # considero la lista delle parole tedesche come la principale
        words_two = words_en  # considero la lista delle parole inglesi come la secondaria

    else:  # se e' l'inglese ad avere meno frasi
        set_one = list_set_en  # considero le liste di synset inglesi una ad uno
        set_two = list_set_de  # considero le liste di synset tedesche k alla volta
        words_one = words_en  # considero la lista delle parole inglesi come la principale
        words_two = words_de  # considero la lista delle parole tedesche come la secondaria

    index_one = 0  # indice che si spostera' di 1 ogni volta
    index_two = 0  # indice che si spostera' di 1 rispetto all'indice dell'ultimo match

    corrispondenze = []  # lista che conterra' gli indici con le corrispondenze

    while index_two < len(set_two) and index_one < len(set_one):  # finche' non arrivo all'ultimo match o all'ultima frase singola
        corr = []  # creo la lista che conterra' la coppia di valore di similarita' e l'indice
        no_corr = []
        if index_two + k <= len(set_two):  # se non sto alle ultime due frasi
            until = index_two + k  # prendo l'indice del secondo testo + k
        else:  # se sto alle ultime due frasi
            until = len(set_two)  # considero la lunghezza del testo

        for j in range(index_two, until):  # dall'indice dell'ultimo match ad until (individuato sopra)
            common = len(set(set_one[index_one]).intersection(
                set(set_two[j])))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
            sum_w = words_one[index_one] + words_two[j]  # prendo la somma delle parole inglesi e tedesche con synset

            if sum_w != 0:  # per evitare errore di divisione per zero
                if common / sum_w >= mean["sum_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    corr.append((common / sum_w, j))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se non supera la soglia
                    no_corr.append((common / sum_w, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice
            else:  # se il denominatore e' 0
                no_corr.append((0.0, set(set_two[j]), j))  # mi salvo la perc, l'insieme di synset e l'indice

        if corr:  # se la lista non e' vuota
            m = max(corr)  # prendo il massimo tra i valori
            corrispondenze.append(([m[1]], "pos"))  # e aggiungo l'indice alla lista delle corrispondenze
            index_two = m[1] + 1  # aumento l'indice con l'ultimo match + 1
            index_one += 1  # aumento di 1 quello della frase singola
        else:  # se la lista e' vuota
            #  mi creo la "permuatzione" degli indici, esempio [1,2] [2,3] [3,4] [1,2,3] [2,3,4] [1,2,3,4]
            index = 0
            s = []
            if len(no_corr) > 2:  # solo se ho almeno 3 indici
                kk = len(no_corr)
                for m in range(0, kk + 1):
                    for x in range(index + 1, index + m):
                        l = []
                        for b in range(x, m + 1):
                            l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
                        s.append(l)
            else:  # senno' basta prendere la lista che ho gia'
                s = [no_corr]

            other_corr = []  # lista ce conterra' le altre corrispondenze

            for frasi in s:  # per la lista di coppie (insieme, indice) nell'insieme di frasi
                ff = set()  # inizializzo l'insieme che conterra' i synset
                ind = []
                for fr in frasi:  # per ogni coppia nella lista
                    ff = ff.union(fr[1])  # unisco l'insieme della coppia all'insieme ff
                    ind.append(fr[2])

                common = len(set(set_one[index_one]).intersection(ff))  # ricavo l'intersezione della coppia di insiemi di synset
                words_two_tot = 0
                for w in ind:
                    words_two_tot += words_two[w]
                sum_w = words_one[index_one] + words_two_tot  # prendo la somma di tutto

                if sum_w != 0:  # per evitare errore di divisione per zero
                    other_corr.append((common / sum_w, ind))  # aggiungo alla lista la coppia (valore, indice)
                else:  # se il denominatore e' 0
                    other_corr.append((0.0, ind))  # aggiungo alla lista la coppia (valore, indice)

            sup_thres = []
            for value in other_corr:  # tra tutte le percentuali
                if value[0] >= mean["sum_#_words"]:  # se il valore di similarita' e' maggiore o uguale a quello di riferimento
                    sup_thres.append(value)  # aggiungo solo quello maggiore della soglia

            if sup_thres:  # se ce n'e' almeno una
                ma = max(sup_thres)  # prendo la perc massima
                valori_uguali = []
                for v in sup_thres:  # controllo se ci sono altre frasi con la stessa perc
                    if v[0] == ma[0]:
                        valori_uguali.append(v)  # li aggiungo alla lista
                lun_list = []
                for i in valori_uguali:  # delle frasi con perc uguale
                    lun_list.append((len(i[1]), i))  # prendo la lunghezza della lista di indici
                minn = min(lun_list)  # prendo quello con lunghezza minore
                m = minn[1]  # ricavo la perc con gli indici
                corrispondenze.append((str(m[1]).replace(", ", ","), "pos"))  # e aggiungo tutti gli indici alla lista delle corrispondenze insieme a pos che indica che e' la traduzione
                index_two = max(m[1]) + 1  # aumento l'indice con il massimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola
            else:  # se non ce n'e' manco manco una che supera la soglia
                m = max(no_corr)  # prendo quella con perc massima tra le singole frasi
                corrispondenze.append(([m[2]], "neg"))  # e aggiungo l'indice alla lista delle corrispondenze insieme a neg che mi indica che non e' la traduzione
                index_two += 1  # aumento l'indice con l'ultimo match + 1
                index_one += 1  # aumento di 1 quello della frase singola

    if len(corrispondenze) < len(set_one):  # se la lista delle corrispondenze e' minore # delle frasi
        for i in range(len(set_one) - len(corrispondenze)):  # per le frasi mancanti
            corrispondenze.append(([-1], "neg"))  # aggiungo come corrispondenza -1, cioe' non ha corrispondenza, insieme a neg

    str_corr = ""  # stringa che conterra' le corrispondenze in formato [indice set_one]:[indice set_two]

    for c in corrispondenze:  # per ogni indice nella lista
        str_corr += "[" + str(corrispondenze.index(c)) + "]:" + str(c[0]) + ":[" + c[1] + "], "  # compongo la stringa
        corrispondenze[corrispondenze.index(c)] = "preso"  # sostituisco l'indice con una stringa in modo da segnare che e' gia' stato considerato

    f = open(lingua + "." + enfile_name[:len(enfile_name) - 7] + "." + str(k) + "_sum_w.corr.txt", "w")  # salvo la stringa in un file
    f.write(lingua + "\n")
    f.write(str_corr[:-2])
    f.close()

    return 1
