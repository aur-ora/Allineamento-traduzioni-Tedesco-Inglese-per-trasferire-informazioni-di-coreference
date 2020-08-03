import stanza
from spacy_stanza import StanzaLanguage

#stanza.download("en")
snlp = stanza.Pipeline(lang="en")
nlp = StanzaLanguage(snlp)

doc = nlp("The boy is eating an apple at school.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print(doc.ents)


