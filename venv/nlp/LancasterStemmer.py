from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords

stemmer = LancasterStemmer()

para="""
Competitive programming is a mentally stimulating activity where individuals or teams solve algorithmic and 
computational problems within a set time frame. It focuses on developing problem-solving skills and logical 
thinking by tackling complex challenges, often in the form of puzzles or coding exercises. Participants are 
expected to implement efficient solutions using programming languages like C++, Python, and Java. 
The problems usually test a wide range of concepts, including data structures (e.g., arrays, trees, graphs), 
algorithms (sorting, searching, dynamic programming), and mathematical reasoning (combinatorics, number theory).
"""

words=para.replace(","," ").replace('-'," ").replace("."," ").replace("("," ").replace(")"," ").lower().split()
stop_words = set(stopwords.words('english'))
stemmed_words = [stemmer.stem(word) for word in words]

for i in range(0,len(words)):
    print(words[i]+" -> "+stemmed_words[i])
