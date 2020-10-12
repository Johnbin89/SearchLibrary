from data_structs import CNode, MyPriorityQueue
from queue import PriorityQueue


def a_search(**kwargs):
    state_space = kwargs.get('state_space', None)
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False)
    

    num_explored = 0
    start = CNode(state=start, parent=None, action=None, cost=0)
    
    frontier = MyPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost
    
    explored = set()

    while True:
        if frontier.empty():
            return None
    
        node = frontier.pop_task()
        print(node)
        num_explored += 1
        explored.add(node.state)

        if node.state == goal:
            actions_to_goal = []
            states_to_goal = []
            while node.parent is not None:
                actions_to_goal.append(node.action)
                states_to_goal.append(node.state)
                node = node.parent
            actions_to_goal.reverse()
            states_to_goal.reverse()
            solution = (actions_to_goal, states_to_goal)
            return solution, explored if show_explored else solution
            #return solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))
        
        for action, state in actions(node.state):
            if state in explored:
                continue
            child = CNode(state=state, parent=node, action=action)
            child.cost = child.cost_from_start + heuristic(child.state, goal)
            if child not in costs or  child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)


def best_first_search(**kwargs):
    state_space = kwargs.get('state_space', None)
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    heuristic = kwargs.get('heuristic', None)
    show_explored = kwargs.get('show_explored', False)
    

    num_explored = 0
    start = CNode(state=start, parent=None, action=None, cost=0)
    
    frontier = MyPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost
    
    explored = set()

    while True:
        if frontier.empty():
            return None
    
        node = frontier.pop_task()
        print(node)
        num_explored += 1
        explored.add(node.state)

        if node.state == goal:
            actions_to_goal = []
            states_to_goal = []
            while node.parent is not None:
                actions_to_goal.append(node.action)
                states_to_goal.append(node.state)
                node = node.parent
            actions_to_goal.reverse()
            states_to_goal.reverse()
            solution = (actions_to_goal, states_to_goal)
            return solution, explored if show_explored else solution
            #return solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))
        
        for action, state in actions(node.state):
            if state in explored:
                continue
            child = CNode(state=state, parent=node, action=action)
            child.cost = heuristic(child.state, goal)
            if child not in costs or  child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)