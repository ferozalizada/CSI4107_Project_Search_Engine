import json
import os
from pathlib import Path

from helpers import constants
from modules.text_processing.Stopword import Stopword


# code inspired from https://www.analyticsvidhya.com/blog/2019/08/comprehensive-guide-language-model-nlp-python-code/
# https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

class BigramModel:

    def __init__(self, collection):
        script_dir = Path(__file__).parent.parent.parent
        corpus_json = ""
        bigram_json = ""

        if collection == constants.UO_CATALOG_COLLECTION:
            corpus_json = os.path.join(script_dir, 'data/uo_courses.json')
            bigram_json = os.path.join(script_dir, 'data/bigram.json')

        elif collection == constants.REUTERS_COLLECTION:
            corpus_json = os.path.join(script_dir, 'data/reuters/reuters.json')
            bigram_json = os.path.join(script_dir, 'data/reuters/bigram.json')

        # get the dictionary of words which are already pre-processed
        if os.path.isfile(corpus_json):
            corpus = {}

            with open(corpus_json, "r+", encoding="utf-8") as json_file:
                corpus = json.load(json_file)
            
            bigram = {}
            
            # list of stopwords
            stopword = Stopword().get_stop_words()
            punctuation = [".", ",", ";", ":", "?", "!", "{", "}", "(", ")", "[", "]", "<", ">", "\"", "\\", "/"]
            
            # building bigram  -- loop through the whole collection
            for doc in corpus["docs"]:
                title = doc["title"].split()
                description = doc["description"].split()

                for i in range(len(title)):
                    if i > 0:
                        word1 = title[i-1].lower()
                        word2 = title[i].lower()

                        # update frequency of co-occurrence
                        if word1 not in stopword and word2 not in stopword and word2[len(word2) -1] not in punctuation:
                            word1_start = 0
                            word1_end = len(word1)
                            word2_start = 0
                            word2_end = len(word2)

                            # remove punctuation
                            if word1[0] in punctuation:
                                word1_start = 1
                            
                            if word1[len(word1) -1] in punctuation:
                                word1_end -= 1
                            
                            if word2[0] in punctuation:
                                word2_start = 1
                            
                            if word2[len(word2) -1] in punctuation:
                                word2_end -= 1

                            key1 = word1[word1_start:word1_end]
                            key2 = word2[word2_start:word2_end]

                            if key1 in bigram:
                                if key2 in bigram[key1]:
                                    bigram[key1][key2] += 1
                                else:
                                    bigram[key1][key2] = 1
                            else:
                                bigram[key1] = {}
                                bigram[key1][key2] = 1
            
                for i in range(len(description)):
                    if i > 0:
                        word1 = description[i-1].lower()
                        word2 = description[i].lower()

                        # update frequency of co-occurrence
                        if word1 not in stopword and word2 not in stopword and word2[len(word2) -1] not in punctuation:
                            word1_start = 0
                            word1_end = len(word1)
                            word2_start = 0
                            word2_end = len(word2)

                            # remove punctuation
                            if word1[0] in punctuation:
                                word1_start = 1
                            
                            if word1[len(word1) -1] in punctuation:
                                word1_end -= 1
                            
                            if word2[0] in punctuation:
                                word2_start = 1
                            
                            if word2[len(word2) -1] in punctuation:
                                word2_end -= 1

                            key1 = word1[word1_start:word1_end]
                            key2 = word2[word2_start:word2_end]

                            if key1 in bigram:
                                if key2 in bigram[key1]:
                                    bigram[key1][key2] += 1
                                else:
                                    bigram[key1][key2] = 1
                            else:
                                bigram[key1] = {}
                                bigram[key1][key2] = 1

            final_bigram = {}
            min_treshold = 5

            for word1 in bigram:
                for word2 in bigram[word1]:
                    # keep words with co-occurrence frequency = 5
                    if bigram[word1][word2] >= min_treshold:
                        if word1 in final_bigram:
                            final_bigram[word1][word2] = bigram[word1][word2]
                        else:
                            final_bigram[word1] = {}
                            final_bigram[word1][word2] = bigram[word1][word2]

            sorted_bigram = {}

            # sort the words by frequency
            for key in final_bigram:
                for word2, freq in sorted(final_bigram[key].items(), key=lambda item: item[1], reverse=True):
                    if key in sorted_bigram:
                        sorted_bigram[key][word2] = freq
                    else:
                        sorted_bigram[key] = {}
                        sorted_bigram[key][word2] = freq

            with open(bigram_json, 'w', encoding="utf-8") as outfile:
                json.dump(sorted_bigram, outfile, indent=4)
        else:
            print("Cannot create bigram model: Corpus does not exist")