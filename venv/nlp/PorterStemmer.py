import re

def is_consonant(word, i):
    vowels = "aeiou"
    if word[i] in vowels:
        return False
    if word[i] == 'y':
        return i == 0 or not is_consonant(word, i - 1)
    return True

def measure(word):
    pattern = re.compile(r"[^aeiou]*[aeiou]+[^aeiou]")
    return len(pattern.findall(word))

def contains_vowel(word):
    return any(c in "aeiou" for c in word)

def ends_with_double_consonant(word):
    return len(word) > 1 and word[-1] == word[-2] and is_consonant(word, -1)

def cvc(word):
    if len(word) < 3:
        return False
    return (is_consonant(word, -1) and not is_consonant(word, -2) and is_consonant(word, -3) and
            word[-1] not in "wxy")

def replace_suffix(word, suffix, replacement, condition=True):
    if word.endswith(suffix) and condition:
        return word[: -len(suffix)] + replacement
    return word

def porter_stemmer(word):
    if len(word) <= 2:
        return word
    
    word = replace_suffix(word, "sses", "ss")
    word = replace_suffix(word, "ies", "i")
    word = replace_suffix(word, "ss", "ss")
    word = replace_suffix(word, "s", "")
    
    if word.endswith("eed"):
        if measure(word[:-3]) > 0:
            word = word[:-1]
    elif (word.endswith("ed") or word.endswith("ing")) and contains_vowel(word[:-2]):
        word = word[:-2] if word.endswith("ed") else word[:-3]
        word = replace_suffix(word, "at", "ate")
        word = replace_suffix(word, "bl", "ble")
        word = replace_suffix(word, "iz", "ize")
        if ends_with_double_consonant(word) and word[-1] not in "lsz":
            word = word[:-1]
        elif measure(word) == 1 and cvc(word):
            word += "e"
    
    if word.endswith("y") and contains_vowel(word[:-1]):
        word = word[:-1] + "i"
    
    step2_suffixes = {
        "ational": "ate", "tional": "tion", "enci": "ence", "anci": "ance",
        "izer": "ize", "abli": "able", "alli": "al", "entli": "ent",
        "eli": "e", "ousli": "ous", "ization": "ize", "ation": "ate",
        "ator": "ate", "alism": "al", "iveness": "ive", "fulness": "ful",
        "ousness": "ous", "aliti": "al", "iviti": "ive", "biliti": "ble"
    }
    for suffix, replacement in step2_suffixes.items():
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 0:
            word = replace_suffix(word, suffix, replacement)
            break
    
    step3_suffixes = {"icate": "ic", "ative": "", "alize": "al", "iciti": "ic", "ical": "ic", "ful": "", "ness": ""}
    for suffix, replacement in step3_suffixes.items():
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 0:
            word = replace_suffix(word, suffix, replacement)
            break
    
    step4_suffixes = ["al", "ance", "ence", "er", "ic", "able", "ible", "ant", "ement", "ment", "ent", "ion", "ou", "ism", "ate", "iti", "ous", "ive", "ize"]
    for suffix in step4_suffixes:
        if word.endswith(suffix) and measure(word[:-len(suffix)]) > 1:
            word = word[:-len(suffix)]
            break
    
    if word.endswith("e") and (measure(word[:-1]) > 1 or (measure(word[:-1]) == 1 and not cvc(word[:-1]))):
        word = word[:-1]
    
    if ends_with_double_consonant(word) and measure(word) > 1 and word.endswith("l"):
        word = word[:-1]
    
    return word


from nltk.corpus import stopwords

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


for word in words:
    print(f"{word} -> {porter_stemmer(word)}")


