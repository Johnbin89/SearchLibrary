libsearch | [![CI](https://github.com/Johnbin89/SearchLibrary/actions/workflows/ci.yml/badge.svg)](https://github.com/Johnbin89/SearchLibrary/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Johnbin89/SearchLibrary/branch/master/graph/badge.svg?token=PQ74UIDAS9)](https://codecov.io/gh/Johnbin89/SearchLibrary)
[![PyPI](https://img.shields.io/pypi/v/libsearch)](https://pypi.org/project/libsearch/)
[![Downloads](https://img.shields.io/pepy/dt/libsearch)](https://pepy.tech/project/libsearch)
===============================================================================

## Description

A Library of search algorithms, used in _State Space Problems_ where the solution is based on a search into a collection of different states, starting from an **Initial state** and following specific rules to get from that state to next possible states until a **Goal state** has been reached.

- Initial State ​ : the state which represents the current description of the problem, from
which the search will begin.
- State Space : ​ the set of all possible States
- Actions ​ : a function that takes a State as an argument and return a set of resulting States.
- Goal State(s) ​ : a State or a set of final States defined by specific rules to terminate the search
and indicate that an acceptable solution was found.

### Implemented Algorithms
The following algorithms are supported. 
#### _Blind Search_

- Depth First Search
- Breadth First Search
- Iterative Deepening
- Branch and Bound

#### _Heuristic Search_

- Best First Search
- A Star
- Iterative Deepening(A- Star)

## Getting started

Install the latest version with:

```shell
pip install libsearch
```
## Usage  

```python
from libsearch import function
```

**Replace _function_ with the algorithm you wish to use by following:**
_In parenthesis you will find the required arguments for each function. (actions is a function as in description above  which returns child State(s) from a parent State)_

#### Blind Search Algorithms:
```python
depth_first_search(actions=actions, start=InitialState, goal=GoalState)
```
```python
breadth_first_search(actions=actions, start=InitialState, goal=GoalState)
```
```python
iterative_deepening(actions=actions, start=InitialState, goal=GoalState)
```
_For Branch and Bound a path_cost function should be provided which returns the cost of reaching a State._
```python
branch_and_bound(actions=actions, start=InitialState, goal=GoalState, path_cost=path_cost)
```

#### Heuristic Search Algorithms:  
_heuristic: A heuristic function defined be the user unique for each problem which returns an estimated cost to reach GoalState from current State._
```python
best_first_search(actions=actions, start=InitialState, goal=GoalState, heuristic=heuristic)
```
```python
a_star(actions=actions, start=InitialState, goal=GoalState, heuristic=heuristic)
```
```python
iterative_deepening_a_star(actions=actions, start=InitialState, goal=GoalState, heuristic=heuristic)
```

#### (Optional arguments)
_For evaluation purposes the following can be set alongside the required arguments above, to return extra information about how the search progressed._
```python
count_states=True            #if True it will return the number of explored states too. num_explored
show_explored=True           #if True it will return the explored(closed) set too.
show_revisited=True          #if True it will return the States reached again after being closed.
show_frontier_rate=True      #if True it will return the size of the frontier at each iteration.
```

Not every algorithm supports every argument:

| Argument | Available on |
| --- | --- |
| `show_explored` | all algorithms |
| `count_states` | all except `iterative_deepening` and `iterative_deepening_a_star` |
| `show_frontier_rate` | all except `branch_and_bound` |
| `show_revisited` | `a_star` and `best_first_search` only |

For `iterative_deepening` and `iterative_deepening_a_star`, `show_frontier_rate` describes the depth-limited pass that found the solution, not all passes combined.

#### Solution
The **solution** returned by algorithms is a python **tuple** consisting of **(list_of_actions, list_of_states)**.  
_list_of_actions_: the actions it took to reach each State on the path to Goal State  
_list_of_states_: the path to the Goal State from Initial State

Each optional argument you request appends one more value to what is returned, always in the same order: _num_explored_, _explored_, _revisited_, _frate_. So they can be combined freely:

```python
solution = a_star(actions=actions, start=InitialState, goal=GoalState, heuristic=heuristic)

solution, num_explored = a_star(actions=actions, start=InitialState, goal=GoalState,
                                heuristic=heuristic, count_states=True)

solution, explored, frate = a_star(actions=actions, start=InitialState, goal=GoalState,
                                   heuristic=heuristic, show_explored=True, show_frontier_rate=True)
```

## Example

Usage of Branch and Bound algorithm for the well-known algorithmic problem [Traveling Salesman (TSP)](https://en.wikipedia.org/wiki/Travelling_salesman_problem).  
In the following Complete Weighted Graph figure each city is represented by a letter and each path has a path cost:

<img src="https://github.com/Johnbin89/SearchLibrary/raw/master/examples/TSPGraph.png" width="700">

We use a Dictionary to implement this Graph in python:
```python
tspGraph = {'A': {'B':8, 'C':5, 'D':10, 'E':8},
        'B': {'A':8, 'C':7, 'D':6, 'E':6},
        'C': {'A':5, 'B':7, 'D':9, 'E':3},
        'D': {'A':10, 'B':6, 'C':9, 'E':4},
        'E': {'A':8, 'B':6, 'C':3, 'D':4}}
```

In this problem States are cities represented by their letters and actions are moves from a city to another. 
e.g The action "A-B" applied to State "A" will result to a new State "B" and has a cost(weight) of 8.

In our module we import the branch and bound function:
```python
from libsearch import branch_and_bound
```

Lets assign the function to a variable (eg. solution):
 ```python
solution = branch_and_bound(actions=g.fullneighbors, start='A', goal='A', path_cost=g.path_cost)
```

If we were to print _solution_ we would get the following:
```shell
(['A-B', 'A-B-D', 'A-B-D-E', 'A-B-D-E-C', 'A-B-D-E-C-A'], ['B', 'D', 'E', 'C', 'A'])
```
The first list are the actions (moving from each letter(State) to the next one) and the latter is a list of States representing the path to reach the Goal State "A", whereas in our case it is the same as the Initial State as described in TSP problem.

##### Optional arguments
If we wish to see how many states the branch and bound algorithm explored:
 ```python
solution, num_explored = branch_and_bound(actions=g.fullneighbors, start='A', goal='A', path_cost=g.path_cost, count_states=True)
```

Checking the value of num_explored we can see that 68 States(path combined) were explored before reaching the Goal.  

More details on the implementation of _fullneighbors_ function which return child States for the specific TSP problem and the path_cost function which return the cost assigned to each path, can be found on [graph.py](https://github.com/Johnbin89/SearchLibrary/blob/master/examples/graph.py) in examples folder.

## Notes 
This implementation of search algorithms as functions can be used virtually in any problem that can be defined as a search in a State Space, as long as the User will define the **actions** function to generate new State from an existing one and in case of Heuristic Search a **heuristic function** to estimate the cost of reaching the Goal State.

In examples folder you can experiment with different algorithms on a Maze problem [maze.py](https://github.com/Johnbin89/SearchLibrary/blob/master/examples/maze.py).
