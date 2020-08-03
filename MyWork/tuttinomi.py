'''
Programma che mi aggiunge le tabelle nome -> nomignoli oltre a quelle nomignolo -> nomi
Prende in input il file "nickfinali.json" che contiene il dizionario dei nomignoli e mi
restituisce il file "nomiGnoli.txt" in cui ci sono anche i nomi
Per runnare:
	python tuttinomi.py nickfinali.json nomiGnoli.txt
'''
import json
import sys

inFile = sys.argv[1]
outFile = sys.argv[2]

nomiGnoli = {}

with open(inFile, "r") as f:
	f_dict = json.load(f)
for chiave in f_dict:
	if chiave in nomiGnoli:
		for elemento in f_dict[chiave]:
			nomiGnoli[chiave].append(elemento)
			if elemento in nomiGnoli:
				nomiGnoli[elemento].append(chiave)
			else:
				nomiGnoli[elemento] = [chiave]
	else:
		nomiGnoli[chiave] = f_dict[chiave]
		for elemento in f_dict[chiave]:
			if elemento in nomiGnoli:
				nomiGnoli[elemento].append(chiave)
			else:
				nomiGnoli[elemento] = [chiave]

with open(outFile, 'w') as json_file:
  json.dump(nomiGnoli, json_file)



