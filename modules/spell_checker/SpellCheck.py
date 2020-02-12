# Name in diagram: spelling correction with weighted edit distance

from spellchecker import SpellChecker


class SpellCheck:

    def __init__(self):
        self.__spell_check = SpellChecker()
    '''
    This class creates an instance of the spell checking library and runs a spell check on the word and 
    the 2 argument is a boolean to turn on the sugestion for candidate words.
    '''

    def spell_checker(self, words, candidates=False):

        input_words = self.__spell_check.unknown(words.split())
        corrected_words = []
        for word in input_words:
            if(not candidates):
                corrected_words.append(self.__spell_check.correction(word))

            else:
                corrected_words.append(self.__spell_check.candidates(word))

        return corrected_words

# Test
# if __name__ == "__main__":
#     spell = SpellCheck()
#     sugg = spell.spell_checker("gaot goat")
#     sugg = spell.spell_checker("gaot goat", True)
#     print("suggestions are : \n", sugg)
