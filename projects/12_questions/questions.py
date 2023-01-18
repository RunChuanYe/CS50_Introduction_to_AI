import nltk
import sys
import os
import string
import math

# how many files, sentences should be matched for any given query.
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    
    file_idfs = compute_idfs(file_words)
    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)
    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string
    (the result of reading the corresonding file).

    note:
        1. Each key should be just the filename, without including the directory name.
           For example, if the directory is called corpus and contains files
           a.txt and b.txt, the keys should be a.txt and b.txt and not corpus/a.txt
           and corpus/b.txt.
    """
    res = {}
    for file_name in os.listdir(directory):
        with open(os.path.join(directory, file_name), encoding="utf-8") as f:
            res[str(file_name)] = f.read()
    return res

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    note:
        1. If a word appears multiple times in the document,
           it should also appear multiple times in the returned list
           (unless it was filtered out).
        2. Filter out punctuation and stopwords (common words that
           are unlikely to be useful for querying). Punctuation is defined
           as any character in string.punctuation (after you import string).
        3. Stopwords are defined as any word in nltk.corpus.stopwords.words("english").
    """
    # get all tokens
    words = nltk.word_tokenize(document.lower())
    # remove the None alphabetic, punctuation, stopwords, and lower the char
    return [word for word in words if word not in string.punctuation\
        and word not in nltk.corpus.stopwords.words("english")\
        and word.isalpha()]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.

    note:
        1. inverse document frequency of a word is defined by taking the natural logarithm
           of the number of documents divided by the number of documents in which
           the word appears.
    """
    # uing set for perf
    words_set = {
        document: set(documents[document])
        for document in documents
    }

    # get all word
    all_words = set()
    for document in words_set:
        all_words = all_words.union(words_set[document])

    # cal the IDF
    res = dict()
    for word in all_words:
        res[word] = 0
        for document in words_set:
            if word in words_set[document]:
                res[word] += 1
        res[word] = math.log(len(documents) / res[word])
    return res


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.

    note:
        1. The returned list of filenames should be of length n and
           should be ordered with the best match first.
        2. Files should be ranked according to the sum of tf-idf values for any word
           in the query that also appears in the file. Words
           in the query that do not appear in the file should not contribute
           to the file's score.
        3. Recall that tf-idf for a term is computed by multiplying the number of times
           the term appears in the document by the IDF value for that term.
    """
    rank_files = {}
    # for every file get the IDF
    for document in files:
        rank_files[document] = 0
        for word in query:
            count = files[document].count(word)
            if count:
                rank_files[document] += count * idfs[word]
    return [k for k, v in sorted(rank_files.items(), key=lambda item: item[1], reverse=True)][:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf.
    note: 
        1. If there are ties, preference should
           be given to sentences that have a higher query term density.
        2. Sentences should be ranked according to “matching word measure”:
           namely, the sum of IDF values for any word in the query that also appears
           in the sentence.
           Note that term frequency should not be taken into account here,
           only inverse document frequency.
        3. Query term density is defined as the proportion of words in the
           sentence that are also words in the query.
           For example, if a sentence has 10 words, 3 of which are in the query,
           then the sentence's query term density is 0.3.
    """
    rank_sentences = []
    # for every file get the IDF
    for sentence in sentences:
        sentence_idf = 0
        for word in query:
            # ever error
            if word in sentences[sentence]:
                sentence_idf += idfs[word]
        rank_sentences.append((sentence, sentence_idf))
    new_rank_sentences = []
    # get the density
    for sentence, idf in rank_sentences:
        sentence_density = 0
        for word in sentences[sentence]:
            sentence_density += 1 if word in query else 0
        sentence_density /= len(sentences[sentence])
        new_rank_sentences.append((sentence, idf, sentence_density))

    rank_sentences = sorted(new_rank_sentences, key=lambda x: (x[1], x[2]), reverse=True)

    return [res[0] for idx, res in enumerate(rank_sentences) if idx < n]    

if __name__ == "__main__":
    main()
