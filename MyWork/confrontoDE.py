import stanza
from spacy_stanza import StanzaLanguage
from nltk.corpus import wordnet as wn
from nltk.tree import ParentedTree

#Uso di stanza per ricavare da una frase i lemmi, i pos, i ner e le dep-parse

#stanza.download("de")
snlp = stanza.Pipeline(lang="de")
nlp = StanzaLanguage(snlp)

parser = []
d = {}
synsets = []
doc = nlp("Die Nelly, eine seetüchtige Jolle, schwoite an ihrem Anker ohne die leiseste Regung in den Segeln und hielt Rast.")
for token in doc:
    #Creo il dizionario dei POS tag
    if token.pos_ not in d:
        d[token.pos_] = [token.lemma_]
    if token.pos_ in d:
        if token.lemma_ not in d[token.pos_]:
            d[token.pos_].append(token.lemma_)
    #Ricavo i synset dei lemma che sono NOUN (sostantivi)
    synsets += ([wn.lemmas(token.lemma_, lang="deu")])
    #Creo la lista delle relazioni del dep parsing
    parser.append(token.dep_)
    #print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print("POS Matches: " + str(d))
print("Dep Parser relations: " + str(parser))
print("Synsets --> " + str(synsets))

def tok_format(tok):
    return "_".join([tok.orth_, tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return ParentedTree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]