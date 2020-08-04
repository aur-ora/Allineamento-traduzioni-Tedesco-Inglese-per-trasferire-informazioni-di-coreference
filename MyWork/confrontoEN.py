import stanza
from spacy_stanza import StanzaLanguage
from nltk.corpus import wordnet as wn

#Uso di stanza per ricavare da una frase i lemmi, i pos, i ner e le dep-parse

#stanza.download("en")
snlp = stanza.Pipeline("en")
nlp = StanzaLanguage(snlp)

d = {}
doc = nlp("The Nellie, a cruising yawl, swung to her anchor without a flutter of the sails, and was at rest.")
for token in doc:
    if token.pos_ not in d:
        d[token.pos_] = [token.lemma_]
    if token.pos_ in d:
        if token.lemma_ not in d[token.pos_]:
            d[token.pos_].append(token.lemma_)
    #print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print(d)



#Ricavare i lemmi (synset) delle parole
#from nltk.corpus import wordnet as wn
#lem = wn.lemmas("anchor")

#print(lem)
