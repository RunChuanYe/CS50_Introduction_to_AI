import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    # Using when if we know nothing about that person’s parents
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

# 2child or not
# num of gene the parent(father or mother has)
PROBS_FOR_GENE2CHILD = {
    True: {
        0: PROBS["mutation"],
        1: 0.5,
        2: 1 - PROBS["mutation"]
    },
    False: {
        0: 1 - PROBS["mutation"],
        1: 0.5,                 # 0.5 * (1 - PROBS["mutation"] + PROB["mutation"])
        2: PROBS["mutation"]
    }
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {

        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # get all people's name
    names = set(people)

    # Enumeration all possible cases given the fact (evidence)
    # Loop over all sets of people who might have the trait
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        # cond:
        #   1. all the people that have trait must be in the set
        #   2. 'None' trait people can be included in the set, but can be empty, some, all
        #   3. all the people that do not have trait must not be in the set  
        # filter all the sets satisfy cond
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                # p is just a scalar
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.

    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.

    empty cell for trait means we don't know whether the one has the trait or not.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def cal_prob_helper(people, curr_case, curr_person):
    """
    return prob for curr person
    """

    mother = people[curr_person]["mother"]
    father = people[curr_person]["father"]

    res = 1
    # cal gene
    if curr_case[curr_person]["gene"] == 0:
        res *= PROBS_FOR_GENE2CHILD[False][curr_case[mother]["gene"]] *\
                PROBS_FOR_GENE2CHILD[False][curr_case[father]["gene"]]
        res *= PROBS["trait"][0][True] if curr_case[curr_person]["trait"] else \
                PROBS["trait"][0][False]
    elif curr_case[curr_person]["gene"] == 1:
        tmp = PROBS_FOR_GENE2CHILD[True][curr_case[mother]["gene"]] *\
                PROBS_FOR_GENE2CHILD[False][curr_case[father]["gene"]]
        tmp += PROBS_FOR_GENE2CHILD[False][curr_case[mother]["gene"]] *\
                PROBS_FOR_GENE2CHILD[True][curr_case[father]["gene"]]
        res *= tmp
        res *= PROBS["trait"][1][True] if curr_case[curr_person]["trait"] else \
                PROBS["trait"][1][False]
    else:
        res *= PROBS_FOR_GENE2CHILD[True][curr_case[mother]["gene"]] *\
                PROBS_FOR_GENE2CHILD[True][curr_case[father]["gene"]]
        res *= PROBS["trait"][2][True] if curr_case[curr_person]["trait"] else \
                PROBS["trait"][2][False]
    return res

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.(all people with every field (num of gene copies,
    trait here) specific, then get a prob (scalar) called joint probability)

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
        
    For example, if the family consists of Harry, James, and Lily, 
        then calling this function where one_gene = {"Harry"}, two_genes = {"James"}, 
        and trait = {"Harry", "James"} should calculate the probability 
        that Lily has zero copies of the gene, Harry has one copy of the gene,
        James has two copies of the gene, Harry exhibits the trait,
        James exhibits the trait, and Lily does not exhibit the trait.
    note:
        1. You may assume that either mother and father are both blank
           (no parental information in the data set),
           or mother and father will both refer to other people in the people dictionary.
        2. For anyone with no parents listed in the data set,
           use the probability distribution PROBS["gene"] to
           determine the probability that they have a particular number of the gene.
        3. For anyone with parents in the data set,
           each parent will pass one of their two genes on to their child randomly,
           and there is a PROBS["mutation"] chance that it mutates 
           (goes from being the gene to not being the gene, or vice versa).
        4. Use the probability distribution PROBS["trait"] (conditional)
           to compute the probability that a person does or does not have a particular trait.
        5. Recall that to compute a joint probability of multiple events,
           you can do so by multiplying those probabilities together.
           But remember that for any child, the probability 
           of them having a certain number of genes is conditional 
           on what genes their parents have.
    """

    # cal num of gene copies first
    # then cal the trait for the trait is conditional on genes
    
    # cal people whose parent is None first.
    # then cal others

    # cal people whose parent is None
    res = 1
    curr_case = {
        name: {
            "gene": 1 if name in one_gene else 2 if name in two_genes else 0,
            "trait": True if name in have_trait else False
        }
        for name in people
    }
    for name in people:
        if people[name]["mother"] is not None:
            continue
        if name in one_gene:
            # gene prob
            res *= PROBS["gene"][1]
            # trait prob
            res *= PROBS["trait"][1][True] if name in have_trait \
                else PROBS["trait"][1][False]
        elif name in two_genes:
            res *= PROBS["gene"][2]
            res *= PROBS["trait"][2][True] if name in have_trait \
                else PROBS["trait"][2][False]
        else:
            res *= PROBS["gene"][0]
            res *= PROBS["trait"][0][True] if name in have_trait \
                else PROBS["trait"][0][False]
    
    # cal others
    for name in people:
        if people[name]["mother"] is None:
            continue
        res *= cal_prob_helper(people, curr_case, name)

    return res

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    
    note:
        1. simple addition is ok!
        2. For each person person in probabilities,
           the function should update the probabilities[person]["gene"] distribution
           and probabilities[person]["trait"] distribution
           by adding p to the appropriate value in each distribution.
           All other values should be left unchanged.
        3. p is just a scalar
        4. For example, if "Harry" were in both two_genes and in have_trait,
           then p would be added to probabilities["Harry"]["gene"][2] and
           to probabilities["Harry"]["trait"][True].
        5. The function should not return any value: 
           it just needs to update the probabilities dictionary.
    """
    curr_case = {
        name: {
            "gene": 1 if name in one_gene else 2 if name in two_genes else 0,
            "trait": True if name in have_trait else False
        }
        for name in probabilities
    }
    
    for name in probabilities:
        probabilities[name]["gene"][curr_case[name]["gene"]] += p
        probabilities[name]["trait"][curr_case[name]["trait"]] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).

    note:
        1. For example, if probabilities["Harry"]["trait"][True] were equal to 0.1
           and probabilities["Harry"]["trait"][False] were equal to 0.3,
           then your function should update the former value to be 0.25 
           and the latter value to be 0.75: the numbers now sum to 1, 
           and the latter value is still three times larger than the former value.
        2. The function should not return any value:
           it just needs to update the probabilities dictionary.
    """
    for name in probabilities:
        prob_sum = sum(probabilities[name]["gene"].values())
        for case in probabilities[name]["gene"]:
            probabilities[name]["gene"][case] /= prob_sum
        
        prob_sum = sum(probabilities[name]["trait"].values())
        for case in probabilities[name]["trait"]:
            probabilities[name]["trait"][case] /= prob_sum
        

if __name__ == "__main__":
    main()
