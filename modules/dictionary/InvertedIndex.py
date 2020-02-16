## Name in diagram: inverted index construction
from modules.dictionary.Dictionary import Dictionary
class InvertedIndex:

    def __init__(self, input_file, output_file,  stopwords=True, stemming=True, normalization=True):
        self.__dictionary = Dictionary()
        self.__dictionary.create_dictionary(input_file, output_file, stopwords, stemming, normalization)


# Test
i = InvertedIndex("data/original_collection.html", 'uo_course1s')
