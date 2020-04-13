from modules.server.Server import start_web_server
from modules.corpus.PreProcessing import PreProcessing
# from modules.corpus.Access import Access
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.dictionary.InvertedIndex import InvertedIndex
from modules.bigram_model.BigramModel import BigramModel
from modules.rocchio_feedback.RocchioFeedback import RocchioFeedback
from helpers import constants

def main():
    #BigramModel(constants.REUTERS_COLLECTION)
    #generateIndexes()
    docs_id = []
    docs_relevant = []
    docs_nonrelevant = []

    for i in range(1, 100):
        docs_id.append(i)
        if i < 11:
            docs_relevant.append(i)
        else:
            docs_nonrelevant.append(i)

    print(len(docs_id))
    print("start")
    rf = RocchioFeedback(constants.REUTERS_COLLECTION, ["security"], docs_id, docs_relevant, docs_nonrelevant)
    rf.run()
    #start_web_server()  # comment this line to test other modules without lunching web server
    #q = BooleanModel('printer AND_NOT (laser OR ink)')

def generateIndexes():
    InvertedIndex(constants.UO_CATALOG_COLLECTION, "data/original_collection.html", 'uo_courses')

main()
