'''
L'ho usato per ordinare i nomignoli in ordine alfabetico
'''
import sys
inFile = sys.argv[1]
outFile = sys.argv[2]

f = open(inFile, "r")
p = open(outFile, "w")
file = f.readlines()
file = sorted(file)
for riga in file:
    	p.write(riga)
f.close()
p.close()
