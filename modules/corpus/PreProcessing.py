# Name in diagram: corpus pre-processing
import json
import os.path

from bs4 import BeautifulSoup

from helpers import constants


##### CODE IN THIS FILE BASED ON THE FOLLOWING SOURCES #####
# https://www.dataquest.io/blog/web-scraping-tutorial-python/ #
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/ #


class PreProcessing:

    def __init__(self, collection, collection_path, corpus_path):
        self.collection = collection
        self.collection_path = collection_path
        self.corpus_path = corpus_path
        self.doc_id = 0

    def __create_corpus(self):
        docs_dict = {}
        docs = []
        docs_dict['docs'] = docs

        #with open(self.collection_path, "rb", encoding="utf-8") as f:
        with open(self.collection_path, "rb") as f:
            contents = f.read().decode('UTF-8')
            soup = BeautifulSoup(contents, 'html.parser')
            courses = soup.find_all('div', class_='courseblock')

            for course in courses:
                title = course.find('p', class_='courseblocktitle').get_text()

                if(title.find('crédits)') == -1):
                    # french course not found
                    self.__add_doc(soup, docs_dict['docs'], course)

        self.__create_corpus_file(docs_dict)

    # Add doc to docs array
    def __add_doc(self, soup, docs, course):
        title = course.find('p', class_='courseblocktitle').get_text().strip()
        description = ""

        try:
            description = course.find(
                'p', class_='courseblockdesc').get_text().strip()
        except AttributeError:
            description = ""

        self.doc_id += 1
        docs.append({"docID": self.doc_id, "title": title,
                     "description": description.strip()})

    def __create_routers_corpus(self):
        docs_dict = {}
        docs = []
        docs_dict['docs'] = docs

        for file_path in self.collection_path:

            with open(file_path, 'rb') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'html.parser')
                reuters = soup.findAll('reuters')

                for reuter in reuters:
                    title = ""
                    try:
                        title = reuter.find('title').get_text().strip()
                        self.__add_reuters_doc(soup, docs_dict['docs'], reuter, title)
                    except AttributeError:
                        title = ""

        self.__create_corpus_file(docs_dict)

    def __add_reuters_doc(self, soup, docs, reuter, title):
        description = ""

        try:
            description = reuter.find('body').get_text().strip()
        except AttributeError:
            description = ""

        self.doc_id += 1
        docs.append({"docID": self.doc_id, "title": title,
                     "description": description})


    def __create_corpus_file(self, json_docs):
        with open(self.corpus_path, 'w', encoding="utf-8") as outfile:
            json.dump(json_docs, outfile)


    # Create a corpus for a given collection
    def generate_corpus(self):
        # Create corpus file if it does not exist
        if os.path.isfile(self.corpus_path) == False:
            if self.collection == constants.UO_CATALOG_COLLECTION:
                self.__create_corpus()
            elif self.collection == constants.REUTERS_COLLECTION:
                self.__create_routers_corpus()