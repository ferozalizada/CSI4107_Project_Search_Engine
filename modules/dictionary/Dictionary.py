import json
import os
from pathlib import Path

from helpers import constants
from modules.corpus.Access import *
from modules.corpus.PreProcessing import PreProcessing
from modules.text_processing.Lemmatizer import *
from modules.text_processing.Normalizer import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Tokenizer import *


class Dictionary:
    def __init__(self, collection):
        self.__stopword = None
        self.__normalizer = Normalizer()
        self.__stemmer = Stemmer()
        self.__tokenizer = Tokenizer()
        self.__preprocessor = None
        self.__corpus_access = None
        self.__corpus_file = []
        self.__input_path = ""
        self.__collection = collection
        # create_dictionary(self, file_path, output_file, stopwords=True, stemming=True, normalization=True)
        self.__dictionary = {
            'original': set(),
            'stopword': set(),
            'processed': set(),
            'stemmed': set(),
            'normalized': set()
        }

    def create_dictionary(self, file_path, output_file, stopwords=True, stemming=True, normalization=True):
        print('creating dictionary')

        script_dir = Path(__file__).parent.parent.parent
        # file_path = "data/original_collection.html"
        html_file = ""
        corpus_file = ""
        # print(corpus_file)

        if self.__collection == constants.UO_CATALOG_COLLECTION:
            html_file = os.path.join(script_dir, file_path)
            self.__input_path = Path(html_file).parent
            corpus_file = os.path.join(Path(html_file).parent, output_file+".json")

            if os.path.isfile(html_file):
                print("HTML file exists")
            else:
                print("HTML file does not exists")
        elif self.__collection == constants.REUTERS_COLLECTION:
            self.__input_path = Path(file_path[0]).parent.parent
            corpus_file = os.path.join(self.__input_path, output_file+".json")

            for i in range(len(file_path)):
                file_path[i] = os.path.join(script_dir, file_path[i])

        # Generate the preprocessed json file
        if os.path.isfile(corpus_file):
            print("Corpus already exists file exists")
        else:
            print("Creating corpus file")
            if self.__collection == constants.UO_CATALOG_COLLECTION:
                PreProcessing(self.__collection, html_file, corpus_file).generate_corpus()
            elif self.__collection == constants.REUTERS_COLLECTION:
                PreProcessing(self.__collection, file_path, corpus_file).generate_corpus()

        self.__corpus_access = Access(corpus_file)
        self.__corpus_file = self.__corpus_access.get_docs_list()

        # 1. delete stop words
        i = 0
        for doc in self.__corpus_file:

            # Tokenize and lower()
            title_tokens = self.__tokenizer.word_tokenizer(
                doc['title'].lower())
            description_tokens = self.__tokenizer.word_tokenizer(
                doc['description'].lower())
            #self.__dictionary['original'] |= set(title_tokens)
            #self.__dictionary['original'] |= set(description_tokens)

            # Stemming
            if stemming:
                title_tokens = self.__stemmer.stem_word(title_tokens)
                description_tokens = self.__stemmer.stem_word(
                    description_tokens)
                #self.__dictionary['stemmed'] |= set(title_tokens.copy())
                #self.__dictionary['stemmed'] |= set(description_tokens)
            # Normalization
            if normalization:
                title_tokens = map(self.__normalizer.normalize, title_tokens)
                description_tokens = map(
                    self.__normalizer.normalize, description_tokens)

                #self.__dictionary['normalized'] |= set(title_tokens)
                #self.__dictionary['normalized'] |= set(description_tokens)

            # StopWords removal
            if stopwords:
                self.__stopword = Stopword().get_stop_words()

                for word in self.__stopword:

                    title_tokens = [e for e in title_tokens if e not in word]
                    description_tokens = [
                        c for c in description_tokens if c not in word]

                    #self.__dictionary['stopword'] |= set(title_tokens)
                    #self.__dictionary['stopword'] |= set(description_tokens)

                    #self.__dictionary['processed'] |= set(title_tokens)
                    #self.__dictionary['processed'] |= set(description_tokens)

                    self.__corpus_file[i]['description'] = self.__corpus_file[i]['description'].replace(
                        self.__corpus_file[i]['description'], " ".join(description_tokens))
                    self.__corpus_file[i]['title'] = self.__corpus_file[i]['title'].replace(
                        self.__corpus_file[i]['title'], " ".join(title_tokens))

            i += 1
        
        self.save_dictionary()
        with open(os.path.join(self.__input_path, "dictionary_short.json"), 'w', encoding="utf-8") as f:
            lists_words = {k: list(v) for (k, v) in self.__dictionary.items()}
            json.dump(lists_words, f, ensure_ascii=False, indent=4)
        return self.__corpus_file

    def save_dictionary(self):
        with open(os.path.join(self.__input_path, "dictionary.json"), 'w', encoding="utf-8") as f:
            json.dump(self.__corpus_file, f)


# Test
# dic = Dictionary()
# dic.create_dictionary("data/original_collection.html", 'uo_courses')
# dic.save_dictionary()


# https://github.com/ArmandSyah/CSI4107-Search-Engine-Project/blob/master/dictionary/dictionary.py
# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
# https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
