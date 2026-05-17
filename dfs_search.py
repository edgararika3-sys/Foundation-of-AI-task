# =============================================================================
# DEPTH FIRST SEARCH (DFS) — Graph Traversal Algorithm
# =============================================================================
# DFS explores a graph by going as DEEP as possible along each branch before
# backtracking.  It uses a STACK (LIFO — Last In, First Out).
#
# Key Properties:
#   - Dives deep before exploring siblings (goes branch-by-branch)
#   - Does NOT guarantee the shortest path
#   - Uses less memory than BFS (only stores current path + stack)
#   - Time Complexity:  O(V + E)  where V = vertices, E = edges
#   - Space Complexity: O(V)      worst case (linear graph, full depth)
#
# Two implementations provided:
#   1. Iterative DFS — uses an explicit stack (mirrors BFS structure)
#   2. Recursive DFS — uses the call stack implicitly (elegant & clear)
#
# Real-world uses: maze solving, topological sorting, cycle detection,
#                  AI game trees (chess, checkers), file system traversal
# =============================================================================


# -----------------------------------------------------------------------------
# GRAPH DEFINITION (same graph as BFS for direct comparison)
# Each key is a node; its value is a list of directly connected neighbours.
# -----------------------------------------------------------------------------
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B', 'H'],
    'F': ['C'],
    'G': ['C', 'I'],
    'H': ['E'],           # <-- one possible goal node
    'I': ['G']            # <-- another possible goal node
}

#
# Visual layout of the graph above:
#
#            A
#           / \
#          B   C
#         / \ / \
#        D  E F  G
#           |     \
#           H      I
#


# =============================================================================
# IMPLEMENTATION 1 — ITERATIVE DFS (using an explicit stack)
# =============================================================================
def dfs_iterative(graph, start, goal):
    """
    Perform Depth First Search iteratively using an explicit stack.

    The stack stores PATHS (not just nodes), so we can reconstruct the
    route from start to goal without needing a separate 'parent' map.

    Parameters
    ----------
    graph : dict
        Adjacency list — { node: [neighbour1, neighbour2, ...] }
    start : str
        Initial node (start state)
    goal  : str
        Target node (goal state)

    Returns
    -------
    path : list or None
        Route from start to goal, or None if goal is unreachable.
    visited_order : list
        All nodes explored, in exploration order.
    """

    # ------------------------------------------------------------------
    # STEP 1 — Initialise the stack with the starting path.
    #          A Python list used as a stack: append() = push,
    #          pop() = pop from right end (LIFO behaviour).
    # ------------------------------------------------------------------
    stack = [[start]]                  # stack holds paths, not nodes
    visited = set()                    # tracks nodes already explored
    visited_order = []                 # records exploration sequence

    print("=" * 60)
    print("  DEPTH FIRST SEARCH — Iterative")
    print("=" * 60)
    print(f"  Start : {start}")
    print(f"  Goal  : {goal}")
    print("-" * 60)

    step = 0

    # ------------------------------------------------------------------
    # STEP 2 — Main DFS loop: process until stack is empty or goal found.
    # ------------------------------------------------------------------
    while stack:

        # Pop the LAST added path (LIFO = depth-first behaviour)
        current_path = stack.pop()
        current_node = current_path[-1]

        # ------------------------------------------------------------------
        # STEP 3 — Skip if already visited (stack may hold duplicate paths
        #          queued before a node was marked visited).
        # ------------------------------------------------------------------
        if current_node in visited:
            continue

        visited.add(current_node)
        visited_order.append(current_node)
        step += 1

        print(f"  Step {step:02d} | Visiting: {current_node:<4} | "
              f"Path so far: {' → '.join(current_path)}")

        # ------------------------------------------------------------------
        # STEP 4 — Goal Test
        # ------------------------------------------------------------------
        if current_node == goal:
            print("-" * 60)
            print(f"  ✓ Goal '{goal}' FOUND!")
            return current_path, visited_order

        # ------------------------------------------------------------------
        # STEP 5 — Expand neighbours (push in REVERSE order so the first
        #          neighbour in the list is explored first, matching the
        #          expected left-to-right DFS traversal order).
        # ------------------------------------------------------------------
        for neighbour in reversed(graph.get(current_node, [])):
            if neighbour not in visited:
                new_path = current_path + [neighbour]
                stack.append(new_path)             # push onto stack

    # ------------------------------------------------------------------
    # STEP 6 — Stack empty: goal not reachable.
    # ------------------------------------------------------------------
    print("-" * 60)
    print(f"  ✗ Goal '{goal}' NOT reachable from '{start}'.")
    return None, visited_order


