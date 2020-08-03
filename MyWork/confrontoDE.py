import stanza
from spacy_stanza import StanzaLanguage

#Uso di stanza per ricavare da una frase i lemmi, i pos, i ner e le dep-parse

#stanza.download("de")
snlp = stanza.Pipeline(lang="de")
nlp = StanzaLanguage(snlp)

doc = nlp("Die Nelly, eine seetüchtige Jolle, schwoite an ihrem Anker ohne die leiseste Regung in den Segeln und hielt Rast.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print(doc.ents)

#Ricavare i lemmi (synset) delle parole --> i lemmi saranno in inglese anche se l'input è tedesco
#così si possono confrontare
from nltk.corpus import wordnet as wn
lem = wn.lemmas("Anker", lang="deu")
print(lem)
