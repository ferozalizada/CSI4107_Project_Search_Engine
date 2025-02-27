# Name in diagram: corpus access
import json


class Access:

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.__length = 0
        self.__json_data = []

    # return the list of docs from a corpus
    def get_docs(self, docs_id):
        docs = []

        # assumption: the docs_id are already in order in increasing order
        i = 0

        with open(self.corpus_path, 'r+', encoding="utf-8") as json_file:
            data = json.load(json_file)

            for item in docs_id:
                for doc in data['docs']:
                    if(doc['docID'] == item):
                        # add doc found to list of docs
                        docs.append(doc)
                        if(i < (len(docs_id) - 1)):
                            i += 1

        return docs

    def get_docs_list(self):
        self.__json_file = open(self.corpus_path)
        self.__json_data = json.load(self.__json_file)['docs']
        return self.__json_data

    # return one doc found by id
    def get_doc(self, doc_id):
        with open(self.corpus_path, 'r+', encoding="utf-8") as json_file:
            data = json.load(json_file)

            for doc in data['docs']:
                if(doc['docID'] == doc_id):
                    return [doc]

        # doc not found
        return []


# test function
def get_item_id(doc):
    return doc['docID']


def get_item_title(doc):
    return doc['title']


def get_item_description(doc):
    return doc['description']


def _print_docs(docs):
    for doc in docs:
        print(doc)