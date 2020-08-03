'''
Trasformo il file con i nomi in un dizionario con i nomi che sono stringhe
C'è la versione più giusta --> stringhe2.py
'''
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

f = open(inFile, "r")
p = open(outFile, "w")
fil = f.readlines()
d = {}
for riga in fil:
	riga = riga.replace("\n","")
	riga = riga.split(",")
	riga = ("").join(riga)
	riga = riga.split()
	riga[len(riga)-1] = riga[len(riga)-1].replace("]","")
	chiave = riga[0][:riga[0].index(":")]
	riga[0] = riga[0][len(chiave)+2:]
	d[chiave] = riga

p.write(str(d))
f.close()
p.close()
