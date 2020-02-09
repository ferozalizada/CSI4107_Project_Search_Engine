from modules.server.server import start_web_server
from modules.corpus.PreProcessing import PreProcessing
from modules.corpus.Access import Access

def main():
    #start_web_server() #comment this line to test other modules without lunching web server
    p = PreProcessing("data/original_collection.html", "data/uo_courses.json")
    p.generate_corpus()

    corpus = Access("data/uo_courses.json")
    print(corpus.get_doc(146))
    print(corpus.get_docs([1,5,70,135,345]))

main()