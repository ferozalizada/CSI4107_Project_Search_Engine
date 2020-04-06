import json
import os

from collections import defaultdict
from collections import namedtuple
from pathlib import Path
from modules.text_processing.Tokenizer import Tokenizer
from modules.text_processing.Tokenizer import Tokenizer
import math


class VectorSpaceModel:
    def __init__(self):
        root_dir = Path(__file__).parent.parent.parent

        inverted_index_json = os.path.join(
            root_dir, "data/inverted_index.json")
        corpus_json = os.path.join(
            root_dir, "data/uo_courses_preprocessed.json")

        with open(inverted_index_json, 'r', encoding='utf-8') as inv_index:
            self.inverted_index = json.load(inv_index)
        with open(corpus_json, 'r', encoding='utf-8') as corpus_file:
            self.corpus = json.load(corpus_file)['docs']

        print(len(self.inverted_index))
        self.set_of_docs = {document['docID'] for document in self.corpus}
        number_of_docs = calculate_idf(self.set_of_docs, self.inverted_index)
        self.tokenizer = Tokenizer()
        self.tf_idf_matrix = calculate_tf_idf(
            self.inverted_index, calculate_idf(self.set_of_docs, self.inverted_index))

    def retrieve(self, query):
        query = query.lower()

        tokens = self.tokenizer.word_tokenizer(query)
        query_vector = [1] * len(tokens)

        doc_vectors = compute_doc_vectors(
            self.set_of_docs, self.tf_idf_matrix, tokens)

        return compute_vector_scores(query_vector, doc_vectors)


def calculate_idf(set_of_docs, inverted_index):
    return {item: math.log10(len(set_of_docs) / len(doc_list)) for item, doc_list in inverted_index.items()}


def calculate_tf_idf(inverted_index, idf_index):
    tf_idf = defaultdict(lambda: defaultdict(int))
    for word, docs in inverted_index.items():

        dict = defaultdict(int)
        for appearance in docs:
            dict[appearance["doc_id"]] = appearance['frequency'] * \
                idf_index[word]
        tf_idf[word] = dict
    # print(tf_idf)
    return tf_idf


def compute_doc_vectors(complete_set, tf_idf_matrix, tokens):

    doc_vectors = defaultdict(tuple)

    for doc_id in complete_set:
        vector = []
        for token in tokens:
            set_of_docweights = tf_idf_matrix[token]
            weight = set_of_docweights[doc_id]
            vector.append(weight)
        doc_vectors[doc_id] = vector

    return doc_vectors


def compute_vector_scores(query_vector, doc_vectors):

    scores = []
    for doc_id, vector in doc_vectors.items():
        score = 0
        for query_vector_weight, doc_tf_idf in zip(query_vector, vector):
            score += query_vector_weight * doc_tf_idf
        scores.append((doc_id, score))
    scores.sort(key=lambda tup: tup[1], reverse=True)
    return [score for score in scores if score[1] != 0]


# test
# vsm = VectorSpaceModel()
# print(vsm.retrieve('cours'))

# TODO: Dictionary sectioning
# TODO: french removal
# TODO: Report and test
# TODO: index once