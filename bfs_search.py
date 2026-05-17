# =============================================================================
# BREADTH FIRST SEARCH (BFS) — Graph Traversal Algorithm
# =============================================================================
# BFS explores a graph level-by-level, starting from the initial node.
# It uses a QUEUE (FIFO — First In, First Out) to track which nodes to visit.
#
# Key Properties:
#   - Explores ALL neighbours at depth d before moving to depth d+1
#   - Guaranteed to find the SHORTEST PATH (in terms of number of edges)
#   - Uses more memory than DFS (stores entire frontier)
#   - Time Complexity:  O(V + E)  where V = vertices, E = edges
#   - Space Complexity: O(V)      worst case stores all nodes in queue
#
# Real-world uses: GPS navigation (shortest route), social networks
#                  (degrees of separation), web crawlers, puzzle solvers
# =============================================================================

from collections import deque   # deque gives O(1) append and popleft (queue ops)


# -----------------------------------------------------------------------------
# GRAPH DEFINITION
# Each key is a node; its value is a list of directly connected neighbours.
# This is called an ADJACENCY LIST representation.
# -----------------------------------------------------------------------------
GRAPH = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B', 'H'],
    'F': ['C'],
    'G': ['C', 'I'],
    'H': ['E'],          # <-- one possible goal node
    'I': ['G']           # <-- another possible goal node
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
# BFS FUNCTION
# =============================================================================
def bfs(graph, start, goal):
    """
    Perform Breadth First Search on a graph.

    Parameters
    ----------
    graph : dict
        Adjacency list — { node: [neighbour1, neighbour2, ...] }
    start : str
        The node from which the search begins (initial state)
    goal  : str
        The target node we are searching for (goal state)

    Returns
    -------
    path : list or None
        Ordered list of nodes from start to goal, or None if unreachable.
    visited_order : list
        All nodes visited, in the order they were first explored.
    """

    # ------------------------------------------------------------------
    # STEP 1 — Initialise the queue with the starting node.
    #          Each entry in the queue is a PATH (list of nodes),
    #          not just a single node.  This lets us reconstruct the
    #          route once we reach the goal.
    # ------------------------------------------------------------------
    queue = deque()
    queue.append([start])          # enqueue the initial path [start]

    # ------------------------------------------------------------------
    # STEP 2 — Initialise the visited set.
    #          We mark nodes visited WHEN we enqueue them (not when we
    #          pop them), preventing duplicate paths in the queue.
    # ------------------------------------------------------------------
    visited = set()
    visited.add(start)

    visited_order = []             # record exploration order for output

    print("=" * 60)
    print("  BREADTH FIRST SEARCH")
    print("=" * 60)
    print(f"  Start : {start}")
    print(f"  Goal  : {goal}")
    print("-" * 60)

    # ------------------------------------------------------------------
    # STEP 3 — Main BFS loop: keep processing until the queue is empty
    #          (all reachable nodes explored) or goal is found.
    # ------------------------------------------------------------------
    step = 0
    while queue:

        # Dequeue the FIRST path added (FIFO — level-by-level)
        current_path = queue.popleft()

        # The current node being examined is the last in the path
        current_node = current_path[-1]

        visited_order.append(current_node)
        step += 1

        print(f"  Step {step:02d} | Visiting: {current_node:<4} | "
              f"Path so far: {' → '.join(current_path)}")

        # --------------------------------------------------------------
        # STEP 4 — Goal Test: have we reached the target node?
        # --------------------------------------------------------------
        if current_node == goal:
            print("-" * 60)
            print(f"  ✓ Goal '{goal}' FOUND!")
            return current_path, visited_order

        # --------------------------------------------------------------
        # STEP 5 — Expand: add all unvisited neighbours to the queue.
        #          Each neighbour gets its own copy of the current path
        #          extended by one node.
        # --------------------------------------------------------------
        for neighbour in graph.get(current_node, []):
            if neighbour not in visited:
                visited.add(neighbour)            # mark before enqueue
                new_path = current_path + [neighbour]   # extend path
                queue.append(new_path)            # enqueue new path

    # ------------------------------------------------------------------
    # STEP 6 — Queue exhausted: goal is not reachable from start.
    # ------------------------------------------------------------------
    print("-" * 60)
    print(f"  ✗ Goal '{goal}' NOT reachable from '{start}'.")
    return None, visited_order


# =============================================================================
# DISPLAY RESULTS
# =============================================================================
def display_result(path, visited_order, algorithm="BFS"):
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
# MAIN — Run BFS for multiple start/goal combinations
# =============================================================================
if __name__ == "__main__":

    # --- Test Case 1: A → H (should find A→B→E→H) ---
    path, order = bfs(GRAPH, start='A', goal='H')
    display_result(path, order)

    print()

    # --- Test Case 2: A → I (should find A→C→G→I) ---
    path, order = bfs(GRAPH, start='A', goal='I')
    display_result(path, order)

    print()

    # --- Test Case 3: D → F (cross-graph path) ---
    path, order = bfs(GRAPH, start='D', goal='F')
    display_result(path, order)
