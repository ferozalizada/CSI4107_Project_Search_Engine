import math
from collections import Counter
import json
import os
from pathlib import Path
from modules.corpus.Access import Access
from helpers import constants

# alpha, beta and gamma values and algorithm based on lectures on Rocchio Feedback
class RocchioFeedback:
    
    def __init__(self, collection, query_terms, docs_id, docs_relevant, docs_nonrelevant):
        self.collection = collection
        self.query_docs = self.get_corpus_docs(docs_id)
        self.query_terms = query_terms # array of query_terms
        self.docs_relevant = docs_relevant
        self.docs_nonrelevant = docs_nonrelevant


    # calculating the tf_idf based on the documents appearing in the result page
    def calculate_tf_idf(self):
        total_docs = len(self.query_docs)
        docs_with_word = {}
        docs_tf = {}

        for doc in self.query_docs:
            doc_id = doc['docID']
            words = doc['description'].split()
            total_words = len(words)
            count = Counter(words)
            words_found = {}
            tf = {}
        
            for word in words:
                # TF = (Number of time the word occurs in the text) / (Total number of words in text)
                tf[word] = math.log10(1 + (count[word] / total_words))
                docs_tf[doc_id] = tf

                if word not in words_found:
                    words_found[word] = True
                    if word not in docs_with_word:
                        docs_with_word[word] = 1
                    else:
                        docs_with_word[word] += 1  # counting number of documents with word t in it
        
        tf_idf = {}
        docs_tf_idf = {}
        for doc_id in docs_tf:
            for word in docs_with_word:
                # IDF = (Total number of documents / Number of documents with word t in it)
                idf = math.log10(total_docs / docs_with_word[word])

                tf = docs_tf[doc_id]
                if word in tf:
                    tf_idf[word] = tf[word] * idf
                else:
                    tf_idf[word] = 0
                
                docs_tf_idf[doc_id] = tf_idf

        sorted_terms_weight = {}

        # sort the words by frequency
        for key, weight in sorted(tf_idf.items(), key=lambda item: item[1], reverse=True):
            sorted_terms_weight[key] = weight

        return [sorted_terms_weight, docs_tf_idf]


    def get_corpus_docs(self, docs_id):
        script_dir = Path(__file__).parent.parent.parent
        corpus_path = ""

        if self.collection == constants.UO_CATALOG_COLLECTION:
            corpus_path = os.path.join(script_dir, 'data/uo_courses.json')
        elif self.collection == constants.REUTERS_COLLECTION:
            corpus_path = os.path.join(script_dir, 'data/reuters/reuters.json')

        a = Access(corpus_path)
        docs = a.get_docs(docs_id)
        return docs


    def run(self):
        result = self.calculate_tf_idf()
        expansion_terms = []
        top = 3
        count = 0

        # get query expansion terms
        for term in result[0]:
            count += 1
            if count > top:
                break
            else:
                expansion_terms.append(term)
         
        docs_tf_idf = result[1]
        docs_weight = {}  # weight for each term in doc (query terms + expansion terms)
        query_weight = [] # weight for each term in query (including expansion terms)

        for doc_id in docs_tf_idf:
            tf_idf = docs_tf_idf[doc_id]
            
            for term in self.query_terms:
                weight = 0

                if term in tf_idf:
                    weight = tf_idf[term]
                
                if doc_id in docs_weight:
                    docs_weight[doc_id].append(weight)
                else:
                    docs_weight[doc_id] = [weight]

            for term in expansion_terms:
                docs_weight[doc_id].append(tf_idf[term])

        for term in self.query_terms:
            query_weight.append(1)

        for term in expansion_terms:
            query_weight.append(0)

        # now that we have terms weight for all docs and query, run rocchio algorithm
        self.RocchioAlgorithm(docs_weight, query_weight)

        return 0

    def RocchioAlgorithm(self, docs_weight, query_weight):
        positive_centroid = []  # positive centroid vector
        negative_centroid = []  # negative centroid vector
        new_query = []          # query vector resulting from rocchio algorithm
        alpha = 1
        beta = 0.75
        gamma = 0.15
        num_terms = len(query_weight)

        # calculate positive and negative centroids values
        for doc_id in docs_weight:
            count = 0
            for weight in docs_weight[doc_id]:

                if doc_id in self.docs_relevant:
                    if len(positive_centroid) < num_terms:
                        positive_centroid.append(weight)
                    else:
                        positive_centroid[count] += weight  # for each term sum the weights of all relevant documents

                elif doc_id in self.docs_nonrelevant:
                    if len(negative_centroid) < num_terms:
                        negative_centroid.append(weight)
                    else:
                        negative_centroid[count] += weight  # for each term sum the weights of all non-relevant documents
                count += 1

        num_dr = len(self.docs_relevant)
        num_dnr = len(self.docs_nonrelevant)

        # calculate resulting query
        for i in range(num_terms):
            positive_centroid[i] = positive_centroid[i] / num_dr
            negative_centroid[i] = negative_centroid[i] / num_dnr

            new_weight = (alpha * query_weight[i]) + (beta * positive_centroid[i]) - (gamma * negative_centroid[i])
            
            if new_weight < 0:
                new_weight = 0

            new_query.append(new_weight)

        print(positive_centroid)
        print(negative_centroid)
        print(new_query)