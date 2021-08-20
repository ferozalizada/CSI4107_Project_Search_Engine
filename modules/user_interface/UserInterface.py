# Name in diagram: user interface
from helpers import constants
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.corpus.Access import Access
from modules.text_processing.Normalizer import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Stopword import *
from modules.vector_space.VectorSpaceModel import VectorSpaceModel


class UserInterface:

  def __init__(self, query, model, collection):
    self.query = query
    self.model = model
    self.collection = collection
    self.__stopword = None
    self.__normalizer = Normalizer()
    self.__stemmer = Stemmer()

  def getDocs(self):
    docs = []
    scores = []

    if(self.model == "Boolean"):
        #print(self.query)
        self.query = self.__cleanQuery()
        #print(self.query)
        q = BooleanModel(self.query, self.collection)

        # print(q)
        docs = q.search()
        docs = list(dict.fromkeys(docs))

    elif(self.model == "VSM"):
        docs = []
        self.query = self.__cleanQuery()
        vsm = VectorSpaceModel(self.collection).retrieve(self.query)
        scores = [i[1] for i in vsm]
        docs = [i[0] for i in vsm]

    corpus = []
    if self.collection == constants.UO_CATALOG_COLLECTION:
        corpus = Access("data/uo_courses.json")
    elif self.collection == constants.REUTERS_COLLECTION:
        corpus = Access("data/reuters/reuters.json")

    if len(docs) > 0:
        json_docs = []
        for i, item in enumerate(corpus.get_docs(docs)):
            if self.model == "VSM":
                item['score'] = scores[i]
                json_docs.append(item)
            else:
                item['score'] = 1
                json_docs.append(item)
        #print(json_docs)
        return json_docs
    else:
        return []

  def __cleanQuery(self):
    q = self.query.split()

    for i in range(len(q)):
        if q[i] not in ["AND", "AND_NOT", "OR"]:
            # lower()
            q[i] = q[i].lower()
            # Stemming
            q[i] = self.__stemmer.stem_word(q[i])
            # Normalization
            q[i] = self.__normalizer.normalize(q[i])

    # StopWords removal
    self.__stopword = Stopword().get_stop_words()

    for word in self.__stopword:
        q = [e for e in q if e not in word or e in ["AND", "AND_NOT", "OR"]]

    return ' '.join(q)

# https://www.sqlite.org/download.html
# https://stackoverflow.com/questions/55190327/nltk-importerror-dll-load-failed-the-specified-module-could-not-be-found