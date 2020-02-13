# Name in diagram: dictionary building

from stop_words import get_stop_words


class Dictionary:

    stop_words = None

    def __init__(self):
        self.stop_words = get_stop_words('en')

        # https: // pypi.org/project/stop-words/
s = Dictionary()
print(s.stop_words)
