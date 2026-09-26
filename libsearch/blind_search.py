from .data_structures import Node, QueueFrontier, StackFrontier, WeightNode


def depth_first_search(*, actions, start, goal, show_explored=False, count_states=False, show_frontier_rate=False, depth=None):
    """
    show_explored: if True it will return the explored(closed) set too.
    count_states: if True it will return the number of explored states. num_explored
    show_frontier_rate: if True it will return the frontier size at each iteration.
    depth: this is used only when dfs is called in iterative deepening to a certain depth

    Returns solution alone, or a tuple of solution followed by whichever
    extras were requested, always in the order above.
    """

    # keep track of growth rate of the frontier
    frate = []
    # print("Depth: {}".format(depth))

    num_explored = 0

    if depth is None:
        start = Node(state=start, parent=None, action=None)
    else:  # this is used only when dfs is called in iterative deepening to a certain depth
        start = Node(state=start, parent=None, action=None, enable_depth=True)

    frontier = StackFrontier()
    frontier.add(start)
    explored = set()
    print("Depth First Search:")
    while True:
        if frontier.empty():
            return None
        frate.append(frontier.len())
        node = frontier.remove()
        # print('In frontier')
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
            # print(solution)
            extras = []
            if count_states:
                extras.append(num_explored)
            if show_explored:
                extras.append(explored)
            if show_frontier_rate:
                extras.append(frate)
            return (solution, *extras) if extras else solution

        explored.add(node.state)
        if depth is None:
            for action, state in actions(node.state):
                if not frontier.contains_state(state) and state not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)
        else:  # this is used only when dfs is called in iterative deepening to a certain depth
            if node.depth <= depth:
                for action, state in actions(node.state):
                    if not frontier.contains_state(state) and state not in explored:
                        child = Node(state=state, parent=node, action=action, enable_depth=True)
                        # print("Child depth: {}".format(depth))
                        frontier.add(child)


def breadth_first_search(*, actions, start, goal, show_explored=False, count_states=False, show_frontier_rate=False):
    """
    show_explored: if True it will return the explored(closed) set too.
    count_states: if True it will return the number of explored states. num_explored
    show_frontier_rate: if True it will return the frontier size at each iteration.

    Returns solution alone, or a tuple of solution followed by whichever
    extras were requested, always in the order above.
    """
    frate = []
    num_explored = 0
    start = Node(state=start, parent=None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)
    explored = set()
    print("Breadth First Search:")
    while True:
        if frontier.empty():
            return None
        frate.append(frontier.len())
        node = frontier.remove()
        # print('In frontier')
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
            extras = []
            if count_states:
                extras.append(num_explored)
            if show_explored:
                extras.append(explored)
            if show_frontier_rate:
                extras.append(frate)
            return (solution, *extras) if extras else solution

        explored.add(node.state)

        for action, state in actions(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


def iterative_deepening(*, actions, start, goal, show_explored=False, show_frontier_rate=False):
    """
    show_explored: if True it will return the explored(closed) set too.
    show_frontier_rate: if True it will return the frontier size at each iteration
    of the depth-limited search that found the solution.
    """
    print("Iterative deepening:")
    depth = 1
    solution = None
    while solution is None:
        solution = depth_first_search(
            actions=actions,
            start=start,
            goal=goal,
            depth=depth,
            show_explored=show_explored,
            show_frontier_rate=show_frontier_rate,
        )
        depth += 1
    # print(solution)
    return solution


def branch_and_bound(*, actions, start, goal, path_cost, show_explored=False, count_states=False):
    """
    show_explored: if True it will return the explored(closed) set too.
    count_states: if True it will return the number of explored states. num_explored
    """

    start = WeightNode(state=start, parent=None, action=None, cost=0)
    frontier = QueueFrontier()
    frontier.add(start)
    explored = set()
    num_explored = 0
    best_cost = float("inf")
    best_solution = None
    print("Branch and Bound:")
    while True:
        if frontier.empty():
            if show_explored and count_states:
                return best_solution, num_explored, explored
            elif show_explored:
                return best_solution, explored
            elif count_states:
                return best_solution, num_explored
            else:
                return best_solution

        node = frontier.remove()
        # node.cost = node.parent.cost + path_cost(node.parent.state + node.state)
        print("Pickedup:", node.action, node.state, node.cost)
        if node.cost < best_cost:
            num_explored += 1
            print("found node with less cost")
            if node.state == goal and node.parent:
                print("solution found")
                best_cost = node.cost
                actions_to_goal = []
                states_to_goal = []
                while node.parent is not None:
                    actions_to_goal.append(node.action)
                    states_to_goal.append(node.state)
                    node = node.parent
                actions_to_goal.reverse()
                states_to_goal.reverse()
                best_solution = (actions_to_goal, states_to_goal)
                print("best solution: {}".format(best_solution))
                print("best cost: {}".format(best_cost))

            explored.add((node.action, node.state))

            for action, state in actions(node.action, node.state):
                if not frontier.contains_node(action, state) and (action, state) not in explored:
                    child = WeightNode(state=state, parent=node, action=action)
                    child.cost = child.parent.cost + path_cost(child.parent.state, child.state)
                    print(child.action, child.cost)
                    frontier.add(child)
