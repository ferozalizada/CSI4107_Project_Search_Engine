from modules.corpus.PreProcessing import PreProcessing
from modules.corpus.Access import *
from modules.text_processing.Tokenizer import *
from modules.text_processing.Stopword import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Normalizer import *
from modules.text_processing.Lemmatizer import *
import os
from pathlib import Path
import json

class Dictionary:
    def __init__(self):
        self.__stopword = None
        self.__normalizer = Normalizer()
        self.__stemmer = Stemmer()
        self.__tokenizer = Tokenizer()
        self.__preprocessor = None
        self.__corpus_access = None
        self.__corpus_file = []
        self.__input_path = ""
        # create_dictionary(self, file_path, output_file, stopwords=True, stemming=True, normalization=True)

    def create_dictionary(self, file_path, output_file, stopwords=True, stemming=True, normalization=True):
        print('creating dictionary')

        script_dir = Path(__file__).parent.parent.parent
        # file_path = "data/original_collection.html"
        html_file = os.path.join(script_dir, file_path)
        corpus_file = os.path.join(Path(html_file).parent, output_file+".json")
        # print(corpus_file)
        self.__input_path = Path(html_file).parent
        if os.path.isfile(html_file):
            print("HTML file exists")
        else:
            print("HTML file does not exists")

        # Generate the preprocessed json file
        if os.path.isfile(corpus_file):
            print("Corpus already exists file exists")
        else:
            print("Creating corpus file")
            PreProcessing(html_file, corpus_file).generate_corpus()

        self.__corpus_access = Access(corpus_file)
        self.__corpus_file = self.__corpus_access.get_docs_list()

        #1. delete stop words
        i = 0
        for doc in self.__corpus_file:

            # Tokenize and lower()
            title_tokens = self.__tokenizer.word_tokenizer(doc['title'].lower())
            description_tokens = self.__tokenizer.word_tokenizer(doc['description'].lower())

            # Stemming
            if stemming:
                title_tokens = self.__stemmer.stem_word(title_tokens)
                description_tokens = self.__stemmer.stem_word(description_tokens)

            # Normalization
            if normalization:
                title_tokens = map(self.__normalizer.normalize, title_tokens)
                description_tokens = map(self.__normalizer.normalize, description_tokens)

            # StopWords removal
            if stopwords:
                self.__stopword = Stopword().get_stop_words()

                for word in self.__stopword:

                    title_tokens = [e for e in title_tokens if e not in word]
                    description_tokens = [c for c in description_tokens if c not in word]

                    self.__corpus_file[i]['description'] = self.__corpus_file[i]['description'].replace(self.__corpus_file[i]['description'], " ".join(description_tokens))
                    self.__corpus_file[i]['title'] = self.__corpus_file[i]['title'].replace(self.__corpus_file[i]['title'], " ".join(title_tokens))

            i += 1

        return self.__corpus_file

    def save_dictionary(self):
        with open(os.path.join(self.__input_path, "dictionary.json"), 'w') as f:
            json.dump(self.__corpus_file, f)


# Test
# dic = Dictionary()
# dic.create_dictionary("data/original_collection.html", 'uo_courses')
# dic.save_dictionary()



# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
# https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
