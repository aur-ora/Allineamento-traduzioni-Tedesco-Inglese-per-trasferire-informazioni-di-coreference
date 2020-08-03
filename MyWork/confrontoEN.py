import stanza
from spacy_stanza import StanzaLanguage

#Uso di stanza per ricavare da una frase i lemmi, i pos, i ner e le dep-parse

#stanza.download("en")
snlp = stanza.Pipeline(lang="en")
nlp = StanzaLanguage(snlp)

doc = nlp("The Nellie, a cruising yawl, swung to her anchor without a flutter of the sails, and was at rest.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print(doc.ents)

#Ricavare i lemmi (synset) delle parole
from nltk.corpus import wordnet as wn
lem = wn.lemmas("anchor")

print(lem)



