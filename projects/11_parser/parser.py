import nltk
import sys

# spread across multiple lines for readability)

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


# N_decorate: adj adj .. n
# V_decorate: adv adv ... v adv adv ...
NONTERMINALS = """

S -> NP V_decorate | S ConjP

V_decorate ->  Adv V_decorate | VP | V_decorate Adv
ConjP -> Conj V_decorate | Conj S


NP -> N | Det N | N_decorate | Det N_decorate 
N_decorate -> Adj N | Adj N_decorate

PP -> P NP | PP PP
VP -> V | V NP | V PP | V NP PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        # get all possible parse tree
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    note:
        1. You may assume that sentence will be a string.
        2. You should use nltk's word_tokenize function to perform
           tokenization.
        3. Your function should return a list of words,
           where each word is a lowercased string.
        4. Any word that doesn't contain at least one alphabetic
           character (e.g. . or 28) should be excluded from the returned list.
    """
    # get all tokens
    words = nltk.word_tokenize(sentence)
    # remove the None alphabetic, and lower the char
    return [word.lower() for word in words if word.isalpha()]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    
    note:
        1. the input will be a nltk.tree object whose label is S
           (that is to say, the input will be a tree representing a sentence).
        2. Your function should return a list of nltk.tree objects,
           where each element has the label NP
    """
    res = []

    for sub_tree in tree.subtrees():
        if sub_tree.label() == "NP":
            res.append(sub_tree) 
    return res


if __name__ == "__main__":
    main()
