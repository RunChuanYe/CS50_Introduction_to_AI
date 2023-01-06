class Node():
    """
    state: curr_people_id
    parent: last_people_id
    action: movie_id in which both of state and parent star
    """
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []          # node
        self.exploreds = {}      # node.state: node
        self.frontier_ids = set()

    def add_to_frontier(self, node):
        # safe
        # else form a loop
        if node.state not in self.exploreds.keys() and node.state not in self.frontier_ids:
            self.frontier.append(node)
            self.frontier_ids.add(node.state)

    def add_to_explored(self, node):
        self.exploreds[node.state] = node

    def is_target(self, node, target):
        return node.state == target

    def get_node_explored_by_id(self, id):
        return self.exploreds.get(id, None)

    def empty_frontier(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty_frontier():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            self.frontier_ids.remove(node.state)
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty_frontier():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            self.frontier_ids.remove(node.state)
            return node

if __name__ == "__main__":
    node1 = Node(1, 1, 1)
    node2 = Node(1, 1, 1)

    nodes = set([node2])
    print(node1 in nodes)

    nodes.add(node1)
    print(nodes)

    li = [1, 2, 3, 4, 5]
    li.reverse()
    print(li)