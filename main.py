#################### TD 3 ####################

#import
import praw
import xmltodict
import urllib.request
import numpy as np    
import pandas as pd

#Partie 1
docs = [] #Liste qui ne contiendra que des documents

textes_Arxiv = []
textes_reddit = []

#Connexion à l'API reddit
reddit = praw.Reddit(client_id='k9t9Uh4CiOx2YbY1Fq1o4g', client_secret='WaaCVpa9njLgkCD1eOfwQo-OBS_sow', user_agent='td3Python')

#Sujet de la recherche
subj = reddit.subreddit('Space')

#Alimenter la liste docs avec essentiellement le champs texte avec REDDIT
for post in subj.hot(limit=100):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_reddit.append(texte)

#Connexion à l'API Arxiv
query = "Space"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

#décoder le "byte stream" url_read
data = url_read.decode()

#obtenir un obj json avec xmltodict
dico = xmltodict.parse(data)
docs = dico['feed']['entry']


for d in docs:
    texte = d['title']+ ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)

# on concatène (ajout des textes reddit et des textes arxiv):
    
corpus = textes_reddit + textes_Arxiv

#print("Corpus length: %d" % len(corpus))
print("Longueur du corpus : " + str(len(corpus)))


#Partie 2

# 2.1 Créer un tableau de type DataFrame avec pandas
data = {'ID': range(1, len(corpus) + 1),
        'Texte': corpus,
        'Origine': ['reddit'] * len(textes_reddit) + ['arxiv'] * len(textes_Arxiv)}

df = pd.DataFrame(data)

# 2.2 Sauvegarder le tableau sur le disque en tant que fichier CSV avec séparateur de tabulation
csv_path = 'corpus_data.csv'
df.to_csv(csv_path, sep='\t', index=False)

# 2.3 Charger le tableau directement en mémoire à partir du fichier CSV
loaded_df = pd.read_csv('corpus_data.csv', sep='\t')


#Partie 3
#1
#print("Corpus length: %d" % len(corpus))
print("Longueur du corpus : " + str(len(corpus)))


for doc in corpus:
    # nombre de phrases
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))
