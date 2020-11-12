import MyWork


def main():
    # enTXT = open("de.sidd.en.txt", "r")
    # deTXT = open("de.sidd.de.txt", "r")
    # wilde_en = open("en.three.wilde.en.txt", "r")
    # wilde_de = open("en.three.wilde.de.txt", "r")
    # mann_en = open("de.three.mann.en.txt")
    # mann_de = open("de.three.mann.de.txt")
    # hesse_en = open("de.three.hesse.g.en.txt")
    # hesse_de = open("de.three.hesse.g.de.txt")
    poe_en = open("en.poe.masque.2.en.txt", "r")
    poe_de = open("en.poe.masque.2.de.txt", "r")
    juenger_en = open("de.juenger.marmor.2.en.txt", "r")
    juenger_de = open("de.juenger.marmor.2.de.txt", "r")
    hesse_en = open("de.hesse.siddhartha.2.en.txt", "r")
    hesse_de = open("de.hesse.siddhartha.2.de.txt", "r")
    conrad_en = open("en.conrad.darkness.2.en.txt", "r")
    conrad_de = open("en.conrad.darkness.2.de.txt", "r")
    zweig_en = open("de.zweig.herzens.2.en.txt", "r")
    zweig_de = open("de.zweig.herzens.2.de.txt", "r")
    stevenson_en = open("en.stevenson.treasure.2.en.txt", "r")
    stevenson_de = open("en.stevenson.treasure.2.de.txt", "r")
    one = open("one.other.txt", "r")
    ein = open("ein.txt", "r")
    right_en = open("sent_perc_en.txt", "r")  # file che contiene le frasi inglesi
    right_de = open("sent_perc_de.txt", "r")  # file che contiene le frasi tedesche con traduzione corrispondente
    wrong_en = open("wrong_sent_perc_en.txt", "r")  # file che contiene le frasi inglesi (in posizione diverse rispetto a right_en)
    wrong_de = open("wrong_sent_perc_de.txt", "r")  # file che cotiene le frasi tedesche senza traduzione corrispondente

    # print(MyWork.media_pond())
    # print(MyWork.media_arit())

    # no_corr = [(0.0, ['bn:05577941n', 'bn:00086611v', 'bn:00025583n', 'bn:00025582n', 'bn:00035909n', 'bn:00088918v', 'bn:00035908n', 'bn:00095597v', 'bn:00087905v', 'bn:00040328n', 'bn:00088913v', 'bn:00088963v', 'bn:03692700n', 'bn:00088914v', 'bn:00098581a', 'bn:00086600v', 'bn:13766567a', 'bn:00088912v', 'bn:00025587n', 'bn:00025584n', 'bn:14481633n', 'bn:00077459n', 'bn:00086557v', 'bn:00085839v', 'bn:00085363v', 'bn:00087845v', 'bn:00041800n', 'bn:03121908n', 'bn:00537938n', 'bn:00088629v', 'bn:00085715v', 'bn:00036188n', 'bn:00025585n', 'bn:00083293v'], 78), (0.0, ['bn:00098594a', 'bn:00005871n', 'bn:05439421n', 'bn:00013389n', 'bn:00032620n', 'bn:00032601n', 'bn:00032607n', 'bn:00080108n', 'bn:03361486n', 'bn:00023151n', 'bn:00098887a', 'bn:00032600n', 'bn:00019035n', 'bn:00007046n', 'bn:00079878n'], 79)]
    #
    # k = 3
    # index = 0
    # s = []
    # for m in range(0, k + 1):
    #     for x in range(index + 1, index + m):
    #         l = []
    #         for b in range(x, m + 1):
    #             l.append(no_corr[b - 1])  # aggiungo la coppia (insieme, indice) nella lista
    #         s.append(l)
    # print(s)
    # print(MyWork.transform_in_file(one, ein))
    # print(MyWork.transform_in_file(right_en, right_de))
    # print(MyWork.transform_in_file(wrong_en, wrong_de))
    # print(MyWork.transform_in_file(poe_en, poe_de))
    # print(MyWork.transform_in_file(hesse_en, hesse_de))
    # print(MyWork.transform_in_file(juenger_en, juenger_de))
    # print(MyWork.transform_in_file(conrad_en, conrad_de))
    # print(MyWork.transform_in_file(zweig_en, zweig_de))
    # print(MyWork.transform_in_file(stevenson_en, stevenson_de))

    # print(MyWork.same_sentence(hesse_en, hesse_de))

    # print(MyWork.auto_analysis(poe_en, "min_length", 3))
    '''
    Devo runnare similarity_k_caso per tutti i casi, per tutti i testi, e k = 1, 3, 5
    Poi, devo runnare auto_analysis per le stesse volte
    '''
    # K = 1, 3, 5 e CASO = min_length
    for k in [1, 3, 5]:
        for lingua in ["ted", "ing"]:
            print(MyWork.similarity_k_min_length(conrad_en, conrad_de, k, lingua))
            print(MyWork.similarity_k_min_length(poe_en, poe_de, k, lingua))
            print(MyWork.similarity_k_min_length(stevenson_en, stevenson_de, k, lingua))
            print(MyWork.similarity_k_min_length(hesse_en, hesse_de, k, lingua))
            print(MyWork.similarity_k_min_length(juenger_en, juenger_de, k, lingua))
            print(MyWork.similarity_k_min_length(zweig_en, zweig_de, k, lingua))
    print("DONE min_length")
    ###############################################################################

    # # K = 1, 3, 5  e CASO = max_length
    # for k in [1, 3, 5]:
        # for lingua in ["ted", "ing"]:
        #     print(MyWork.similarity_k_max_length(conrad_en, conrad_de, k, lingua))
        #     print(MyWork.similarity_k_max_length(poe_en, poe_de, k, lingua))
        #     print(MyWork.similarity_k_max_length(stevenson_en, stevenson_de, k, lingua))
        #     print(MyWork.similarity_k_max_length(hesse_en, hesse_de, k, lingua))
        #     print(MyWork.similarity_k_max_length(juenger_en, juenger_de, k, lingua))
        #     print(MyWork.similarity_k_max_length(zweig_en, zweig_de, k, lingua))
    # print("DONE max_length")
    # ###############################################################################
    #
    # # K = 1, 3, 5 e CASO = union
    # for k in [1, 3, 5]:
        # for lingua in ["ted", "ing"]:
        #     print(MyWork.similarity_k_union(conrad_en, conrad_de, k, lingua))
        #     print(MyWork.similarity_k_union(poe_en, poe_de, k, lingua))
        #     print(MyWork.similarity_k_union(stevenson_en, stevenson_de, k, lingua))
        #     print(MyWork.similarity_k_union(hesse_en, hesse_de, k, lingua))
        #     print(MyWork.similarity_k_union(juenger_en, juenger_de, k, lingua))
        #     print(MyWork.similarity_k_union(zweig_en, zweig_de, k, lingua))
    # print("DONE union")
    # ###############################################################################
    #
    # # K = 1, 3, 5 e CASO = max_w
    # for k in [1, 3, 5]:
        # for lingua in ["ted", "ing"]:
        #     print(MyWork.similarity_k_max_words(conrad_en, conrad_de, k, lingua))
        #     print(MyWork.similarity_k_max_words(poe_en, poe_de, k, lingua))
        #     print(MyWork.similarity_k_max_words(stevenson_en, stevenson_de, k, lingua))
        #     print(MyWork.similarity_k_max_words(hesse_en, hesse_de, k, lingua))
        #     print(MyWork.similarity_k_max_words(juenger_en, juenger_de, k, lingua))
        #     print(MyWork.similarity_k_max_words(zweig_en, zweig_de, k, lingua))
    # print("DONE max_words")
    # ###############################################################################
    #
    # # K = 1, 3, 5 e CASO = min_w
    # for k in [1, 3, 5]:
        # for lingua in ["ted", "ing"]:
        #     print(MyWork.similarity_k_min_words(conrad_en, conrad_de, k, lingua))
        #     print(MyWork.similarity_k_min_words(poe_en, poe_de, k, lingua))
        #     print(MyWork.similarity_k_min_words(stevenson_en, stevenson_de, k, lingua))
        #     print(MyWork.similarity_k_min_words(hesse_en, hesse_de, k, lingua))
        #     print(MyWork.similarity_k_min_words(juenger_en, juenger_de, k, lingua))
        #     print(MyWork.similarity_k_min_words(zweig_en, zweig_de, k, lingua))
    # print("DONE min_words")
    # ###############################################################################
    #
    # # K = 1, 3, 5 e CASO = sum_w
    # for k in [1, 3, 5]:
    #   for lingua in ["ted", "ing"]:
        #     print(MyWork.similarity_k_sum_words(conrad_en, conrad_de, k, lingua))
        #     print(MyWork.similarity_k_sum_words(poe_en, poe_de, k, lingua))
        #     print(MyWork.similarity_k_sum_words(stevenson_en, stevenson_de, k, lingua))
        #     print(MyWork.similarity_k_sum_words(hesse_en, hesse_de, k, lingua))
        #     print(MyWork.similarity_k_sum_words(juenger_en, juenger_de, k, lingua))
        #     print(MyWork.similarity_k_sum_words(zweig_en, zweig_de, k, lingua))
    # print("DONE sum_words")
    # ##############################################################################
    #
    # Analisi automatizzata
    # for k in [1, 3, 5]:
    #     for caso in ["min_length", "max_length", "union", "max_w", "min_w", "sum_w"]:
    #         for lingua in ["ted", "ing"]:
    #             print(MyWork.auto_analysis(conrad_en, caso, k, lingua))
    #             print(MyWork.auto_analysis(poe_en, caso, k, lingua))
    #             print(MyWork.auto_analysis(stevenson_en, caso, k, lingua))
    #             print(MyWork.auto_analysis(hesse_en, caso, k, lingua))
    #             print(MyWork.auto_analysis(juenger_en, caso, k, lingua))
    #             print(MyWork.auto_analysis(zweig_en, caso, k, lingua))
    #
    # for k in [1, 3, 5]:
    #     for caso in ["min_length", "max_length", "union", "max_w", "min_w", "sum_w"]:
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.en.conrad.darkness.2.txt", "r"), open("analysis_ted.en.conrad.darkness.2.txt", "r")))
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.en.poe.masque.2.txt", "r"), open("analysis_ted.en.poe.masque.2.txt", "r")))
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.en.stevenson.treasure.2.txt", "r"), open("analysis_ted.en.stevenson.treasure.2.txt", "r")))
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.de.hesse.siddhartha.2.txt", "r"), open("analysis_ted.de.hesse.siddhartha.2.txt", "r")))
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.de.juenger.marmor.2.txt", "r"), open("analysis_ted.de.juenger.marmor.2.txt", "r")))
    #         print(MyWork.precision_recall_f1(conrad_en, caso, k, open("analysis_ing.de.zweig.herzens.2.txt", "r"), open("analysis_ted.de.zweig.herzens.2.txt", "r")))

    # print("DONE EVERYTHING")


if __name__ == "__main__":
    main()