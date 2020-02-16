## Name in diagram: boolean retrieval model
from modules.boolean_retrieval.QueryPreProcessing import QueryPreProcessing
import random 
import json

class BooleanModel:

    def __init__(self, query):
        self.query = query

    def search(self):
        prec = {}
        prec["AND"] = 3
        prec["OR"] = 4
        prec["AND_NOT"] = 2
        prec["("] = 1

        self.inverted_index = self.__generateIndex()
        q = QueryPreProcessing()
        result = []
        qlen = len(self.query.split())
        #print(qlen)
        if qlen == 1:
            result = self.__searchInIndex("", self.query, "")
        elif qlen > 1:
            postfix_expr = q.infixToPostfix(prec, self.query)
            #print(postfix_expr)
            result = q.postfixEval(self.__searchInIndex, prec, postfix_expr)
        
        return result

    def __searchInIndex(self, op, op1, op2):
        docs1 = []
        docs2 = []
        docs = []
        
        if type(op1) == list:
            docs1 = op1
        elif op1 in self.inverted_index:
            docs1 = self.inverted_index[op1] #self.invertedIndex[op1]

        if type(op2) == list:
            docs2 = op2
        elif op2 in self.inverted_index:
            docs2 = self.inverted_index[op2] #self.invertedIndex[op2]

        len1 = len(docs1)
        len2 = len(docs2)

        if(op == "AND"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i]["doc_id"] == docs2[j]["doc_id"]:
                    docs.append(docs1[i]["doc_id"]) # append docs appearing in both term indexes
                    i += 1
                    j += 1
                elif docs1[i]["doc_id"] < docs2[j]["doc_id"]:
                    i += 1
                else:
                    j += 1

        elif(op == "OR"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i]["doc_id"] == docs2[j]["doc_id"]:
                    docs.append(docs1[i]["doc_id"]) # append docs appearing in both term indexes
                    i += 1
                    j += 1
                elif docs1[i]["doc_id"] < docs2[j]["doc_id"]:
                    docs.append(docs1[i]["doc_id"]) # append docs appearing in both term indexes
                    i += 1
                else:
                    docs.append(docs2[j]["doc_id"]) # append docs appearing in both term indexes
                    j += 1
            
            while i < len1:
                docs.append(docs1[i]["doc_id"])
                i += 1

            while j < len2:
                docs.append(docs2[j]["doc_id"])
                j += 1

        elif(op == "AND_NOT"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i]["doc_id"] == docs2[j]["doc_id"]:
                    i += 1
                    j += 1
                elif docs1[i]["doc_id"] < docs2[j]["doc_id"]:
                    docs.append(docs1[i]["doc_id"]) # append docs appearing in docs1 but not docs2
                    i += 1
                else:
                    j += 1

        elif op == "":
            i = 0
            while len1 > 0 and i < len1: 
                docs.append(docs1[i]["doc_id"]) # append docs appearing in docs1
                i += 1
        
        return docs

    def __generateIndex(self):
        inverted_index = {}

        with open("data/inverted_index.json") as json_file:
            inverted_index = json.load(json_file)

        return inverted_index

    #https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/
    #https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
    #https://www.geeksforgeeks.org/python-list-sort/

