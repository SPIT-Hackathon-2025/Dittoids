import nltk
from collections import defaultdict
import numpy as np

nltk.download('punkt')

def tokenize_corpus(corpus):
    """Tokenizes the corpus into words and returns a list of sentences (tokenized)."""
    sentences = nltk.sent_tokenize(corpus.lower())
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    return tokenized_sentences

def build_bigram_counts(tokenized_sentences):
    """Builds bigram frequency table from tokenized sentences."""
    unigram_counts = defaultdict(int)
    bigram_counts = defaultdict(lambda: defaultdict(int))
    
    for sentence in tokenized_sentences:
        for i in range(len(sentence) - 1):
            unigram_counts[sentence[i]] += 1
            bigram_counts[sentence[i]][sentence[i + 1]] += 1
        unigram_counts[sentence[-1]] += 1  # Last word
    
    return unigram_counts, bigram_counts

def compute_bigram_probabilities(unigram_counts, bigram_counts):
    """Computes bigram probabilities without smoothing."""
    bigram_probs = {}
    for w1 in bigram_counts:
        bigram_probs[w1] = {}
        for w2 in bigram_counts[w1]:
            bigram_probs[w1][w2] = bigram_counts[w1][w2] / unigram_counts[w1]
    return bigram_probs

def compute_bigram_probabilities_smoothed(unigram_counts, bigram_counts, vocab_size):
    """Computes bigram probabilities using add-one smoothing."""
    bigram_probs_smoothed = {}
    for w1 in bigram_counts:
        bigram_probs_smoothed[w1] = {}
        for w2 in bigram_counts[w1]:
            bigram_probs_smoothed[w1][w2] = (bigram_counts[w1][w2] + 1) / (unigram_counts[w1] + vocab_size)
    return bigram_probs_smoothed

def sentence_probability(sentence, bigram_probs):
    """Calculates the probability of a sentence using bigram probabilities."""
    words = nltk.word_tokenize(sentence.lower())
    prob = 1.0
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if w1 in bigram_probs and w2 in bigram_probs[w1]:
            prob *= bigram_probs[w1][w2]
        else:
            return 0  # If any bigram is missing, probability is 0
    return prob

# Example Usage:
corpus = "I love NLP. NLP is fun and exciting. I love learning new things."
tokenized_sentences = tokenize_corpus(corpus)
unigram_counts, bigram_counts = build_bigram_counts(tokenized_sentences)
bigram_probs = compute_bigram_probabilities(unigram_counts, bigram_counts)
vocab_size = len(unigram_counts)
bigram_probs_smoothed = compute_bigram_probabilities_smoothed(unigram_counts, bigram_counts, vocab_size)

sentence = "I love NLP"
print("Probability (without smoothing):", sentence_probability(sentence, bigram_probs))
