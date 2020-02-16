## Name in diagram: inverted index construction
from modules.dictionary.Dictionary import Dictionary
from collections import defaultdict
from collections import Counter

class InvertedIndex:

    def __init__(self, input_file, output_file,  stopwords=True, stemming=True, normalization=True):
        self.__dictionary = Dictionary()
        self.__dictionary = self.__dictionary.create_dictionary(input_file, output_file, stopwords, stemming, normalization)
        inverted_index = defaultdict(list)
        for doc in self.__dictionary:
            # print(doc)
            # print("DocID =>",word['docID'])
            # print("Title =>", word['title'])
            # print("Description =>", word['description'])
            # for word, freq in Counter(doc['description'].split()).items():
            for word in doc['description'].split():
                inverted_index[doc['docID']].append(word)
                # break
            break

        for k,v in inverted_index.items():
            print(f'DocID : {k}===>', ", ".join(v))
# Test
i = InvertedIndex("data/original_collection.html", 'uo_course1s')
