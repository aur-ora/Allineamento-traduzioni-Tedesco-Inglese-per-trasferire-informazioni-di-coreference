'''
Trasformo il file con i nomi in un dizionario con i nomi e i nomignoli che sono stringhe
Prendo in input il file "NickSort.txt" che contiene solo i nomignoli con la lista dei rispettivi nomi
(Ho sistemato solo le chiavi con questo codice, per le stringhe dentro le liste ho cambiato gli apici con le virgolette, in questo
modo si poteva leggere un dizionario con json).
Per runnare:
	python stringhe2.py NickSort.txt nickfinali.txt
'''
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

f = open(inFile, "r")
p = open(outFile, "w")
fil = f.readlines()
d = {}
p.write("{")
for riga in fil:
    riga = riga.replace("\n","")
    riga = riga.split(",")
    riga = ("").join(riga)
    riga = riga.split()
    riga[len(riga)-1] = riga[len(riga)-1].replace("]","")
    chiave = riga[0][:riga[0].index(":")]
    riga[0] = riga[0][len(chiave)+2:]
    d[chiave] = riga
    p.write("\""+ chiave + "\"" +":"+ str(d[chiave]) + ",")
    d = {}
p.write("}")
f.close()
p.close()
