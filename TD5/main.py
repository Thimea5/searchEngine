import praw
import urllib.request
import xmltodict
import datetime
import pickle
import numpy as np
from classes import Document
from classes import RedditDocument
from classes import ArxivDocument
from classes import Corpus

corpus = Corpus()

# API Reddit
reddit = praw.Reddit(client_id='wkrZkUQKt7HoqatgYvb6hw', client_secret='cHZP5DMTGEsMp6T-Aiq_9EI2-BK1Ug', user_agent='TD3_Python')
subr = reddit.subreddit('Coronavirus')

textes_Reddit = []
for post in subr.hot(limit=1):
    #texte = post.title
    #texte = texte.replace("\n", " ")
    #textes_Reddit.append(texte)
    reddit_doc = RedditDocument(titre=post.title, auteur=post.author.name, date=(datetime.datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')), url=post.url, texte=post.selftext, nb_commentaires=50)


arxiv_doc = ArxivDocument(titre="Titre Arxiv", auteur="Auteur Principal", date="2023-11-30", url="http://arxiv.org", texte="Contenu Arxiv", coauteurs=["Coauteur1", "Coauteur2", "Coauteur3"])

corpus.ajouter_document(reddit_doc)
corpus.ajouter_document(arxiv_doc)

#corpus.afficher_corpus()
