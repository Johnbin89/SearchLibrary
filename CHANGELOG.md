# Changelog

All notable changes to `libsearch` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-26

First release since 0.0.5.post1 in November 2020. It publishes the source
changes that were committed at the time but never released, and adds opt-in
instrumentation for inspecting how a search progressed.

### Changed

- **Breaking.** Every search function now takes keyword-only parameters instead
  of `**kwargs`. `actions`, `start` and `goal` are required, as are `heuristic`
  for the heuristic searches and `path_cost` for `branch_and_bound`.
- **Breaking.** `StackFrontier` and `QueueFrontier` hold the frontier in a
  `collections.deque` rather than a `list`.

### Added

- `show_frontier_rate` returns the size of the frontier at each iteration, for
  studying how the frontier grows during a search. Available on
  `depth_first_search`, `breadth_first_search`, `iterative_deepening`, `a_star`,
  `best_first_search` and `iterative_deepening_a_star`. For the two
  iterative-deepening functions it describes the pass that found the solution,
  not all passes combined. Not available on `branch_and_bound`.
- `show_revisited` returns the states that were reached again after having been
  closed, on `a_star` and `best_first_search`.
- `StackFrontier.len()` and `ModPriorityQueue.len()` report the current frontier
  size.
- `StackFrontier.contents()` prints the action and state of everything currently
  queued.

### Fixed

- `branch_and_bound` builds child nodes as `WeightNode` instead of `Node`.
  Children carry an accumulated path cost, which `Node` does not model.
- `StackFrontier.remove()` pops from a deque instead of rebuilding the list with
  a slice, making each removal O(1) rather than O(n) in the size of the
  frontier.

### Compatibility

Returned arguments are unchanged for every flag combination that existed in
0.0.5.post1. A call with no flags returns the solution alone, `count_states`
appends `num_explored`, `show_explored` appends the closed set, and both
together return a 3-tuple as before.

The values added in this release appear only when their own flag is set. When
several are requested they always arrive in the same order:

```
solution, num_explored, explored, revisited, frate
```

## [0.0.5.post1] - 2020-11-22

Last release of the original series. See the git history for detail.
