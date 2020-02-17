import json
import os

from collections import defaultdict
from collections import namedtuple
from pathlib import Path

from modules.text_processing.Tokenizer import Tokenizer
import math

class VectorSpaceModel:
    def __init__(self):
        root_dir = Path(__file__).parent.parent.parent

        inverted_index_json = os.path.join(root_dir, "data/inverted_index.json")
        corpus_json = os.path.join(root_dir, "data/uo_courses_preprocessed.json")

        with open(inverted_index_json) as inv_index:
            self.inverted_index = json.load(inv_index)
        with open(corpus_json) as corpus_file:
            self.corpus = json.load(corpus_file)['docs']

        print(len(self.inverted_index))
        self.set_of_docs = {document['docID'] for document in self.corpus}
        number_of_docs = compute_idf(self.set_of_docs, self.inverted_index)
        # print(number_of_docs)
        print(self.inverted_index)
        # print(self.corpus['docs'])
        # tf_idf = compute_tf_idf(self.inverted_index, compute_idf(self.set_of_docs, self.inverted_index))
        # print(tf_idf)

def compute_idf(set_of_docs, inverted_index):
    return {item: math.log10(len(set_of_docs) / len(doc_list)) for item, doc_list in inverted_index.items()}






# test
vsm = VectorSpaceModel()


# TODO: Dictionary sectioning
# TODO: french removal
# TODO: Report and test
# TODO: index once