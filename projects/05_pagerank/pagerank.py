import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    #  hope that the output of these two functions 
    # should be similar when given the same corpus!
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.

    The keys in that dictionary represent pages (e.g., "2.html"),
    and the values of the dictionary are a set of all of the pages linked to by the key 
    (e.g. {"1.html", "3.html"}).
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # remove link from curr_page to itself
            # remove duplicate links using set
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the curr corpus(dict)
    # filename and link both are pages.key field
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    param:
        The corpus is a Python dictionary
        mapping a page name to a set of all pages linked to by that page.
        The page is a string representing which page the random surfer is currently on.

    Return a probability distribution over which page to visit next,
    given a current page.

    note: 
        With probability `damping_factor`, choose a link at random
        linked to by `page`. With probability `1 - damping_factor`, choose
        a link at random chosen from all pages in the corpus.

        The values in this returned probability distribution should sum to 1.
    """
    prob_distr = dict()

    page_num = len(corpus)
    if len(corpus[page]):
        # with probility `1 - damping_factor`
        for p in corpus:
            prob_distr[p] = 1 / page_num * (1 - damping_factor)

        # With probability `damping_factor`
        links_num = len(corpus[page])
        for p in corpus[page]:
            prob_distr[p] += 1 / links_num * damping_factor
    else:
        # not link case
        for p in corpus:
            prob_distr[p] = 1 / page_num

    return prob_distr

def generate_sample(transition_model):
    """
    return the next page
    """
    # key: page_name, value: range for curr page
    page_range = dict()
    curr_range = 0
    for p in transition_model:
        curr_range += transition_model[p]
        page_range[p] = curr_range

    # get random float from [0.0, 1.0)
    random_sample = random.random()

    # get page name that includes the random_sample
    res = None
    for p in page_range:
        if page_range[p] > random_sample:
            if res is None:
                res = p
                continue
            if page_range[res] > page_range[p]:
                res = p
    return res

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # get all transiton_models 
    transition_models = dict()
    for p in corpus:
        transition_models[p] = transition_model(corpus, p, damping_factor)

    # start a page by random
    page = list(corpus.keys())[random.randrange(len(corpus))]

    # init the samples count
    samples = dict()
    for p in corpus:
        samples[p] = 0
    samples[page] += 1
    # samping
    # [0, n)
    for i in range(n-1):
        page = generate_sample(transition_models[page])
        samples[page] += 1

    res = dict()

    for page in corpus:
        res[page] = samples[page] / n
    return res

def check_threshold(curr_res, last_res, threshold):
    """
    return true if all(|curr_res - last_res| < threshold)
    otherwise return false
    """
    for p in curr_res:
        if abs(curr_res[p] - last_res[p]) >= threshold / 2:
            return False

    return True

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # assigning each page a rank of 1 / N,
    # where N is the total number of pages in the corpus.
    res = dict()
    page_num = len(corpus)
    for p in corpus:
        res[p] = 1 / page_num


    # init the threadhold
    # repeat until no PageRank 
    # value changes by more than 0.001 between the current rank values and the new rank values.
    threshold = 0.001

    # iterate
    # A page that has no links at all
    # should be interpreted as having one link for every page in the corpus
    # (including itself).
    while True:
        last_pg = res
        res = dict()
        for target_p in corpus:
            res[target_p] = (1 - damping_factor) / page_num
            for from_p in corpus:
                if target_p in corpus[from_p]:
                    # not empty in corpus[from_p]
                    link_num = len(corpus[from_p])
                    res[target_p] += damping_factor / link_num * last_pg[from_p]
                elif len(corpus[from_p]) == 0:
                    # treat it link to all other pages
                    res[target_p] += damping_factor / page_num * last_pg[from_p]
        if check_threshold(res, last_pg, threshold):
            break
    return res

if __name__ == "__main__":
    main()
