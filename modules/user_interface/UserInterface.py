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
    dummy = True

    if(self.model == "Boolean"):
      dummy = True
    elif(self.model == "VSM"):
      dummy = False

    corpus = Access("data/uo_courses.json")  # LATER CORPUS WILL BE ACCESSED VIA MODELS (BRM AND VSM)
    return corpus.get_doc(146)