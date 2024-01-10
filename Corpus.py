# Corpus.py
from Classes import Author
from singleton import Singleton
import re
import pandas as pd
from scipy.sparse import csr_matrix

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

        matches = re.finditer(fr'\b{re.escape(keyword)}\b', self.full_text, flags=re.IGNORECASE)
        # prendre les indices
        matching_doc_indices = [match.start() for match in matches]
        concordance_results = []
        for index in matching_doc_indices:
            # prendre le contexte gauche et droit du mot-clé
            context_left = self.full_text[max(0, index - context_size):index]
            context_right = self.full_text[index + len(keyword):index + len(keyword) + context_size]
            concordance_results.append((context_left, keyword, context_right))
        columns = ['Contexte Gauche', 'Motif Trouvé', 'Contexte Droit']
        concordance_df = pd.DataFrame(concordance_results, columns=columns)

        return concordance_df
    
    def text_cleaner(self, texte):
        texte = texte.lower()
        texte = texte.replace("\n", " ") 
        texte = re.sub(r'[^\w\s]', '', texte) #supprimer la ponctuation
        texte = re.sub(r'\d', '', texte) #chiffre

        return texte
    
    #td6
    def build_vocabulaire(self):
        #maj pour le td7
        vocab = {}
        for doc in self.id2doc.values():
            text = self.text_cleaner(doc.texte)
            words = text.split()
            cleaned_words = [self.text_cleaner(word) for word in words]

            word_counts = {}
            for word in cleaned_words:
                if word not in word_counts:
                    word_counts[word] = 1
                else:
                    word_counts[word] += 1

            for word, count in word_counts.items():
                if word not in vocab:
                    vocab[word] = {
                        'id': len(vocab) + 1,  # Identifiant unique, commence à 1
                        'total_occurrences': count
                    }
                else:
                    vocab[word]['total_occurrences'] += count

        # Trier le dictionnaire par ordre alphabétique des mots
        vocab = dict(sorted(vocab.items()))

        return vocab

    #td6 2.3
    def count_word_occurrences(self, vocabulary):
        word_counts = {word: 0 for word in vocabulary}
        for doc in self.id2doc.values():
            words = doc.texte.split()
            cleaned_words = [self.text_cleaner(word) for word in words]
            for word in cleaned_words:
                if word in word_counts:
                    word_counts[word] += 1
        return word_counts


    #2.4
    def count_word_occurrences_with_document_frequency(self, vocabulary):
        word_counts = {word: {'term freq': 0, 'document freq': 0} for word in vocabulary}
        for doc in self.id2doc.values():
            words = doc.texte.split()
            cleaned_words = [self.text_cleaner(word) for word in words]
            for word in set(cleaned_words):  # Utilisez un ensemble pour éviter de compter plusieurs fois le même mot dans un même document
                if word in word_counts:
                    word_counts[word]['term freq'] += cleaned_words.count(word)  # Utilisez cleaned_words au lieu de words
                    word_counts[word]['document freq'] += 1
        return word_counts
    
    def build_tf_matrix(self, vocabulary):
        data = []
        col_indices = []
        row_indices = []

        for doc_id, doc in self.id2doc.items():
            cleaned_text = self.text_cleaner(doc.texte)
            word_counts = {word: cleaned_text.split().count(word) for word in vocabulary if word in cleaned_text.split()}

            for word, count in word_counts.items():
                if word in vocabulary:
                    col_index = vocabulary[word]['id'] - 1  # Ajuster l'indice à 0
                    #print(f"Word: {word}, Column Index: {col_index}")
                    if 0 <= col_index < len(vocabulary):
                        data.append(count)
                        col_indices.append(col_index)
                        row_indices.append(doc_id - 1)  # Soustraire 1 pour ajuster l'indice de ligne
                    #else:
                        #print(f"Invalid column index {col_index} for word {word}")
                #else:
                    #print(f"Word '{word}' not found in the vocabulary.")

        #print(f" row : {len(row_indices)}")
        #print(f" col : {len(col_indices)}")
        #print(f" vocabulary r  : {len(vocabulary)}")
        #print(f" id2doc c: {len(self.id2doc)}")

        tf_matrix = csr_matrix((data, (row_indices, col_indices)), shape=(len(self.id2doc), len(vocabulary)))
        return tf_matrix