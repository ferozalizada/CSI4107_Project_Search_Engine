# Name in diagram: inverted index construction
from modules.dictionary.Dictionary import Dictionary
from collections import defaultdict
from collections import Counter
import json
import os
from pathlib import Path


class InvertedIndex:

    def __init__(self, input_file, output_file,  stopwords=True, stemming=True, normalization=True):
        self.__dictionary = Dictionary()
        self.__dictionary = self.__dictionary.create_dictionary(
            input_file, output_file, stopwords, stemming, normalization)
        inverted_index = defaultdict(list)

        for doc in self.__dictionary:
            # print(doc)
            # print("DocID =>",word['docID'])
            # print("Title =>", word['title'])
            # print("Description =>", word['description'])
            # for word, freq in Counter(doc['description'].split()).items():
            set_of_words = doc['description'].split()
            c = None
            for word in set_of_words:
                #  docid: word freq
                # this is the frequency of the word
                c = Counter(doc['description'].split())
                # print(c[word])
                # inverted_index[word].append(doc['docID'])
                # break
                indexedword = IndexedWord(doc['docID'], c[word])

                inverted_index[word].append(indexedword.__dict__)
                # print(indexedword.__dict__)

        script_dir = Path(__file__).parent.parent.parent
        inverted_index_json = os.path.join(
            script_dir, 'data/inverted_index.json')

        if not os.path.isfile(inverted_index_json):
            with open(inverted_index_json, 'w', encoding="utf-8") as outfile:
                json.dump(inverted_index, outfile, indent=4)
        else:
            print("cant create index json")

        # for k, v in inverted_index.items():
        #     print(f'Words : {k} ===> docID: ', v)


class IndexedWord:
    def __init__(self, doc_id, frequency):
        self.doc_id = doc_id
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)

    def __contains__(self, key):
        return key == self.doc_id


# Test
i = InvertedIndex("data/original_collection.html", 'uo_courses')
