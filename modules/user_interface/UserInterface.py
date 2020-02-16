## Name in diagram: user interface
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.vector_space.VectorSpaceModel import VectorSpaceModel
from modules.corpus.Access import Access ######## THIS IS ONLY FOR TEST ########

class UserInterface:

  def __init__(self, query, model, collection):
    self.query = query
    self.model = model
    self.collection = collection

  def getDocs(self):
    docs = []

    if(self.model == "Boolean"):
      q = BooleanModel(self.query)
    
      docs = q.search()
      docs = list( dict.fromkeys(docs) )
      #print(lst)
    elif(self.model == "VSM"):
      docs = []

    corpus = Access("data/uo_courses.json")  # LATER CORPUS WILL BE ACCESSED VIA MODELS (BRM AND VSM)
    if len(docs) > 0:
      return corpus.get_docs(docs)
    else:
      return []