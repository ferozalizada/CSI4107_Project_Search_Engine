from modules.corpus.PreProcessing import PreProcessing
from modules.text_processing.Tokenizer import *
from modules.text_processing.Stopword import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Normalizer import *
from modules.text_processing.Lemmatizer import *


class Dictionary:
    def __init__(self):
        self.__stopword = Stopword()
        self.__normalizer = Normalizer()
        self.__Stemmer = Stemmer()
        self.__tokenizer = Tokenizer()
        self.__preprocessor = None

    def create_dictionary(self, stopwords=True, stemming=True, normalization=True):
        print('creating dictionary')
        print(self.__stopword.get_stop_words())

        # __preprocessor = PreProcessing(
        #     './data/original_collection.html', './data/data.json').generate_corpus()


dic = Dictionary()
dic.create_dictionary()
# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
# https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
