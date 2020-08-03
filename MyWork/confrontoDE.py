import stanza
from spacy_stanza import StanzaLanguage

#stanza.download("de")
snlp = stanza.Pipeline(lang="de")
nlp = StanzaLanguage(snlp)

doc = nlp("Der Junge isst in der Schule einen Apfel.")
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print(doc.ents)