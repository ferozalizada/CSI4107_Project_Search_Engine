# Name in diagram: inverted index construction
from modules.dictionary.Dictionary import Dictionary
from collections import defaultdict
from collections import Counter
import json
import os
from pathlib import Path
from helpers import constants


class InvertedIndex:

    def __init__(self, collection, input_file, output_file,  stopwords=True, stemming=True, normalization=True):
        
        script_dir = Path(__file__).parent.parent.parent
        inverted_index_json = ""

        if collection == constants.UO_CATALOG_COLLECTION:
            inverted_index_json = os.path.join(script_dir, 'data/inverted_index.json')
        elif collection == constants.REUTERS_COLLECTION:
            inverted_index_json = os.path.join(script_dir, 'data/reuters/inverted_index.json')

        # create index files only once
        if not os.path.isfile(inverted_index_json):

            self.__dictionary = Dictionary(collection)
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
                    if word.isnumeric() == False:
                        c = Counter(doc['description'].split())
                        # print(c[word])
                        # inverted_index[word].append(doc['docID'])
                        # break
                        indexedword = IndexedWord(doc['docID'], c[word])

                        inverted_index[word].append(indexedword.__dict__)
                    # print(indexedword.__dict__)

            with open(inverted_index_json, 'w', encoding="utf-8") as outfile:
                json.dump(inverted_index, outfile, indent=4)

        else:
            print("Inverted index already exists")

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
#i = InvertedIndex(constants.UO_CATALOG_COLLECTION, "data/original_collection.html", 'uo_courses')

reuters_files = ["data/reuters/original/reut2-000.sgm", "data/reuters/original/reut2-001.sgm", "data/reuters/original/reut2-002.sgm", "data/reuters/original/reut2-003.sgm", "data/reuters/original/reut2-004.sgm",
                 "data/reuters/original/reut2-005.sgm", "data/reuters/original/reut2-006.sgm", "data/reuters/original/reut2-007.sgm", "data/reuters/original/reut2-008.sgm", "data/reuters/original/reut2-009.sgm",
                 "data/reuters/original/reut2-010.sgm", "data/reuters/original/reut2-011.sgm", "data/reuters/original/reut2-012.sgm", "data/reuters/original/reut2-013.sgm", "data/reuters/original/reut2-014.sgm",
                 "data/reuters/original/reut2-015.sgm", "data/reuters/original/reut2-016.sgm", "data/reuters/original/reut2-017.sgm", "data/reuters/original/reut2-018.sgm", "data/reuters/original/reut2-019.sgm", 
                 "data/reuters/original/reut2-020.sgm", "data/reuters/original/reut2-021.sgm"]

i = InvertedIndex(constants.REUTERS_COLLECTION, reuters_files, 'reuters')
