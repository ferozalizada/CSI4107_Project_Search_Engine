# Name in diagram: Lemmatizer building

from nltk.stem import PorterStemmer


class Lemmatizer:

    # __stop_words = None
    __stemmer = None

    def __init__(self):
        self.__stop_words = stopwords
        self.__stemmer = PorterStemmer()

    # def get_stop_words(self):
    #     return self.__stop_words

    def stem_word(self, word):
        list_of_stemmed_words = []
        try:
            return self.__stemmer.stem(word)
        except:
            if(isinstance(word, list)):
                for index in word:
                    list_of_stemmed_words.append(self.__stemmer.stem(index))
                return list_of_stemmed_words


# Tests
# s = Lemmatizer()
# print('list of stop words: \n')
# print(s.get_stop_words())

# print('list of stop with one word: \n')
# word = "stopping"
# print(f'\n Stemming:  {word}  =>  ', s.stem_word(word))

# print('list of stop with one word: \n')
# word_list = ["friend", "friendship", "friends", "friendships", "stabil",
#              "destabilize", "misunderstanding", "railroad", "moonlight", "football"]
# print(f'\n Stemming:  \n{word_list}  =>  \n', s.stem_word(word_list))

# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
