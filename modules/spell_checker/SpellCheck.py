# Name in diagram: spelling correction with weighted edit distance

from spellchecker import SpellChecker


class SpellCheck:

    def __init__(self):
        self.__spell_check = SpellChecker()

    def create_dictionary(self, path):
        self.__spell_check = SpellChecker(language=None, case_sensitive=False)
        self.__spell_check.word_frequency.load_dictionary(path)

    """
    This class creates an instance of the spell checking library and runs a spell check on the word and 
    the 2 argument is a boolean to turn on the sugestion for candidate words.
    """

    def spell_checker(self, words, candidates=False):

        input_words = self.__spell_check.unknown(words.split())
        corrected_words = []
        for word in input_words:
            if(not candidates):
                corrected_words.append(self.__spell_check.correction(word))
            else:
                corrected_words.append(self.__spell_check.candidates(word))

        return corrected_words

    def find_weighted_distance(self, word):
        spellchecker(word)

    # def edit_distance(self, word):

        # word = ENSURE_UNICODE(word).lower(
        # ) if not self._case_sensitive else ENSURE_UNICODE(word)
        # if self._check_if_should_check(word) is False:
        #     return {word}
        # letters = self._word_frequency.letters
        # splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        # deletes = [L + R[1:] for L, R in splits if R]
        # transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        # replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        # inserts = [L + c + R for L, R in splits for c in letters]
        # return set(deletes + transposes + replaces + inserts)


if __name__ == "__main__":
    spell = SpellCheck()
    sugg = spell.spell_checker("thi sis gaot goat")
    print("Spell check are : \n", sugg, "\n")
    # sugg = spell.spell_checker("gaot goat", True)
    # print("suggestions are : \n", sugg, "\n")
# TODO: edit distance
