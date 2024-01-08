class Document:
    # Initialisation des variables de la classe
    def __init__(self, titre="", auteur="", date="", url="", texte=""):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre : {self.titre}\tAuteur : {self.auteur}\tDate : {self.date}\tURL : {self.url}\tTexte : {self.texte}\t"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    

class Author:
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = []
        
    def add(self, production):
        self.ndoc += 1
        self.production.append(production)
    def __str__(self):
        return f"Auteur : {self.name}\t# productions : {self.ndoc}"


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

    def __init__(self, titre="", author= [], date="", url="", texte=""):
        super().__init__(titre, author, date, url, texte)
        self.author = author

    def get_authors(self):
        return self.author

    def set_authors(self, author):
        self.author = author

    def __str__(self):
        parent_str = super().__str__()
        #authors_str = ', '.join(self.author)
        return f"{parent_str}\nAuthor and co-authors : {self.author}\n"
    