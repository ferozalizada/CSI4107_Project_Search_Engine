
# Normalizer U.S.A -> USA and low-cost to lowcost
import re


class Normalizer:

    def __init__(self):
        print('created class')

    def normalize(self, word):
        # Lower case
        word = word.strip()
        word = re.sub('[^A-Za-z]+', '', word).lower()
        # converting numbers into words or removing numbers
        return word


# Test
wordnormalizer = Normalizer()

print(wordnormalizer.normalize(' US A'))
print(wordnormalizer.normalize('Us10'))
print(wordnormalizer.normalize('Usa-098710?'))
print(wordnormalizer.normalize('this is a 101 #$^&street'))


# https://medium.com/@datamonsters/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908
