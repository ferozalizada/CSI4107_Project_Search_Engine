from modules.server.Server import start_web_server
from modules.corpus.PreProcessing import PreProcessing
# from modules.corpus.Access import Access
from modules.boolean_retrieval.BooleanModel import BooleanModel


def main():

    # start_web_server()  # comment this line to test other modules without lunching web server
    start_web_server()
    p = PreProcessing("data/original_collection.html", "data/uo_courses.json")
    p.generate_corpus()

    q = BooleanModel('printer AND_NOT (laser OR ink)')
    
    print(q.search())
    #print(q.infixToPostfix('(7 AND 8) OR (3 AND 2)'))
    #print(q.infixToPostfix('(7 + 8) / (3 + 2)'))
    #print(q.postfixEval('7 8 + 3 2 + /'))
    # start_web_server()  # comment this line to test other modules without lunching web server
    #p = PreProcessing("data/original_collection.html", "data/uo_courses.json")
    #p.generate_corpus()

    # p.fun()

    #corpus = Access("data/uo_courses.json")
    # print(corpus.get_doc(146))
    # print(corpus.get_docs([1,5,70,135,345]))


main()
