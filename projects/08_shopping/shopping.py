import sys
import csv

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# 12330 * 0.4 for test
TEST_SIZE = 0.4


ENCODE_MONTH = {
    month: idx
    for idx, month in enumerate(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 
                                 'Sep', 'Oct', 'Nov', 'Dec'])
}

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.

    note:
        1. The lists should be ordered according to 
          the order the users appear in the spreadsheet.
        2. need to tramsiform the data to fit the spec
        3. Note that, to build a nearest-neighbor classifier,
           all of our data needs to be numeric.
        4. Administrative, Informational, ProductRelated, Month,
           OperatingSystems, Browser, Region, TrafficType, VisitorType,
           and Weekend should all be of type int (Using int() for typecast)

           TODO: Month, VisitorType, Weekend
        5. Administrative_Duration, Informational_Duration, ProductRelated_Duration,
           BounceRates, ExitRates, PageValues, and SpecialDay should all be of type float.
           (Using float() for typecast)

           TODO: None
        6. Month should be 0 for January, 1 for February, 2 for March,
           etc. up to 11 for December.

           VisitorType should be 1 for returning visitors and 0 for non-returning visitors.

           Weekend should be 1 if the user visited on a weekend and 0 otherwise.
        7. Each value of labels should either be the integer 1,
           if the user did go through with a purchase, or 0 otherwise.
        8. For example, the value of the first evidence list should be
           [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0]
           and the value of the first label should be 0.
    """
    # need to tramsiform the data to fit the spec

    evidences = []
    labels = []
    with open(filename) as f:
        reader = csv.reader(f)
        # pass the first line, (header)
        next(reader)
        for row in reader:
            evidence =[]
            # note the data type is str for all col.
            labels.append(1 if row[-1] == 'TRUE' else 0)
            # 'Administrative', 'Administrative_Duration',
            evidence.append(int(row[0]))
            evidence.append(float(row[1]))
            # 'Informational', 'Informational_Duration',
            evidence.append(int(row[2]))
            evidence.append(float(row[3]))
            # 'ProductRelated', 'ProductRelated_Duration'
            evidence.append(int(row[4]))
            evidence.append(float(row[5]))

            # 'BounceRates', 'ExitRates', 'PageValues', 'SpecialDay',
            evidence.append(float(row[6]))
            evidence.append(float(row[7]))
            evidence.append(float(row[8]))
            evidence.append(float(row[9]))

            # Month
            evidence.append(ENCODE_MONTH[row[10][:3]])

            # 'OperatingSystems', 'Browser', 'Region', 'TrafficType'
            evidence.append(int(row[11]))
            evidence.append(int(row[12]))
            evidence.append(int(row[13]))
            evidence.append(int(row[14]))

            # VisitorType
            evidence.append(1 if row[15] == 'Returning_Visitor' else 0)

            # Weekend
            evidence.append(1 if row[16] == 'TRUE' else 0)
            
            evidences.append(evidence)

    return (evidences, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return 
    a scikit-learn nearest-neighbor classifier 
    (a k-nearest-neighbor classifier where k = 1) fitted on that training data.
    """

    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return two floating-point values (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.

    note:
        You may assume that the list of true labels will contain
        at least one positive label and at least one negative label.
    """
    # init
    sensitivity, specificity = (0, 0)
    total_posi, total_nega = (0, 0)

    for label, pred in zip(labels, predictions):
        if label:
            total_posi += 1
            if pred:
                sensitivity += 1
        else:
            total_nega += 1
            if not pred:
                specificity += 1
    sensitivity = sensitivity / total_posi if total_posi else 0.0
    specificity = specificity / total_nega if total_nega else 0.0
    return (sensitivity, specificity)
    
if __name__ == "__main__":
    main()
