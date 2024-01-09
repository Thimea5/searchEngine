# Corpus.py
from Classes import Author
from singleton import Singleton
import re
import pandas as pd

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
    
    def concordance(self, keyword, context_size=50):
        if not hasattr(self, 'full_text'):
            self.full_text = " ".join(doc.texte for doc in self.id2doc.values())

        # Utiliser la fonction finditer de re pour obtenir tous les passages contenant le mot-clé
        matches = re.finditer(fr'\b{re.escape(keyword)}\b', self.full_text, flags=re.IGNORECASE)

        # Extraire les indices des documents correspondants
        matching_doc_indices = [match.start() for match in matches]

        # Initialiser une liste pour stocker les résultats
        concordance_results = []

        # Construire la concordance pour chaque index
        for index in matching_doc_indices:
            # Extraire le contexte gauche et droit du mot-clé
            context_left = self.full_text[max(0, index - context_size):index]
            context_right = self.full_text[index + len(keyword):index + len(keyword) + context_size]

            # Ajouter le résultat à la liste
            concordance_results.append((context_left, keyword, context_right))

        # Convertir la liste en un tableau pandas pour une meilleure représentation
        columns = ['Contexte Gauche', 'Motif Trouvé', 'Contexte Droit']
        concordance_df = pd.DataFrame(concordance_results, columns=columns)

        return concordance_df