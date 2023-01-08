# CS50


# Proj

## 00_pkg

Install all pkg needed to setup.

run:

1. `conda env create -f .\package-list.yaml`

    Using defaul env name: `cs50`

    **Or**

    `conda env create -f .\package-list.yaml -n <new_env_name>`

    Specific the env name

2. **make sure new env is used**

**please ignore other pkg install, if you have run above.**

## 01_degrees

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

## 02_tic_tac_toe

### 02.1 pkg install

Install pygame: **(Upgrade and just for curr user)**

`python -m pip install -U pygame --user`

test: 

`python -m pygame.examples.aliens`

Uninstall pygame:

`python -m pip uninstall pygame`

ref: [pygame.org](https://www.pygame.org/wiki/GettingStarted)

Or Using `conda` **Recommanded**

1. `conda env create -f .\package-list.yaml`

    Using defaul env name: `cs50`

    **Or**

    `conda env create -f .\package-list.yaml -n <new_env_name>`

    Specific the env name

2. **make sure new env is used**


### 02.2 details

- Using `copy.deepcopy()`

- **Since Tic-Tac-Toe is a tie given optimal play by both sides, you should never be able to beat the AI (though if you don’t play optimally as well, it may beat you!)**

- Alpha-beta pruning is optional, but may make your AI run more efficiently!

res:

![1673177070388](image/README/1673177070388.png)

res: (**Using Alpha-Beta Pruning**)

![1673179781373](image/README/1673179781373.png)

# Test

A nice test framework: [CS50AI-test](https://github.com/jetkan-yk/cs50ai-test)

1. Install pytest:

    `conda install -c anaconda pytest`

2. Install pytest-repeat: 
   
    `conda install -c conda-forge pytest-repeat`

3. Clone repo:

    `git clone https://github.com/jetkan-yk/cs50ai-test`

4. more detail, see [CS50AI-test](https://github.com/jetkan-yk/cs50ai-test)