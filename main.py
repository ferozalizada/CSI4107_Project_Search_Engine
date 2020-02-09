from modules.server.server import start_web_server
from modules.corpus.PreProcessing import PreProcessing

def main():
    #start_web_server() #comment this line to test other modules without lunching web server
    p = PreProcessing("data/original_collection.html", "data/uo_courses.json")
    p.generate_corpus()

main()