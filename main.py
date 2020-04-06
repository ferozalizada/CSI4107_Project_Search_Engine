from modules.server.Server import start_web_server
from modules.corpus.PreProcessing import PreProcessing
# from modules.corpus.Access import Access
from modules.boolean_retrieval.BooleanModel import BooleanModel
from modules.dictionary.InvertedIndex import InvertedIndex

def main():
    generateIndexes()
    #i = InvertedIndex("data/original_collection.html", 'uo_courses')
    start_web_server()  # comment this line to test other modules without lunching web server
    #q = BooleanModel('printer AND_NOT (laser OR ink)')

def generateIndexes():
    #p = PreProcessing("data/original_collection.html", "data/uo_courses.json")
    #p.generate_corpus()

    i = InvertedIndex("data/original_collection.html", 'uo_courses')

main()
