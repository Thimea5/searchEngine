# Corpus.py
from Classes import Author
from singleton import Singleton
import re

class Corpus(metaclass=Singleton):
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]].add(doc.texte)

        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

    def show(self, n_docs=-1, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":  # Tri alphabétique
            docs = list(sorted(docs, key=lambda x: x.titre.lower()))[:n_docs]
        elif tri == "123":  # Tri temporel
            docs = list(sorted(docs, key=lambda x: x.date))[:n_docs]

        print("\n".join(list(map(repr, docs))))

    def __repr__(self):
        docs = list(self.id2doc.values())
        docs = list(sorted(docs, key=lambda x: x.titre.lower()))

        return "\n".join(list(map(str, docs)))
    
    def search(self, keyword):
        matching_docs = []

        keyword_pattern = re.compile(fr'\b{re.escape(keyword)}\b', flags=re.IGNORECASE)

        for index, doc in self.id2doc.items():
            title_matches = keyword_pattern.search(doc.titre)
            text_matches = keyword_pattern.search(doc.texte)

            if title_matches or text_matches:
                matching_docs.append(doc)

        return matching_docs