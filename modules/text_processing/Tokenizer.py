# TODO: do we need tokenizers?

import re


class Tokenizer:
    def word_tokenizer(self, word):
        return word.split(" ")

    def sentence_tokenizer(self, word):
        return re.compile(r'([A-Za-z0-9][^\.!?]*[\.!?]*)', re.M).findall(word)


# token = Tokenizer()
# print(token.word_tokenizer('THis is A search engine. THat does usual stuff.'))
# print(token.sentence_tokenizer(
#     'THis is A search engine. THat does usual stuff 1 year ago. Ok this is good'))