# =============================================================================
# IMPLEMENTATION 2 — RECURSIVE DFS (uses Python's call stack implicitly)
# =============================================================================
def dfs_recursive(graph, current, goal, visited=None, path=None,
                  visited_order=None, step_counter=None):
    """
    Perform Depth First Search recursively.

    Each function call represents going one level deeper.  Python's own
    call stack acts as the DFS stack — recursion IS the stack.

    Parameters
    ----------
    graph         : dict  — adjacency list
    current       : str   — node currently being examined
    goal          : str   — target node
    visited       : set   — nodes already explored (shared across calls)
    path          : list  — current path from start to 'current'
    visited_order : list  — exploration order (shared across calls)
    step_counter  : list  — mutable counter [n] shared across calls

    Returns
    -------
    path : list or None
    visited_order : list
    """

    # ------------------------------------------------------------------
    # Initialise mutable defaults on the first call only.
    # Using a list for step_counter makes it mutable across recursion.
    # ------------------------------------------------------------------
    if visited is None:
        visited       = set()
        path          = []
        visited_order = []
        step_counter  = [0]   # list so it can be mutated in nested calls

    # ------------------------------------------------------------------
    # STEP 1 — Mark the current node as visited and extend the path.
    # ------------------------------------------------------------------
    visited.add(current)
    path = path + [current]       # create NEW list (don't mutate shared state)
    visited_order.append(current)
    step_counter[0] += 1

    print(f"  Step {step_counter[0]:02d} | Visiting: {current:<4} | "
          f"Path so far: {' → '.join(path)}")

    # ------------------------------------------------------------------
    # STEP 2 — Goal Test: base case — stop recursion if goal reached.
    # ------------------------------------------------------------------
    if current == goal:
        return path, visited_order

    # ------------------------------------------------------------------
    # STEP 3 — Recursive case: explore each unvisited neighbour.
    #          DFS dives into the first neighbour before trying others.
    # ------------------------------------------------------------------
    for neighbour in graph.get(current, []):
        if neighbour not in visited:
            result_path, _ = dfs_recursive(
                graph, neighbour, goal,
                visited, path, visited_order, step_counter
            )
            # If the recursive call found the goal, propagate it upward
            if result_path is not None:
                return result_path, visited_order

    # ------------------------------------------------------------------
    # STEP 4 — Backtrack: no neighbour led to the goal from here.
    #          Returning None causes the caller to try the next neighbour.
    # ------------------------------------------------------------------
    return None, visited_order


# =============================================================================
# DISPLAY RESULTS
# =============================================================================
def display_result(path, visited_order, algorithm="DFS"):
    """Pretty-print the final search results."""
    print()
    print("=" * 60)
    print(f"  {algorithm} RESULTS SUMMARY")
    print("=" * 60)

    if path:
        print(f"  Search Path  : {' → '.join(path)}")
        print(f"  Path Length  : {len(path) - 1} edge(s)")
    else:
        print("  Search Path  : No path found")

    print(f"  Nodes Visited: {' → '.join(visited_order)}")
    print(f"  Total Visited: {len(visited_order)}")
    print("=" * 60)


# =============================================================================
# MAIN — Run both DFS implementations and compare
# =============================================================================
if __name__ == "__main__":

    # -----------------------------------------------------------------------
    # TEST CASE 1 — Iterative DFS: A → H
    # Expected path: A → B → E → H  (dives deep on B branch first)
    # -----------------------------------------------------------------------
    path, order = dfs_iterative(GRAPH, start='A', goal='H')
    display_result(path, order, "DFS (Iterative)")

    print()
    print("~" * 60)
    print()

    # -----------------------------------------------------------------------
    # TEST CASE 2 — Recursive DFS: A → H
    # Same graph, same start/goal — compare with iterative output above
    # -----------------------------------------------------------------------
    print("=" * 60)
    print("  DEPTH FIRST SEARCH — Recursive")
    print("=" * 60)
    print(f"  Start : A")
    print(f"  Goal  : H")
    print("-" * 60)
    path, order = dfs_recursive(GRAPH, current='A', goal='H')
    print("-" * 60)
    print("  ✓ Goal 'H' FOUND!")
    display_result(path, order, "DFS (Recursive)")

    print()
    print("~" * 60)
    print()

    # -----------------------------------------------------------------------
    # TEST CASE 3 — Iterative DFS: A → I
    # Expected path: dives into A→B first, backtracks, then A→C→G→I
    # -----------------------------------------------------------------------
    path, order = dfs_iterative(GRAPH, start='A', goal='I')
    display_result(path, order, "DFS (Iterative)")

    print()
    print("~" * 60)
    print()

    # -----------------------------------------------------------------------
    # TEST CASE 4 — Cross-graph: D → F
    # DFS must traverse from leaf D back to root A and across to F
    # -----------------------------------------------------------------------
    path, order = dfs_iterative(GRAPH, start='D', goal='F')
    display_result(path, order, "DFS (Iterative)")
