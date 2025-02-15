import nltk
from nltk.corpus import stopwords

text = """
Competitive programming is a mentally stimulating activity where individuals or teams solve algorithmic and 
computational problems within a set time frame. It focuses on developing problem-solving skills and logical 
thinking by tackling complex challenges, often in the form of puzzles or coding exercises. Participants are 
expected to implement efficient solutions using programming languages like C++, Python, and Java. 
The problems usually test a wide range of concepts, including data structures (e.g., arrays, trees, graphs), 
algorithms (sorting, searching, dynamic programming), and mathematical reasoning (combinatorics, number theory).

Competitive programming contests are organized globally, with popular platforms like Codeforces, LeetCode, 
HackerRank, and AtCoder hosting regular competitions. These contests are not just about writing correct code; 
they emphasize speed and efficiency. Problems often have multiple solutions with varying degrees of time and 
space complexity. Competitors must strive to optimize their code to meet constraints, such as processing 
large inputs in a limited amount of time or memory.

Participating in competitive programming improves one’s coding proficiency, enhances problem-solving 
abilities, and fosters a deeper understanding of algorithms and data structures. It is also a gateway to 
career opportunities in tech, as companies value the analytical and programming skills gained through such 
activities.
"""

words=text.lower().split()

stop_words = set(stopwords.words('english'))

for word in words:
    if word in stop_words:
        print(word,end=" ")

# print(" ".join(filtered_words))
