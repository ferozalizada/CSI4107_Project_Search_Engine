# Name in diagram: corpus access
import json


class Access:

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    # return the list of docs from a corpus

    def get_docs(self, docs_id):
        docs = []

        # assumption: the docs_id are already in order in increasing order
        i = 0

        with open(self.corpus_path) as json_file:
            data = json.load(json_file)

            for doc in data['docs']:
                if(doc['docID'] == docs_id[i]):
                    # add doc found to list of docs
                    docs.append(doc)
                    if(i < (len(docs_id) - 1)):
                        i += 1

        # self._print_docs(docs)
        return docs

    # return one doc found by id

    def get_doc(self, doc_id):
        with open(self.corpus_path) as json_file:
            data = json.load(json_file)

            for doc in data['docs']:
                if(doc['docID'] == doc_id):
                    return [doc]

        # doc not found
        return []

    # test function

    def _print_docs(self, docs):
        for doc in docs:
            print(doc)
