# 0.search

Finding a solution to a problem, like a navigator app that finds the **best** route from your origin to the destination, or like playing a game and figuring out the next move.

## 0.1 data struct

```c
struct node {
    state;
    parent_node;
    action_from_parent_node;
    path_cost;
}node;
```

## 0.2 algorithm

0. if the source == target, exit.

---

1. If the frontier is empty,

    Stop. There is no solution to the problem.

2. Remove a node from the frontier and add to exlored set.

3.  Expand the node (find all the new nodes that could be reached from this node)

    If the new node is the goal state,

    *   Return the solution. Stop.
    
    Else,

    * Add the new node to the frontier set.(**if the both frontier and explored set not contain this node**, else **endless loop** or **the node that has been added to the frontier set will be replace!**)

this method for the **BFS** is guaranteed to be **optimal**

## 0.3 DFS

Pros:
*    At best, this algorithm is the **fastest**. If it “lucks out” and always chooses the right path to the solution (by chance), then depth-first search takes the least possible time to get to a solution.

Cons:
*   It is possible that the found solution is **not optimal**.
*   At worst, this algorithm will explore every possible path before finding the solution, thus **taking the longest possible time** before reaching the solution.

## 0.4 BFS

Pros:
*   This algorithm is guaranteed to find the **optimal solution**.

Cons:

*   This algorithm is almost **guaranteed to take longer than the minimal time** to run.
*   At worst, this algorithm takes the **longest possible time** to run.

## 0.5 Greedy Best-First Search

However, it is important to emphasize that, as with any heuristic, it can go wrong and lead the algorithm down a slower path than it would have gone otherwise. It is possible that an **uninformed search algorithm will provide a better solution faster, but it is less likely to do so than an informed algorithm.**

**heuristic function** $h(n)$:
the function estimates **how close to the goal the next node is**, but it can be **mistaken**.

**Manhattan distance**: 
$d(x, y) = |x_1 - x_2| + |y_1 - y_2|$

## 0.6 A* Search

A development of the greedy best-first algorithm, A* search considers not only `f(n)`, the estimated cost from the current location to the goal, but also `g(n)`, the cost that was accrued until the current location.

For A* search to be **optimal**, the heuristic function, h(n), should be:

*   Admissible, or never overestimating the true cost, and
*   Consistent, which means that the estimated path cost to the goal of a new node in addition to the cost of transitioning to it from the previous node is greater or equal to the estimated path cost to the goal of the previous node. To put it in an equation form, h(n) is consistent if **for every node** n and successor node n’ with step cost c, `h(n) ≤ h(n’) + c`, **which means the h(n) is the shortest path's cost.**

## 0.7 Adversarial Search

Whereas, previously, we have discussed algorithms that need to find an answer to a question, in adversarial search the algorithm faces an opponent that tries to achieve the opposite goal. Often, AI that uses adversarial search is encountered in games, such as tic tac toe.

### 0.7.1 Minimax

both players **go all out**.

### 0.7.2 Alpha-Beta Pruning

A way to **optimize Minimax**, Alpha-Beta Pruning skips some of the recursive computations that are decidedly unfavorable. 

### 0.7.3 Depth-Limited Minimax

Depth-limited Minimax considers only a pre-defined number of moves before it stops, **without ever getting to a terminal state**. 

Depth-limited Minimax relies on an evaluation function that estimates the expected utility of the game from a given state, or, in other words, assigns values to states. 

The better the evaluation function, the better the Minimax algorithm that relies on it.