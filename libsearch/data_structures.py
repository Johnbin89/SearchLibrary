from dataclasses import InitVar, dataclass, field
from typing import Any, Optional


# eq=False keeps identity hashing: nodes are used as dict keys by the priority queue.
@dataclass(eq=False)
class Node:
    """
    A node of the search tree, used in blind search.
    Tracks:
    - depth: number of steps from the root.
    """

    state: Any
    parent: Optional["Node"] = field(default=None, repr=False)
    action: Any = None
    depth: int = field(init=False)

    def __post_init__(self):
        self.depth = self.parent.depth + 1 if self.parent else 0

    def path(self):
        """Return (actions, states) from the root to this node, root excluded."""
        actions, states, node = [], [], self
        while node.parent is not None:
            actions.append(node.action)
            states.append(node.state)
            node = node.parent
        actions.reverse()
        states.reverse()
        return actions, states


@dataclass(eq=False)
class CostNode(Node):
    """
    A node that keeps the cost of the path from the root.
    Tracks:
    - cost_from_start (g): the parent's cost_from_start plus step_cost, the cost of the edge
      parent -> self. step_cost defaults to 1 (ex. moving on next tile in a maze) and is set
      per edge in weighted graphs (ex. branch_and_bound).
    """

    parent: Optional["CostNode"] = field(default=None, repr=False)
    step_cost: InitVar[float] = 1
    cost_from_start: float = field(init=False)

    def __post_init__(self, step_cost):
        super().__post_init__()
        self.cost_from_start = self.parent.cost_from_start + step_cost if self.parent else 0


@dataclass(eq=False)
class HeuristicNode(CostNode):
    """
    A node that keeps a heuristic estimate too. Used in informed search.
    Tracks:
    - estimated_cost (h): estimated cost from this node to the goal, calculated by a heuristic function.
    - total_cost (f): cost_from_start + estimated_cost, the estimated cost of the full path to goal through this node.
    """

    estimated_cost: float = 0

    @property
    def total_cost(self):
        return self.cost_from_start + self.estimated_cost


from collections import deque


class StackFrontier:
    def __init__(self):
        self.frontier = deque()

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def contains_node(self, action, state):
        return any(node.state == state and node.action == action for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def len(self):
        return len(self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop()

    def contents(self):
        for node in self.frontier:
            print("Action: {}, State: {}".format(node.action, node.state))


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.popleft()


import itertools
from heapq import heappop, heappush
from queue import PriorityQueue


class ModPriorityQueue(PriorityQueue):
    """
    https://docs.python.org/2/library/heapq.html#priority-queue-implementation-notes
    """

    def _init(self, maxsize):
        self.queue = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = "<removed-task>"  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task, priority: float = 0):
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = (priority, count, task)
        print("entry: {}".format(entry))
        self.entry_finder[task] = entry
        heappush(self.queue, entry)

    def remove_task(self, task):
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        "Remove and return the lowest priority task. Raise KeyError if empty."
        while self.queue:
            priority, count, task = heappop(self.queue)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError("pop from an empty priority queue")

    def len(self):
        return len(self.queue)
