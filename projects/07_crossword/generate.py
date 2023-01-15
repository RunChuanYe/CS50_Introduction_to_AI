import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # remove the words whose len != variable's len
        for variable in self.crossword.variables:
            new_domain = set()
            for word in self.domains[variable]:
                if len(word) == variable.length:
                    new_domain.add(word)
            self.domains[variable] = new_domain

    def check_char_conflict(self, x_idx, y_idx, x_val, y_domain):
        """
        x_val: string
        y_domain: string set
        if x_val[x_idx] == any(y_domain - x_val)[y_idx]
        return false, otherwise, return true
        """
        for y_val in y_domain - set(x_val):
            if y_val[y_idx] == x_val[x_idx]:
                return False
        return True

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no

        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        note:
            1. A conflict in the context of the crossword puzzle 
               is a square for which two variables disagree on
               what character value it should take on
            2. (x, y) must be in the crossword.overlaps.keys()
        """
        new_domain = set()
        modify = False

        x_idx, y_idx = self.crossword.overlaps[x, y]
        y_domain = self.domains[y]
        for val in self.domains[x]:
            if self.check_char_conflict(x_idx, y_idx, val, y_domain):
                modify = True
            else:
                new_domain.add(val)
        if modify:
            self.domains[x] = new_domain
            return True

        return False            


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        1. where each arc is a tuple (x, y) of a variable x and a different variable y.
            arcs is a list
        2. do not need to worry about enforcing word uniqueness in this function
           (you'll implement that check in the consistent function.)

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If `arcs` is None, begin with initial list of all arcs in the problem.
        # all arcs include both the (var1, var2) and (var2, var1)
        if arcs is None:
            overlaps = {
                key: self.crossword.overlaps[key]
                for key in self.crossword.overlaps.keys()
                if self.crossword.overlaps[key] is not None
            }
            arcs = list(overlaps.keys())


        while len(arcs) != 0:
            x, y = arcs[0]
            arcs = arcs[1:]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for variable in (self.crossword.neighbors(x) - {y}):
                    # why (variable, x) ? other than (x, variable) ?
                    # for next tie the variable's domain, not x's
                    arcs.append((variable, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.

        note:
            1. regardless of what that value is
            2. assignment: {variable: words, ...}
        """

        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        note: 
            1. words fit in crossword puzzle without conflicting characters
            2. not duplicate words
            3. Note that the assignment may not be complete:
               not all variables will necessarily be present in the assignment.
            4. ignore the length check
        """
        # not duplicate words
        if len(set(assignment.values())) < len(assignment.keys()):
            return False
        
        # words fit in crossword puzzle without conflicting characters
        for overlap in self.crossword.overlaps:
            if self.crossword.overlaps[overlap] is None:
                continue
            if overlap[0] in assignment and overlap[1] in assignment:
                x_idx, y_idx = self.crossword.overlaps[overlap]
                if self.check_char_conflict(x_idx, y_idx,\
                    assignment[overlap[0]], {assignment[overlap[1]]}):
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        return a list of all of the values in the domain of var,
        ordered according to the least-constraining values heuristic

        note:
            1. Recall that the least-constraining values heuristic is computed 
               as the number of values ruled out for neighboring unassigned variables.
               That is to say, if assigning var to a particular value results in
               eliminating n possible choices for neighboring variables,
               you should order your results in ascending order of n
            2. any variable present in assignment already has a value, and therefore shouldn't 
               be counted when computing the number of values ruled out for neighboring
               unassigned variables.
            3. For domain values that eliminate the same number of possible choices for neighboring 
               variables, any ordering is acceptable.
            4. the same word should be removed too, count it in
        """

        # using a dict to store the "heuristic"
        h = dict()
        neighbors = self.crossword.neighbors(var)
        for x_val in self.domains[var]:
            h[x_val] = 0
            for neighbor in neighbors:
                # already assigned
                if neighbor in assignment:
                    continue
                # iterator the neighbor's domain
                for neighbor_val in self.domains[neighbor]:
                    if neighbor_val == x_val:
                        h[x_val] += 1
                        continue
                    x_idx, y_idx = self.crossword.overlaps[var, neighbor]
                    if self.check_char_conflict(x_idx, y_idx, x_val, {neighbor_val}):
                        h[x_val] += 1

        # get the ordered list of val in the order of h increasing
        # return sorted(h)
        return [k for k, v in sorted(h.items(), key=lambda item: item[1])]
        # return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. 
        If there is a tie, choose the variable with the highest
        degree (has the most neighbors).
        If there is a tie, any of the tied variables are acceptable
        return values.
        
        note: 
            1. You may assume that the assignment will not be complete:
               not all variables will be present in the assignment.
        """
        remain_vars = set(self.crossword.variables) - set(assignment)
        
        # onlu one var remaining, return it
        if len(remain_vars) == 1:
            return list(remain_vars)[0]
        # num of vars >= 2 
        
        # https://www.adamsmith.haus/python/answers/how-to-sort-by-two-keys-in-python
        # using sorted specific two key

        h_func = [
            (var, len(self.domains[var]), len(self.crossword.neighbors(var)))
            for var in remain_vars
        ]
        
        sorted_h_func = sorted(h_func, key= lambda x: (x[1], x[2]))

        return sorted_h_func[0][0]


    def inference_assign(self, assignment):
        """
        return a list of tuple
        where a tuple is a (var, val) pair
        mean that in the curr assignment, the var has only one choice, that is val
        """

        res = []
        remain_vars = set(self.crossword.variables) - set(assignment)
        assigned_vars = set(assignment)
        # check all remain_vars if any of them has only one choice
        for remain_var in remain_vars:
            remain_vals = list(self.domains[remain_var])
            for neighbor in self.crossword.neighbors(remain_var):
                if neighbor in assigned_vars:
                    new_remain_vals = []
                    val_neighbor = assignment[neighbor]
                    # neighbor must overlap
                    x_idx, y_idx = self.crossword.overlaps[remain_var, neighbor]
                    for val_curr_var in remain_vals:
                        # remove conflict assignment
                        if self.check_char_conflict(x_idx, y_idx, val_curr_var, {val_neighbor}):
                            continue
                        new_remain_vals.append(val_curr_var)
                    remain_vals = new_remain_vals
            if len(remain_vals) == 1:
                res.append((remain_var, remain_vals[0]))
            # for the impossible assignment, stop curr backtrace used in the backtrace func.
            if len(remain_vals) == 0:
                res.append((remain_var, None))
        return res

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        your algorithm is more efficient if you interleave search with inference (as by maintaining arc consistency every time you make a new assignment
        """

        # ever error
        if self.assignment_complete(assignment):
            return assignment

        # select curr var
        curr_var = self.select_unassigned_variable(assignment)
        vals = self.order_domain_values(curr_var, assignment)
        for val in vals:
            assignment[curr_var] = val
            if self.consistent(assignment):

                inferences = self.inference_assign(assignment)
                if len(inferences):
                    # conflict assignment
                    if any(assign[1] is None for assign in inferences):
                        del assignment[curr_var]
                        continue

                    for k, v in inferences:
                        assignment[k] = v

                if self.backtrack(assignment) is not None:
                    return assignment

                if len(inferences):
                    for k, v in inferences:
                        del assignment[k]

            # ever error
            del assignment[curr_var]
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
