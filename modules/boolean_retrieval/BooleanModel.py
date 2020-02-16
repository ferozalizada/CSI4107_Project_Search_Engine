
# Name in diagram: boolean retrieval model
class BooleanModel:

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

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

        self.invertedIndex = self.__tempIndex()
        q = QueryPreProcessing()
        postfix_expr = q.infixToPostfix(prec, self.query)
        print(postfix_expr)
        result = q.postfixEval(self.__searchInIndex, prec, postfix_expr)
        
        return result

    def __searchInIndex(self, op, op1, op2):
        docs1 = []
        docs2 = []
        docs = []
        
        if type(op1) == list:
            docs1 = op1
        else:
            docs1 = self.invertedIndex[op1]

        if type(op2) == list:
            docs2 = op2
        else:
            docs2 = self.invertedIndex[op2]

        len1 = len(docs1)
        len2 = len(docs2)

        if(op == "AND"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i] == docs2[j]:
                    docs.append(docs1[i]) # append docs appearing in both term indexes
                    i += 1
                    j += 1
                elif docs1[i] < docs2[j]:
                    i += 1
                else:
                    j += 1

        elif(op == "OR"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i] == docs2[j]:
                    docs.append(docs1[i]) # append docs appearing in both term indexes
                    i += 1
                    j += 1
                elif docs1[i] < docs2[j]:
                    docs.append(docs1[i]) # append docs appearing in both term indexes
                    i += 1
                else:
                    docs.append(docs2[j]) # append docs appearing in both term indexes
                    j += 1
            
            while i < len1:
                docs.append(docs1[i])
                i += 1

            while j < len2:
                docs.append(docs2[j])
                j += 1

        elif(op == "AND_NOT"):
            i = 0
            j = 0
            while len1 > 0 and len2 > 0 and (i < len1 and j < len2):
                if docs1[i] == docs2[j]:
                    i += 1
                    j += 1
                elif docs1[i] < docs2[j]:
                    docs.append(docs1[i]) # append docs appearing in docs1 but not docs2
                    i += 1
                else:
                    j += 1

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
        
        terms_docsID["printer"].append(360)
        terms_docsID["printer"].append(59)
        terms_docsID["printer"].append(177)
        terms_docsID["ink"].append(360)
        terms_docsID["ink"].append(59)
        terms_docsID["ink"].append(177)
        terms_docsID["laser"].append(360)
        terms_docsID["laser"].append(59)
        terms_docsID["laser"].append(177)

        # sort docsID
        for term in terms_docsID:
            terms_docsID[term].sort()
        
        return terms_docsID
        


    #https://www.geeksforgeeks.org/python-add-new-keys-to-a-dictionary/
    #https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
    #https://www.geeksforgeeks.org/python-list-sort/

