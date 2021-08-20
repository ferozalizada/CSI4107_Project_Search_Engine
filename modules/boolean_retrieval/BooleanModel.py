# Name in diagram: boolean retrieval model
import json

from helpers import constants
from modules.boolean_retrieval.QueryPreProcessing import QueryPreProcessing


class BooleanModel:

    def __init__(self, query, collection):
        self.query = query
        self.collection = collection

    def search(self):
        prec = {}
        prec["AND"] = 3
        prec["OR"] = 4
        prec["AND_NOT"] = 2
        prec["("] = 1

        self.inverted_index = self.__generateIndex()

        #dct = list(self.inverted_index)
        #for key in dct: print(key)

        """dct = list(self.inverted_index)
        for key in dct: 
            if key.isnumeric() == True:
                print(key)"""

        q = QueryPreProcessing()
        result = []
        qlen = len(self.query.split())

        if qlen == 1:
            result = self.__searchInIndex("", self.query, "")
        elif qlen > 1:
            postfix_expr = q.infixToPostfix(prec, self.query)
            result = q.postfixEval(self.__searchInIndex, prec, postfix_expr)

        return result

    ##### Algorithm based on the lectures on Boolean Retrieval #####
    def __searchInIndex(self, op, op1, op2):
        docs1 = []
        docs2 = []
        docs = []

        if type(op1) == list:
            docs1 = op1
        elif op1 in self.inverted_index:
            docs1 = self.inverted_index[op1]

        if type(op2) == list:
            docs2 = op2
        elif op2 in self.inverted_index:
            docs2 = self.inverted_index[op2]

        len1 = len(docs1)
        len2 = len(docs2)

        if(op == "AND"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                docID_1 = 0
                docID_2 = 0

                if type(docs1[i]) == int:
                    docID_1 = docs1[i]
                else:
                    docID_1 = docs1[i]["doc_id"]

                if type(docs2[j]) == int:
                    docID_2 = docs2[j]
                else:
                    docID_2 = docs2[j]["doc_id"]

                if docID_1 == docID_2:
                    # append docs appearing in both term indexes
                    docs.append(docID_1)
                    i += 1
                    j += 1
                elif docID_1 < docID_2:
                    i += 1
                else:
                    j += 1

        elif(op == "OR"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                docID_1 = 0
                docID_2 = 0

                if type(docs1[i]) == int:
                    docID_1 = docs1[i]
                else:
                    docID_1 = docs1[i]["doc_id"]

                if type(docs2[j]) == int:
                    docID_2 = docs2[j]
                else:
                    docID_2 = docs2[j]["doc_id"]

                if docID_1 == docID_2:
                    # append docs appearing in both term indexes
                    docs.append(docID_1)
                    i += 1
                    j += 1
                elif docID_1 < docID_2:
                    # append docs appearing in both term indexes
                    docs.append(docID_1)
                    i += 1
                else:
                    # append docs appearing in both term indexes
                    docs.append(docID_2)
                    j += 1

            while i < len1:
                docs.append(docID_1)
                i += 1

            while j < len2:
                docs.append(docID_2)
                j += 1

        elif(op == "AND_NOT"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                docID_1 = 0
                docID_2 = 0

                if type(docs1[i]) == int:
                    docID_1 = docs1[i]
                else:
                    docID_1 = docs1[i]["doc_id"]

                if type(docs2[j]) == int:
                    docID_2 = docs2[j]
                else:
                    docID_2 = docs2[j]["doc_id"]

                if docID_1 == docID_2:
                    i += 1
                    j += 1
                elif docID_1 < docID_2:
                    # append docs appearing in docs1 but not docs2
                    docs.append(docID_1)
                    i += 1
                else:
                    j += 1

        elif op == "":
            i = 0
            while len1 > 0 and i < len1:
                # append docs appearing in docs1
                docs.append(docs1[i]["doc_id"])
                i += 1

        return docs

    def __generateIndex(self):
        inverted_index = {}
        file_path = ""

        if self.collection == constants.UO_CATALOG_COLLECTION:
            file_path = "data/inverted_index.json"
        elif self.collection == constants.REUTERS_COLLECTION:
            file_path = "data/reuters/inverted_index.json"

        with open(file_path, "r+", encoding="utf-8") as json_file:
            inverted_index = json.load(json_file)

        return inverted_index
