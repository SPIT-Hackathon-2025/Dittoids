

import nltk
import pandas as pd
from nltk.util import bigrams
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')

# selecting the corpus
corpus = """Competitive programming is a mentally stimulating activity where individuals or teams solve algorithmic and 
computational problems within a set time frame. It focuses on developing problem-solving skills and logical 
thinking by tackling complex challenges, often in the form of puzzles or coding exercises. Participants are 
expected to implement efficient solutions using programming languages like C++, Python, and Java. """

# tokenizing the text
tokens = nltk.word_tokenize(corpus)

# Creating bigrams
bigram_list = list(bigrams(tokens))

# frequency distribution of bigrams
cfd = ConditionalFreqDist(bigram_list)

# unigram frequencies
fdist = FreqDist(tokens)

# vocab size
vocab_size  = len(fdist)

# Calculate bigram probabilty
def calculate_bigram_probability(w1,w2,cfd,fdist):
  return cfd[w1][w2] / fdist[w1]

# calculate add one smoothing(Laplace Smoothing)
def add_one_smoothing(w1,w2,cfd,fdist,vocab_size):
  return (cfd[w1][w2]+1) / (fdist[w1]+vocab_size)

# Predicting next word using bigram probabilty
def predict_next_word(word,cfd,fdist):
  if word not in cfd:
    return None

  next_word = max(cfd[word],key= lambda x:calculate_bigram_probability(word,x,cfd,fdist))
  return next_word

# Predicting next word using add one smoothing(laplace smoothing)
def predict_next_word_smoothed(word,cfd,fdist,vocab_size):
  if word not in cfd:
    return None

  next_word = max(cfd[word],key=lambda x: add_one_smoothing(word,x,cfd,fdist,vocab_size))

  return next_word


# Print bigram probabilties
print("\nbigram Probabilities:")
for w1 in cfd:
  for w2 in cfd[w1]:
    prob = calculate_bigram_probability(w1,w2,cfd,fdist)
    print(f"P({w2} | {w1}) = {prob:.4f}")


# print probabilities using add one smoothing
print("\nbigram probabilities using add one smoothing")
for w1 in cfd:
  for w2 in cfd[w1]:
    prob = add_one_smoothing(w1,w2,cfd,fdist,vocab_size)
    print(f"P({w2} | {w1}) = {prob:.4f}")

# Predict next word without smoothing
word = "programming"
next_word = predict_next_word(word, cfd, fdist)
print(f"Next word after '{word}' (without smoothing): {next_word}")

# Predict next word with add-one smoothing
next_word_smoothed = predict_next_word_smoothed(word, cfd, fdist, vocab_size)
print(f"Next word after '{word}' (with add-one smoothing): {next_word_smoothed}")

