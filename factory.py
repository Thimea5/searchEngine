#factory
from abc import ABC, abstractmethod
from Corpus import Corpus


# Classe abstraite du générateur de corpus
class CorpusGenerator(ABC):
    @abstractmethod
    def create_corpus(self, name):
        pass

# Implémentation concrète du générateur de corpus pour Reddit
class RedditCorpusGenerator(CorpusGenerator):
    def create_corpus(self, name):
        # Logique spécifique pour créer un corpus Reddit
        corpus = Corpus(name)
        # Ajoutez des documents Reddit spécifiques
        # ...

        return corpus

# Implémentation concrète du générateur de corpus pour ArXiv
class ArxivCorpusGenerator(CorpusGenerator):
    def create_corpus(self, name):
        # Logique spécifique pour créer un corpus ArXiv
        corpus = Corpus(name)
        return corpus