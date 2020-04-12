from modules.server.Server import start_web_server
from modules.corpus.PreProcessing import PreProcessing
# from modules.corpus.Access import Access
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.dictionary.InvertedIndex import InvertedIndex
from modules.bigram_model.BigramModel import BigramModel
from helpers import constants

def main():
    #BigramModel(constants.REUTERS_COLLECTION)
    #generateIndexes()
    start_web_server()  # comment this line to test other modules without lunching web server
    #q = BooleanModel('printer AND_NOT (laser OR ink)')

def generateIndexes():
    InvertedIndex(constants.UO_CATALOG_COLLECTION, "data/original_collection.html", 'uo_courses')

main()
