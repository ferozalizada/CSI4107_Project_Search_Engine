from modules.text_processing.Lemmatizer import *
from modules.text_processing.Normalizer import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Stopword import *
from modules.text_processing.Tokenizer import *


class Dictionary:
    def __init__(self):
        self.__stopword = stopwords
        self.__normalizer = Normalizer()
        self.__Stemmer = Stemmer()
        self.__tokenizer = Tokenizer()

    def create_dictionary(self, stopwords=True, stemming=True, normalization=True):
        print('creating dictionary')

# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
# https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
