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

# Test sur la classe Document
print("Test sur la classe Document")
Doc = Document("Les Miserables","Victor Hugo","1862","https://Miserables","testText")

if Doc.auteur == "Victor Hugo":
    print("Test auteur : OK")
else:
    print("Test auteur : Échec")

if Doc.date == "1862":
    print("Test date : OK")
else:
    print("Test date : Échec")

if Doc.texte == "testText":
    print("Test texte : OK")
else:
    print("Test texte : Échec")

if Doc.titre == "Les Miserables":
    print("Test titre : OK")
else:
    print("Test titre : Échec")

if Doc.url == "https://Miserables":
    print("Test url : OK")
else:
    print("Test url : Échec")

# Test sur la classe Author
print("Test sur la classe Author")
author = Author("Pascal")
author.add("testProduction")

if author.name == "Pascal":
    print("Test nom auteur : Ok")
else:
    print("Test nom auteur : Échec")

if (author.ndoc == 1):
    print("Test ndoc : Ok")
else:
    print("Test ndoc : Échec")

if author.production[0] == "testProduction":
    print("Test production : OK")
else:
    print("Test production : Échec")

# Test sur la classe RedditDocument
print("Test sur la classe RedditDocument")
DocReddit = RedditDocument("Etranger","Albert Camus","1900","https://Etranger","testTextA",42)

if DocReddit.auteur == "Albert Camus":
    print("Test auteur : OK")
else:
    print("Test auteur : Échec")

if DocReddit.date == "1900":
    print("Test date : OK")
else:
    print("Test date : Échec")

if DocReddit.texte == "testTextA":
    print("Test texte : OK")
else:
    print("Test texte : Échec")

if DocReddit.titre == "Etranger":
    print("Test titre : OK")
else:
    print("Test titre : Échec")

if DocReddit.url == "https://Etranger":
    print("Test url : OK")
else:
    print("Test url : Échec")

if DocReddit.nb_commentaires == 42:
    print("Test nb_commentaires : OK")
else:
    print("Test nb_commentaires : Échec")

# Test sur la classe ArxivDocument
print("Test sur la classe ArxivDocument")
DocArxiv = ArxivDocument("Candide",["Jacques Fiot","Voltaire"],"1900","https://Candide","testTextB")

if DocArxiv.author[0] == "Jacques Fiot":
    print("Test author : OK")
else:
    print("Test author : Échec")

if DocArxiv.author[1] == "Voltaire":
    print("Test author : OK")
else:
    print("Test author : Échec")

if DocArxiv.date == "1900":
    print("Test date : OK")
else:
    print("Test date : Échec")

if DocArxiv.texte == "testTextB":
    print("Test texte : OK")
else:
    print("Test texte : Échec")

if DocArxiv.titre == "Candide":
    print("Test titre : OK")
else:
    print("Test titre : Échec")

if DocArxiv.url == "https://Candide":
    print("Test url : OK")
else:
    print("Test url : Échec")

if DocArxiv.get_authors() == ["Jacques Fiot","Voltaire"]:
    print("Test get_authors : OK")
else:
    print("Test get_authors : Échec")