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
from factory import RedditCorpusGenerator
from factory import ArxivCorpusGenerator
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
url = f'https://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
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

# Client utilisant le générateur de corpus
def generate_corpus(generator, name):
    return generator.create_corpus(name)

#reddit_generator = RedditCorpusGenerator()
#arxiv_generator = ArxivCorpusGenerator()

#reddit_corpus = reddit_generator.create_corpus("RedditCorpus")
#arxiv_corpus = arxiv_generator.create_corpus("ArxivCorpus")

#print("voici le reddit corpus")
#print(repr(reddit_corpus))

#print("voici le arxivCorpus corpus")
#print(repr(arxiv_corpus))

#On voit donc que le singleton fonctionne correctement puisque la factory créer des instance de corpus mais il n'y en a qu'une qui est gardée

##### TD6 #####

#recherche par mot clé (donc si un docuement contient le mot clé, on le garde et on l'affiche avec la fonction search)
testSearchWord = "Fock"
resSearchWord = corpus.search(testSearchWord)

#print('resultat de la recherche du mot ' + testSearchWord)
#for doc in resSearchWord:
    #print("\n - " + repr(doc))

#recherche par concordance
testConcoWord = "Fock"
#print('\nresultat de la concordance du mot ' + testConcoWord)
concordance_result = corpus.concordance("space")
#print(concordance_result)

#partie 2
#2.1 (test de la fonction text_cleaner)
text_test = "Ceci est un exemple de texte\navec des chiffres 123 et de la ponctuation !"
texte_nettoye = corpus.text_cleaner(text_test)
#print(texte_nettoye)

#2.2 (stocker le vocabulaiee en bouclant sur les docs du corpus)
voc = corpus.build_vocabulaire()
#print(voc)

#2.3 compter les occurences de chaque mot
word_count = corpus.count_word_occurrences(voc)

dfWord = pd.DataFrame(list(word_count.items()), columns=['Mot', 'Occurrences'])
dfWord = dfWord.sort_values(by='Occurrences', ascending=False)
#print("\ndfWord  : \n")
#print(dfWord)

#2.4 
word_count_df = corpus.count_word_occurrences_with_document_frequency(voc)

# Créez un DataFrame à partir du dictionnaire de fréquence des mots
freq = pd.DataFrame(list(word_count_df.items()), columns=['Mot', 'Occurrences'])
freq = freq.sort_values(by='Occurrences', key=lambda x: x.apply(lambda y: y['term freq']), ascending=False)
#print("\nfreq : \n")
#print(freq)


##### TD7 ####
#2.1
#print('voc avec term, id et total occurences')
#print(voc)

#2.2
#ligne : doc - colonne mot donc exemple ligne 0 colonne 0 donne le nombre de fois que le mot d'index 0 dans le doc 0 apparait 
tf_matrix = corpus.build_tf_matrix(voc)
assert tf_matrix.shape[1] == len(voc), "La taille de la matrice ne correspond pas à la taille du vocabulaire"
# Afficher la matrice de term frequency
#print("Matrice de Term Frequency (TF):")
#print(tf_matrix.toarray())

#2.3 
total_occurrences = tf_matrix.sum(axis=0)

# Calculer le nombre total de documents contenant chaque mot
doc_count = (tf_matrix > 0).sum(axis=0)

vocab = dict(sorted(voc.items()))

# Attribuer des indices commençant à 0
for index, (word, info) in enumerate(vocab.items()):
    info['id'] = index

#assert min(info['id'] for info in voc.values()) == 0, "Les indices du vocabulaire ne commencent pas à 0"
# Boucle pour chaque mot de vocab
for word, info in vocab.items():
    word_id = info['id']
    info['total_occurrences'] = total_occurrences[0, word_id]
    info['doc_count'] = doc_count[0, word_id]

    #print(f"{word} : {info}")

#Rappel : vocab est un dictionnaire contenant les mots, ainsi que leur id et leur total d'occurences dans le corpus

# Accéder au mot à l'index ind dans le dictionnaire vocab
index = 6
w = next((mot for mot, info in vocab.items() if info['id'] == index), None)

