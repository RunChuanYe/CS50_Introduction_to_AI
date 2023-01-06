# CS50


# Proj

## 1_degrees

Using the **BFS** method, BFS is always guaranteed to be optimal.

Improv and Fix:

- check whether is target or not, before add node to the frontier
- before add node to the frontier, checking
    
    1. this node is not in the explored for **avoiding the endless loop**
    2. this node is not in the frontier for **avoiding the node.parent and node.action be update causing lenger path.**
- using backtracking for the shortest path
- be careful with `in` and `not in`
- Using `set, dict` other than `list` to **get better perf**

res:

![1673009165226](image/README/1673009165226.png)

# Test

A nice test framework: [CS50AI-test](https://github.com/jetkan-yk/cs50ai-test)

1. Install pytest:

    `conda install -c anaconda pytest`

2. Install pytest-repeat: 
   
    `conda install -c conda-forge pytest-repeat`

3. Clone repo:

    `git clone https://github.com/jetkan-yk/cs50ai-test`