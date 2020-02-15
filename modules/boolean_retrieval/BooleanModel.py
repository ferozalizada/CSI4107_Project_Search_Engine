## Name in diagram: boolean retrieval model
from modules.boolean_retrieval.QueryPreProcessing import QueryPreProcessing
import random 

class BooleanModel:

    def __init__(self, query):
        self.query = query

    def search(self):
        prec = {}
        prec["AND"] = 3
        prec["OR"] = 4
        prec["AND_NOT"] = 2
        prec["("] = 1

        q = QueryPreProcessing()
        postfix_expr = q.infixToPostfix(prec, self.query)
        result = q.postfixEval(self.__searchInIndex, prec, postfix_expr)
        self.__tempIndex()
        return result

    def __searchInIndex(self, op, op1, op2, docs):

        if(op == "AND"):
            # op1 AND op2 must be in index
            docs.append(op1) # append docs retrieved in inverted index
        elif(op == "OR"):
            # op1 OR op2 must be in index
            docs.append(op2) # append docs retrieved in inverted index
        elif(op == "AND_NOT"):
            # op1 must be in index but not op2
            docs.append(op1) # append docs retrieved in inverted index

        return docs

    def __tempIndex(self):
        dictionary = ['printer', 'ink', 'laser', 'printer', 'ink', 'laser', 'printer', 'ink', 'laser','printer', 'ink', 'laser'] # terms
        terms_docsID = {}

        # build a list of term/docID pairs
        for term in dictionary:
            docID = random.randint(1,500)
            if(term in terms_docsID):
                terms_docsID[term].append(docID)
            else:
                terms_docsID[term] = [docID]
        
        # sort docsID
        for term in terms_docsID:
            terms_docsID[term].sort()
        
        print(terms_docsID)
        


    #https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/
    #https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
    #https://www.geeksforgeeks.org/python-list-sort/