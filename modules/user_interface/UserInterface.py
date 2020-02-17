## Name in diagram: user interface
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.vector_space.VectorSpaceModel import VectorSpaceModel
from modules.corpus.Access import Access
from modules.text_processing.Stopword import *
from modules.text_processing.Stemmer import *
from modules.text_processing.Normalizer import *

# from modules.vector_space.VectorSpaceModel import VectorSpaceModel
from modules.corpus.Access import Access ######## THIS IS ONLY FOR TEST ########


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

    if(self.model == "Boolean"):
      self.query = self.__cleanQuery()
      q = BooleanModel(self.query)
      
      docs = q.search()
      docs = list( dict.fromkeys(docs) )
      
    elif(self.model == "VSM"):
      docs = []

    corpus = Access("data/uo_courses.json")
    if len(docs) > 0:
      return corpus.get_docs(docs)
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

#https://www.sqlite.org/download.html
#https://stackoverflow.com/questions/55190327/nltk-importerror-dll-load-failed-the-specified-module-could-not-be-found