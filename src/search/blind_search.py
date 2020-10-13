from .data_structs import Node, StackFrontier, QueueFrontier


def depth_first_search(**kwargs):
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    depth = kwargs.get('depth', None)   #this is used only when dfs is called in iterative deepening to a certain depth
    
    #print("Depth: {}".format(depth))
    
    num_explored = 0
    
    if depth == None:
        start = Node(state=start, parent=None, action=None)
    else: #this is used only when dfs is called in iterative deepening to a certain depth
        start = Node(state=start, parent=None, action=None, enable_depth=True) 

    frontier = StackFrontier()
    frontier.add(start)
    explored = set()
    print("dfs in pip")
    while True:

        if frontier.empty():
            return None

        node = frontier.remove()
        print('In frontier')
        num_explored += 1

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
            print(solution)
            if show_explored:
                return solution, explored
            else:
                return solution
            #return solution

        
        explored.add(node.state)
        if depth == None:
            for action, state in actions(node.state):
                if not frontier.contains_state(state) and state not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
        else:    #this is used only when dfs is called in iterative deepening to a certain depth
            if node.depth <= depth:
                for action, state in actions(node.state):
                    if not frontier.contains_state(state) and state not in explored:
                        child = Node(state=state, parent=node, action=action, enable_depth=True)
                        print("Child depth: {}".format(depth))
                        frontier.add(child)              




def breadth_first_search(**kwargs):
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.

    num_explored = 0
    start = Node(state=start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    explored = set()

    while True:

        if frontier.empty():
            return None

        node = frontier.remove()
        #print('In frontier')
        num_explored += 1

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
            return solution
        
        explored.add(node.state)

        for action, state in actions(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)



def iterative_deepening(**kwargs):
    state_space = kwargs.get('state_space', None)
    actions = kwargs.get('actions', None)
    start = kwargs.get('start', None)
    goal = kwargs.get('goal', None)
    show_explored = kwargs.get('show_explored', False) #if True it will return the explored(closed) set too.
    
    depth = 1
    solution = None
    while solution == None:
        solution = depth_first_search(actions=actions, start=start, goal=goal, depth=depth, show_explored=show_explored)
        depth += 1
    print(solution)
    return solution