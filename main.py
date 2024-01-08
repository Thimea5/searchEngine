import praw
import urllib, urllib.request
import xmltodict
import pickle
import datetime
from Corpus import Corpus
from Classes import Document
from Classes import Author
from Classes import RedditDocument
from Classes import ArxivDocument

# Connexion à l'API REDDIT
reddit = praw.Reddit(client_id='k9t9Uh4CiOx2YbY1Fq1o4g', client_secret='WaaCVpa9njLgkCD1eOfwQo-OBS_sow', user_agent='td3Python')

# limite et sujet de la requête
subjct = reddit.subreddit('space')
textes_Reddit = []
docs_bruts = []

for post in subjct.hot(limit=2):
    docs_bruts.append(("Reddit", post))

# Récupération du texte
docs = []

afficher_cles = False

# Paramètres
query_terms = ["space"]
max_results = 2

# Requête ARXIV
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))

# Ajout résumés à la liste
for i, entry in enumerate(data["feed"]["entry"]):
    docs.append(entry["summary"].replace("\n", ""))
    docs_bruts.append(("ArXiv", entry))

docs = list(set(docs))

for i, doc in enumerate(docs):
    #print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<20 :
        docs.remove(doc)

longueChaineDeCaracteres = " ".join(docs)

collection = []
for nature, doc in docs_bruts:
    if nature == "ArXiv":  # Les fichiers de ArXiv ou de Reddit sont pas formatés de la même manière à ce stade.
        #showDictStruct(doc)

        titre = doc["title"].replace('\n', '')  # On enlève les retours à la ligne
        try:
            authors = ", ".join([a["name"] for a in doc["author"]])  # On fait une liste d'auteurs, séparés par une virgule
        except:
            authors = doc["author"]["name"]  # Si l'auteur est seul, pas besoin de liste

        summary = doc["summary"].replace("\n", "")  # On enlève les retours à la ligne
        date = datetime.datetime.strptime(doc["published"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d")  # Formatage de la date en année/mois/jour avec librairie datetime
    
        doc_classe = ArxivDocument(titre, authors, date, doc["id"], summary)  # Création du Document
        collection.append(doc_classe)  # Ajout du Document à la liste.

    elif nature == "Reddit":
        titre = doc.title.replace("\n", '')
        auteur = str(doc.author)
        date = datetime.datetime.fromtimestamp(doc.created).strftime("%Y/%m/%d")
        url = "https://www.reddit.com/"+doc.permalink
        texte = doc.selftext.replace("\n", "")
        nb_commentaires = doc.num_comments

        doc_classe = RedditDocument(titre, auteur, date, url, texte, nb_commentaires)
        collection.append(doc_classe)

# Création de l'index de documents
id2doc = {}
for i, doc in enumerate(collection):
    id2doc[i] = doc.titre

authors = {}
aut2id = {}
num_auteurs_vus = 0

# Création de la liste+index des Auteurs
for doc in collection:
    if doc.auteur not in aut2id:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc.auteur)
        aut2id[doc.auteur] = num_auteurs_vus

    authors[aut2id[doc.auteur]].add(doc.texte)

corpus = Corpus("Mon corpus")

# Construction du corpus à partir des documents
for doc in collection:
    corpus.add(doc)
#corpus.show(tri="abc")



# Ouverture d'un fichier, puis écriture avec pickle
with open("corpus.pkl", "wb") as f:
    pickle.dump(corpus, f)

# Supression de la variable "corpus"
del corpus

# Ouverture du fichier, puis lecture avec pickle
with open("corpus.pkl", "rb") as f:
    corpus = pickle.load(f)

#voir le corpus
print(repr(corpus))
