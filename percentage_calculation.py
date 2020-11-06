from .alignment_BabelNet import create_set_en, create_set_de
import json
import copy


# calcolare la similarita' per calcolare la percentuali per i 6 casi definiti (lo uso per avere le percentuali di riferimento)
def calculate_percentage(enfile, defile):
    sent_en, list_set_en, tok_en, words_en = create_set_en(enfile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de, tok_de, words_de = create_set_de(defile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase tedesca

    min_length = []  # lista che contiene tutte le percentuali per il caso 1
    max_length = []  # lista che contiene tutte le percentuali per il caso 2
    union_set = []  # lista che contiene tutte le percentuali per il caso 3
    max_w = []   # lista che contiene tutte le percentuali per il caso 4
    min_w = []   # lista che contiene tutte le percentuali per il caso 5
    sum_w = []   # lista che contiene tutte le percentuali per il caso 6

    # Caso 1 -> denominatore come minimo di lunghezza dei due insiemi di synset
    for i in range(min(len(list_set_de), len(list_set_en))):  # prendo le frasi attraverso gli indici della lista
        common = len(list_set_en[i].intersection(list_set_de[i]))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimum = min(len(list_set_de[i]), len(list_set_en[i]))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

        if minimum != 0:
            min_length.append(common/minimum)
        else:
            min_length.append(0.0)

    # Caso 2 -> denominatore come massimo di lunghezza dei due insiemi di synset
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        maximum = max(len(list_set_en[i]), len(list_set_de[i]))

        if maximum != 0:
            max_length.append(common/maximum)
        else:
            max_length.append(0.0)

    # Caso 3 -> denominatore come unione dei due insiemi
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        union = len(list_set_en[i].union(list_set_de[i]))

        if union != 0:
            union_set.append(common/union)
        else:
            union_set.append(0.0)

    # Caso 4 -> denominatore come massimo tra il numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        max_words = max(words_en[i], words_de[i])

        if max_words != 0:
            max_w.append(common/max_words)
        else:
            max_w.append(0.0)

    # Caso 5 -> denominatore come minimo tra il numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        min_words = min(words_en[i], words_de[i])

        if min_words != 0:
            min_w.append(common/min_words)
        else:
            min_w.append(0.0)

    # Caso 6 -> denominatore come somma di numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        sum_words = words_en[i] + words_de[i]

        if sum_words != 0:
            sum_w.append(common/sum_words)
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

    print("min_length")
    print(min_length)
    print("max_length")
    print(max_length)
    print("union_set")
    print(union_set)
    print("min_w")
    print(min_w)
    print("max_w")
    print(max_w)
    print("sum_w")
    print(sum_w)

    return perc_case


# calcolo la media sia per il caso in cui le frasi sono traduzioni e il caso in cui non lo sono per tutti e sei i casi e salvare le medie in un dizionario
def media():
    right_en = open("sent_perc_en.txt", "r")  # file che contiene le frasi inglesi
    right_de = open("sent_perc_de.txt", "r")  # file che contiene le frasi tedesche con traduzione corrispondente
    wrong_en = open("wrong_sent_perc_en.txt", "r")  # file che contiene le frasi inglesi (in posizione diverse rispetto a right_en)
    wrong_de = open("wrong_sent_perc_de.txt", "r")  # file che cotiene le frasi tedesche senza traduzione corrispondente
    right_perc_case = calculate_percentage(right_en, right_de)
    wrong_perc_case = calculate_percentage(wrong_en, wrong_de)

    mean = {}  # dizionario che contiene la media delle due medie (traduzione giusta e sbagliata) per ciascuno dei 6 casi

    for type_cal_perc in right_perc_case:
        mean[type_cal_perc] = (right_perc_case[type_cal_perc] + wrong_perc_case[type_cal_perc]) / 2  # Media tra percentuali tra frasi con trad giusta e sbagliata

    with open('media_casi.json', 'w') as fp:
        json.dump(mean, fp)

    return 1


# il metodo similarity_k_min_length calcola la similarita' tra le frasi inglesi e tedesche, in cui se e' un originale tedesco confronta una frase tedesca con k inglesi e prende quelle con percentuale maggiore
# della percentuale di riferimento e tra questi prende il maggiore, stessa cosa se la percentuale e' minore, viceversa per gli originali inglesi, una frase inglese e k tedesche, pero' solo per il primo caso
# in cui come denominatore prendo il minimo di lunghezza tra gli insiemi di synset
def similarity_k_min_length(enfile, defile, k):
    sent_en, list_set_en, tok_en, words_en = create_set_en(enfile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de, tok_de, words_de = create_set_de(defile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase tedesca)
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)
    enfile_name = enfile.name
    file = open("casi_perc_k" + str(k) + "_" + enfile_name[3:len(enfile_name) - 7] + ".txt", "w")  # file che conterra' i 6 dizionari con le info sulle traduzioni di un solo testo

    d_1 = {"TRAD": {}, "NO_TRAD": {}}
    if str(enfile.name).startswith("de"):  # se e' un originale tedesco
        print("de")
        set_one = list_set_de  # considero le frasi tedesche una ad uno
        set_two = list_set_en  # considero le frasi inglesi k alla volta
        list_one = sent_de
        list_two = sent_en
    else:  # se e' un originale inglese
        print("en")
        set_one = list_set_en  # considero le frasi inglesi una ad uno
        set_two = list_set_de  # considero le frasi tedesche k alla volta
        list_one = sent_en
        list_two = sent_de

    for i in range(len(set_one)):  # per l'indice nella lista di frasi
        if i < len(set_two) - 2:  # se non sto alle ultime due frasi
            if i + k > len(set_two):  # se indice + k (numero di frasi da considerare) e' maggiore della lunghezza della lista da cui prendo le k frasi
                till = len(set_two)  # allora il limite del range e' la lunghezza della lista
            else:  # se indice + k e' minore della lunghezza della lista
                till = i + k  # allora considera i + k
        else:  # se invece sto alle ultime due frasi
            till = len(set_two)

        d_1["TRAD"][i] = []

        d_1["NO_TRAD"][i] = []

        for j in range(i, till):  # da i (indice della frase singola) a i + k oppure len(set_two)
            common = len(set_one[i].intersection(set_two[j]))  # numeratore = intersezione tra gli insiemi di synset della frase inglese e tedesca
            minimum = min(len(set_one[i]), len(set_two[j]))  # denominatore = lunghezza minimo tra questi due insiemi

            if minimum != 0:  # se il denominatore non e' uguale a 0 (evitare errore di divisione per zero)
                div = common / minimum
                if div >= mean["min_length"]:
                    d_1["TRAD"][i].append(str(j) + " - " + str(list_two[j]))

                else:
                    d_1["NO_TRAD"][i].append(str(j) + " - " + str(list_two[j]))

            else:  # senno'
                d_1["NO_TRAD"][i].append(str(j) + " - " + str(list_two[j]))

    file.write(str(len(sent_en)) + " FRASI INGLESI E " + str(len(sent_de)) + " FRASI TEDESCHE" + "\n")
    file.write("\n")
    file.write("CASO 1 - minimo tra lunghezze di insiemi di synset \n")
    for key in d_1:
        file.write(str(key) + "\n")
        for kk in d_1[key]:
            file.write(str(kk) + " - " + str(list_one[kk]) + "\n")
            file.write("\n")
            for value in d_1[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")

            file.write("______________________________________________________________________________________________________________________________________________________________\n")
        file.write("\n")
    file.write("\n")
    file.write("\n")

    # ind_sent = []
    #
    # indici = list(range(len(list_set_de)))  # ho la lista degli indici delle frasi della lista da cui prendiamo k frasi
    # print(indici)
    # for i in range(len(list_set_en)):  # per ogni frase nella lista da cui prendiamo solo una frase
    #     min_length = []  # lista di coppie (percentuale, indice frase)
    #     print("i -- " + str(i))
    #     for j in range(k):  # per i k elementi
    #         if j >= len(indici):
    #             break
    #         print("j -- " + str(j))
    #         print("indici[j] -- " + str(indici[j]))
    #         common = len(list_set_en[i].intersection(list_set_de[indici[j]]))  # numeratore = intersezione tra gli insiemi di synset della frase inglese e tedesca
    #         minimum = min(len(list_set_en[i]), len(list_set_de[indici[j]]))  # denominatore = lunghezza minimo tra questi due insiemi
    #
    #         if minimum != 0:  # se il denominatore non e' uguale a 0 (evitare errore di divisione per zero)
    #             div = common / minimum
    #             if div >= mean["min_length"]:
    #                 d_1["TRAD"].append(([i, sent_en[i], indici[j]], sent_de[indici[j]] ))
    #                 min_length.append((div, indici[j], True))
    #             else:
    #                 d_1["NO_TRAD"][i] = [sent_en[i], sent_de[indici[j]]]
    #                 min_length.append((div, indici[j], False))  # mi salvo nella lista la coppia di divisione tra numeratore e denomintore (la percentuale) e l'indice di una delle k frasi
    #
    #         else:  # senno'
    #             d_1["NO_TRAD"][i] = [sent_en[i], sent_de[indici[j]]]
    #             min_length.append((0.0, indici[j], False))  # mi salvo la coppia ma la divisione e' 0.0
    #
    #     print("min_length -- " + str(min_length))
    #
    #     s = max(min_length)
    #
    #     print("s prima -- " + str(s))

        # for t in range(k):
        #     if s[1] not in ind_sent:
        #         ind_sent.append(s[1])
        #         break
        #     else:
        #         min_length.remove(s)
        #         if len(min_length) != 0:
        #             s = max(min_length)
        # print("s dopo -- " + str(s))
        # indici.remove(s[1])

    return 1


#  mi salvo in un dizionario le info sulle traduzioni, quali indici (frasi) lo sono e quali non, per tutti e sei i casi
def similarity(enfile, defile):
    sent_en, list_set_en, tok_en, words_en = create_set_en(enfile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase inglese
    sent_de, list_set_de, tok_de, words_de = create_set_de(defile)  # prendo la lista di frasi e la lista degli insiemi dei synset di ciascuna frase tedesca)
    enfile_name = enfile.name
    with open("media_casi_arit.json", "r") as f:
        mean = json.load(f)
    file = open("casi_perc_" + enfile_name[3:len(enfile_name) - 7] + ".txt", "w")  # file che conterra' i 6 dizionari con le info sulle traduzioni di un solo testo

    # dizionario per ciascun caso, che ha come chiave la stringa che indica se e' traduzione o no
    # e come valore un altro dizionario che avra' come chiave l'indice delle frasi e come valore la lista delle due frasi
    d_1 = {"TRAD": {}, "NO_TRAD": {}}
    d_2 = {"TRAD": {}, "NO_TRAD": {}}
    d_3 = {"TRAD": {}, "NO_TRAD": {}}
    d_4 = {"TRAD": {}, "NO_TRAD": {}}
    d_5 = {"TRAD": {}, "NO_TRAD": {}}
    d_6 = {"TRAD": {}, "NO_TRAD": {}}

    # Caso 1 -> denominatore come minimo di lunghezza dei due insiemi di synset
    for i in range(min(len(list_set_de), len(list_set_en))):  # prendo le frasi attraverso gli indici della lista
        common = len(list_set_en[i].intersection(list_set_de[i]))  # ricavo l'intersezione della coppia di insiemi di synset (inglese e tedesco)
        minimum = min(len(list_set_de[i]), len(list_set_en[i]))  # prendo il minimo di lunghezza tra l'insieme dei synset inglesi e tedeschi

        if minimum != 0:
            if common/minimum >= mean["min_length"]:
                d_1["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_1["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_1["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Caso 2 -> denominatore come massimo di lunghezza dei due insiemi di synset
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        maximum = max(len(list_set_en[i]), len(list_set_de[i]))

        if maximum != 0:
            if common/maximum >= mean["max_length"]:
                d_2["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_2["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_2["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Caso 3 -> denominatore come unione dei due insiemi
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        union = len(list_set_en[i].union(list_set_de[i]))

        if union != 0:
            if common/union >= mean["union"]:
                d_3["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_3["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_3["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Caso 4 -> denominatore come massimo tra il numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        max_words = max(words_en[i], words_de[i])

        if max_words != 0:
            if common/max_words >= mean["max_#_words"]:
                d_4["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_4["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_4["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Caso 5 -> denominatore come minimo tra il numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        min_words = min(words_en[i], words_de[i])

        if min_words != 0:
            if common/min_words >= mean["min_#_words"]:
                d_5["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_5["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_5["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Caso 6 -> denominatore come somma di numero di parole inglesi e tedesche
    for i in range(min(len(list_set_en), len(list_set_de))):
        common = len(list_set_en[i].intersection(list_set_de[i]))
        sum_words = words_en[i] + words_de[i]

        if sum_words != 0:
            if common/sum_words >= mean["sum_#_words"]:
                d_6["TRAD"][i] = [sent_en[i], sent_de[i]]
            else:
                d_6["NO_TRAD"][i] = [sent_en[i], sent_de[i]]
        else:
            d_6["NO_TRAD"][i] = [sent_en[i], sent_de[i]]

    # Per salvare le info in un file
    file.write(str(len(sent_en)) + " FRASI INGLESI E " + str(len(sent_de)) + " FRASI TEDESCHE" + "\n")
    file.write("\n")
    file.write("CASO 1 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_1["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_1["NO_TRAD"].values())) + "\n")
    for key in d_1:
        file.write(str(key) + "\n")
        for kk in d_1[key]:
            file.write(str(kk) + ":\n")
            for value in d_1[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")
    file.write("\n")
    file.write("\n")

    file.write("CASO 2 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_2["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_2["NO_TRAD"].values())) + "\n")
    for key in d_2:
        file.write(str(key) + "\n")
        for kk in d_2[key]:
            file.write(str(kk) + ":\n")
            for value in d_2[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")
    file.write("\n")
    file.write("\n")

    file.write("CASO 3 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_3["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_3["NO_TRAD"].values())) + "\n")
    for key in d_3:
        file.write(str(key) + "\n")
        for kk in d_3[key]:
            file.write(str(kk) + ":\n")
            for value in d_3[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")
    file.write("\n")
    file.write("\n")

    file.write("CASO 4 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_4["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_4["NO_TRAD"].values())) + "\n")
    for key in d_4:
        file.write(str(key) + "\n")
        for kk in d_4[key]:
            file.write(str(kk) + ":\n")
            for value in d_4[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")
    file.write("\n")
    file.write("\n")

    file.write("CASO 5 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_5["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_5["NO_TRAD"].values())) + "\n")
    for key in d_5:
        file.write(str(key) + "\n")
        for kk in d_5[key]:
            file.write(str(kk) + ":\n")
            for value in d_5[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")
    file.write("\n")
    file.write("\n")

    file.write("CASO 6 --> " + "# FRASI CHE SONO TRADUZIONE = " + str(len(d_6["TRAD"].values())) + " # FRASI CHE NON SONO TRADUZIONE = " + str(len(d_6["NO_TRAD"].values())) + "\n")
    for key in d_6:
        file.write(str(key) + "\n")
        for kk in d_6[key]:
            file.write(str(kk) + ":\n")
            for value in d_6[key][kk]:
                file.write(str(value) + "\n")
                file.write("\n")

    file.close()

    return 1

