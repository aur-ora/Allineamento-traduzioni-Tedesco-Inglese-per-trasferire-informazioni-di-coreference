import stanza
from spacy_stanza import StanzaLanguage
from nltk.corpus import wordnet as wn
from nltk import Tree
from nltk.tree import ParentedTree

#Uso di stanza per ricavare da una frase i lemmi, i pos, i ner e le dep-parse

#stanza.download("en")
snlp = stanza.Pipeline("en")
nlp = StanzaLanguage(snlp)

parser = []
d = {}
synsets = []
doc = nlp("The Nellie, a cruising yawl, swung to her anchor without a flutter of the sails, and was at rest.")
for token in doc:
    #Creo il dizionario dei POS tag
    if token.pos_ not in d:
        d[token.pos_] = [token.lemma_]
    if token.pos_ in d:
        if token.lemma_ not in d[token.pos_]:
            d[token.pos_].append(token.lemma_)
    #Ricavo i synset dei lemmi
    synsets += ([wn.lemmas(token.lemma_)])
    #Creo la lista delle relazioni del dep parsing
    parser.append(token.dep_)
    #print(token.text, token.lemma_, token.pos_, token.dep_, token.ent_type_)
print("POS Matches: " + str(d))
print("Dep Parser relations: " + str(parser))
print("Synsets --> " + str(synsets))
#Serve per ricavare l'albero delle depencency
'''def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
'''
#Stampa l'albero su video
#[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

def tok_format(tok):
    return "_".join([tok.orth_, tok.dep_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return ParentedTree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]
