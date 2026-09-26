from .data_structures import HeuristicNode, ModPriorityQueue, StackFrontier


def a_star(
    *, actions, start, goal, heuristic, show_explored=False, count_states=False, show_revisited=False, show_frontier_rate=False
):
    """
    show_explored: if True it will return the explored(closed) set too.
    count_states: if True it will return the number of explored states. num_explored
    show_revisited: if True it will return the states reached again after being closed.
    show_frontier_rate: if True it will return the frontier size at each iteration.

    Returns solution alone, or a tuple of solution followed by whichever
    extras were requested, always in the order above.
    """

    frate = []
    num_explored = 0
    start = HeuristicNode(state=start, parent=None, action=None, cost=0)

    frontier = ModPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost

    explored = set()
    revisited = []
    print("A Star:")
    while True:
        if frontier.empty():
            return None
        frate.append(frontier.len())
        node = frontier.pop_task()
        # print(node)
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
            extras = []
            if count_states:
                extras.append(num_explored)
            if show_explored:
                extras.append(explored)
            if show_revisited:
                extras.append(revisited)
            if show_frontier_rate:
                extras.append(frate)
            return (solution, *extras) if extras else solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))

        for action, state in actions(node.state):
            if state in explored:
                revisited.append(state)
                continue
            child = HeuristicNode(state=state, parent=node, action=action)
            child.cost = child.cost_from_start + heuristic(child.state, goal)
            if child not in costs or child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)


def best_first_search(
    *, actions, start, goal, heuristic, show_explored=False, count_states=False, show_revisited=False, show_frontier_rate=False
):
    """
    show_explored: if True it will return the explored(closed) set too.
    count_states: if True it will return the number of explored states. num_explored
    show_revisited: if True it will return the states reached again after being closed.
    show_frontier_rate: if True it will return the frontier size at each iteration.

    Returns solution alone, or a tuple of solution followed by whichever
    extras were requested, always in the order above.
    """

    frate = []
    num_explored = 0
    start = HeuristicNode(state=start, parent=None, action=None, cost=0)

    frontier = ModPriorityQueue()
    costs = {}
    frontier.add_task(start, start.cost)
    costs[start] = start.cost

    explored = set()
    revisited = []
    print("Best First Search:")
    while True:
        if frontier.empty():
            return None
        frate.append(frontier.len())
        node = frontier.pop_task()
        # print(node)
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
            extras = []
            if count_states:
                extras.append(num_explored)
            if show_explored:
                extras.append(explored)
            if show_revisited:
                extras.append(revisited)
            if show_frontier_rate:
                extras.append(frate)
            return (solution, *extras) if extras else solution
        print("node state: {} , goal: {}".format(node.state, goal))
        print("Node cost: {}".format(node.cost))

        for action, state in actions(node.state):
            if state in explored:
                revisited.append(state)
                continue
            child = HeuristicNode(state=state, parent=node, action=action)
            # print("Child state: {}".format(child.state))
            # print("goal: {}".format(goal))
            child.cost = heuristic(child.state, goal)
            # print("Child cost: {}".format(child.cost))
            if child not in costs or child.cost < costs[child]:
                if child in costs:
                    frontier.remove_task(child)
                costs[child] = child.cost
                frontier.add_task(child, child.cost)


from heapq import heappop, heappush


def id_depth_first_search(*, actions, start, goal, heuristic, show_explored=False, show_frontier_rate=False, depth=None):
    """
    This dfs implementation is used only for iterative deepening a* below.
    Returns the solution or the new cost limit to be inserted into next dfs search

    show_explored: if True it will return the explored(closed) set too.
    show_frontier_rate: if True it will return the frontier size at each iteration.
    depth: this is used only when dfs is called in iterative deepening to a certain depth
    """

    # print("Depth: {}".format(depth))

    num_explored = 0
    frate = []

    start = HeuristicNode(state=start, parent=None, action=None, cost=0)

    frontier = StackFrontier()
    frontier.add(start)
    encountered_costs = []
    explored = set()
    print("dfs in informed")
    while True:
        # when the search with the bound of cost finish without solution, returns the new bound which is the minimum from costs greater than current bound.
        if frontier.empty():
            return heappop(encountered_costs)
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
            if show_explored:
                extras.append(explored)
            if show_frontier_rate:
                extras.append(frate)
            return (solution, *extras) if extras else solution

        explored.add(node.state)
        if node.cost <= depth:
            for action, state in actions(node.state):
                if not frontier.contains_state(state) and state not in explored:
                    child = HeuristicNode(state=state, parent=node, action=action)
                    child.cost = child.cost_from_start + heuristic(child.state, goal)
                    frontier.add(child)
        else:
            heappush(encountered_costs, node.cost)


def iterative_deepening_a_star(*, actions, start, goal, heuristic, show_explored=False, show_frontier_rate=False):
    """
    show_explored: if True it will return the explored(closed) set too.
    show_frontier_rate: if True it will return the frontier size at each iteration
    of the cost-limited search that found the solution.
    """

    root_node = HeuristicNode(state=start, parent=None, action=None, cost=0)
    depth = root_node.cost
    solution = None
    print("Iterative Deepening with A Star:")
    while True:
        solution = id_depth_first_search(
            actions=actions,
            start=start,
            goal=goal,
            depth=depth,
            heuristic=heuristic,
            show_explored=show_explored,
            show_frontier_rate=show_frontier_rate,
        )
        if isinstance(solution, int):
            depth = solution
            print("Depth id: {}".format(depth))
        else:
            break
    # print(solution)
    return solution
