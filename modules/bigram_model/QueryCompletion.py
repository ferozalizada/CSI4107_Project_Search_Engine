import json
import os
from pathlib import Path
from modules.text_processing.Stopword import Stopword
from modules.text_processing.Stemmer import Stemmer
from modules.text_processing.Normalizer import Normalizer
from helpers import constants

class QueryCompletion:

    def __init__(self, query, model, collection):
        self.query = query
        self.model = model
        self.collection = collection
        self.__stopword = None
        self.__normalizer = Normalizer()
        self.__stemmer = Stemmer()

    def getSuggestions(self, top_results = 5):
        clean_query = self.__cleanQuery()  # pre-process query

        script_dir = Path(__file__).parent.parent.parent
        bigram_json = ""

        if self.collection == constants.UO_CATALOG_COLLECTION:
            bigram_json = os.path.join(script_dir, 'data/bigram.json')

        elif self.collection == constants.REUTERS_COLLECTION:
            bigram_json = os.path.join(script_dir, 'data/reuters/bigram.json')

        # get the bigram of words
        if os.path.isfile(bigram_json):
            bigram = {}

            with open(bigram_json, "r+", encoding="utf-8") as json_file:
                bigram = json.load(json_file)

            lastWord = clean_query[len(clean_query) - 1]

            # return top 5 words as suggestions
            if lastWord in bigram:
                count = 0
                suggestions = []
                words_count = len(bigram[lastWord])

                for key in bigram[lastWord]:
                    if count < top_results and count < words_count:
                        if self.model == "Boolean":
                            suggestions.append(self.query + " AND " + key)
                        elif self.model == "VSM":
                            suggestions.append(self.query + " " + key)

                        count += 1
                    else:
                        break

                return suggestions
            else:
                return []

        else:
            print("Bigram does not exist")
            return []
    
    def __cleanQuery(self):
        q = self.query.split()

        for i in range(len(q)):
            if q[i] not in ["AND", "AND_NOT", "OR"]:
                # lower()
                q[i] = q[i].lower()

        # StopWords removal
        self.__stopword = Stopword().get_stop_words()

        for word in self.__stopword:
            q = [e for e in q if e not in word or e in ["AND", "AND_NOT", "OR"]]

        return q