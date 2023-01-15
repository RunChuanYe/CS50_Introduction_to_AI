import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation

    Notice that each cell is a pair (i, j) 
    where i is the row number (ranging from 0 to height - 1) 
    and j is the column number (ranging from 0 to width - 1).
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def __hash__(self):
        tmp = [cell for cell in self.cells]
        tmp.sort()
        return hash((*tmp, self.count))

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            # for the use of loop end
            return True
        return False

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            # for the use of loop end
            return True
        return False


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def mark_safe_or_mine(self):
        """
        if the knowledge change, then loop again
        else end loop
        """
        change = True
        while change:
            change = False
            for sentense in self.knowledge:
                if len(sentense.cells) == 0:
                    continue
                if sentense.known_safes():
                    change = True
                    safe_set = sentense.known_safes().copy()
                    for c in safe_set:
                        self.mark_safe(c)

                if sentense.known_mines():
                    change = True
                    mine_set = sentense.known_mines().copy()
                    for c in mine_set:
                        self.mark_mine(c)

    def expand_KB(self):
        while True:
            new_knowledge = set()
            remove = set()
            # remove same knowledge (e.g. empty knowledge, and speed up using set)
            self_knowledge_tmp = set(self.knowledge)
            for i in range(len(self.knowledge)):
                # remove empty knowledge
                if len(self.knowledge[i].cells) == 0:
                    remove.add(self.knowledge[i])
                    continue
                for j in range(len(self.knowledge)):
                    # remove empty knowledge
                    if len(self.knowledge[j].cells) == 0:
                        remove.add(self.knowledge[j])
                        continue
                    # get new knowledge
                    if self.knowledge[i].cells < self.knowledge[j].cells:
                        new_sentense = Sentence(self.knowledge[j].cells - self.knowledge[i].cells,\
                            self.knowledge[j].count - self.knowledge[i].count)
                        if new_sentense not in self_knowledge_tmp:
                            new_knowledge.add(new_sentense)

                

            # remove empty knowledge 
            # produced in the mark
            for sentense in remove:
                self_knowledge_tmp.remove(sentense)

            self.knowledge = list(self_knowledge_tmp)

            # empty new knowledge inferenced
            if len(new_knowledge) == 0:
                break

            # add new knowledge
            for k in new_knowledge:
                self.knowledge.append(k)

            # refactor the KB
            self.mark_safe_or_mine()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # 2) mark the cell as safe

        # this cell is removed from the knowledge forever
        # even in the inference
        self.mark_safe(cell)
        
        # do not miss this
        # for cell in self.moves_made:
        #     self.mark_safe(cell)


        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`
        neighbor_cells = []
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                # simple
                # only include cells whose state is still undetermined in the sentence.
                if (i, j) in self.safes:    # include move has made
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cells.append((i, j))
        self.knowledge.append(Sentence(neighbor_cells, count))


        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        self.mark_safe_or_mine()

        # 5) add any new sentences to the AI's knowledge base
        #     if they can be inferred from existing knowledge
        #     should not remove the bigger set!
        self.expand_KB()



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.

        return a move in safe and not choosen
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
            
        return a move not in self.mines and not choosen
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and\
                    (i, j) not in self.moves_made:
                    return (i, j)

        return None

if __name__ == "__main__": 

    # hash is order sentisitive
    empty_sentense1 = Sentence([], 0)
    empty_sentense2 = Sentence([], 0)

    empty_sentense1.cells = {'1597', '1697', '144'}
    empty_sentense1.cells.add('705')
    empty_sentense2.cells = {'705', '1697', '144'}
    empty_sentense2.cells.add('1597')

    print(empty_sentense1.cells)
    print(empty_sentense2.cells)

    print(hash(empty_sentense1) == hash(empty_sentense2))
    print(empty_sentense1 == empty_sentense2)

    empty_sentense2.cells.remove('705')
    li1 = [empty_sentense2, empty_sentense1]
    li2 = [empty_sentense1, empty_sentense2]
    print(li1 == li2)