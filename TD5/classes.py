class Document:

    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte


class RedditDocument(Document):

    def __init__(self, titre="", auteur="", date="", url="", texte="", nb_commentaires=0):
        super().__init__(titre, auteur, date, url, texte)
        self.nb_commentaires = nb_commentaires

    def get_nb_commentaires(self):
        return self.nb_commentaires

    def set_nb_commentaires(self, nb_commentaires):
        self.nb_commentaires = nb_commentaires

    def __str__(self):
        parent_str = super().__str__()
        return f"{parent_str}\nNombre de commentaires : {self.nb_commentaires}"
    

class ArxivDocument(Document):

    def __init__(self, titre="", auteur="", date="", url="", texte="", coauteurs=[]):
        super().__init__(titre, auteur, date, url, texte)
        self.coauteurs = coauteurs

    def get_coauteurs(self):
        return self.coauteurs

    def set_coauteurs(self, coauteurs):
        self.coauteurs = coauteurs

    def __str__(self):
        parent_str = super().__str__()
        coauteurs_str = ', '.join(self.coauteurs)
        return f"{parent_str}\nCo-auteurs : {coauteurs_str}"


class Corpus:
    def __init__(self):
        self.documents = []

    def ajouter_document(self, document):
        self.documents.append(document)

    def afficher_corpus(self):
        for document in self.documents:
            print(document)