## Name in diagram: corpus pre-processing
from bs4 import BeautifulSoup
import json
import os.path

class PreProcessing:

    def __init__(self, collection_path, corpus_path):
        self.collection_path = collection_path
        self.corpus_path = corpus_path
        self.doc_id = 0


    def _create_corpus(self):
        docs = []

        with open(self.collection_path, "rb") as f:

            contents = f.read().decode('UTF-8')
            soup = BeautifulSoup(contents, 'html.parser')
            courses = soup.find_all('div', class_='courseblock')
            
            for course in courses:
                title = course.find('p', class_='courseblocktitle').get_text()

                if(title.find('crédits)') == -1):
                    # french course not found
                    self._add_doc(soup, docs, course)
            
        json_docs = json.dumps(docs)
        self._create_corpus_file(json_docs)


    # Add doc to docs array
    def _add_doc(self, soup, docs, course):
        title = course.find('p', class_='courseblocktitle').get_text()
        description = ""

        try:
            description = course.find('p', class_='courseblockdesc').get_text()
        except AttributeError:
            description = ""

        self.doc_id += 1
        docs.append({"docID": self.doc_id, "title": title, "description": description})
    

    def _create_corpus_file(self, json_docs):
        with open(self.corpus_path, 'w') as outfile:
            json.dump(json_docs, outfile)


    # Create a corpus for a given collection
    def generate_corpus(self):
        # Create corpus file if it does not exist
        if os.path.isfile(self.corpus_path) == False:
            self._create_corpus()


# https://www.w3schools.com/python/python_file_open.asp
# https://www.w3schools.com/python/python_json.asp
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
# https://stackoverflow.com/questions/10971033/backporting-python-3-openencoding-utf-8-to-python-2
# https://www.w3schools.com/python/python_arrays.asp
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# https://linuxize.com/post/python-check-if-file-exists/