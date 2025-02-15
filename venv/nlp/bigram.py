import nltk
from nltk import bigrams, trigrams
from nltk.corpus import reuters
from collections import defaultdict


nltk.download('reuters')
nltk.download('punkt')


words = nltk.word_tokenize(' '.join(reuters.words()))

