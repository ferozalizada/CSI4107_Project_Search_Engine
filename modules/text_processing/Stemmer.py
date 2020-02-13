# Name in diagram: dictionary building
from nltk import PorterStemmer

from nltk.stem import PorterStemmer


class Stemmer:

    __stemmer = None

    def __init__(self):
        self.__stemmer = PorterStemmer()

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
s = Stemmer()

print('list of stop with one word: \n')
word = "stopping"
print(f'\n Stemming:  {word}  =>  ', s.stem_word(word))

# print('list of stop with one word: \n')
# word_list = ["friend", "friendship", "friends", "friendships", "stabil",
#              "destabilize", "misunderstanding", "railroad", "moonlight", "football"]
# print(f'\n Stemming:  \n{word_list}  =>  \n', s.stem_word(word_list))

# https: // pypi.org/project/stop-words/
# https://www.datacamp.com/community/tutorials/stemming-lemmatization-python
