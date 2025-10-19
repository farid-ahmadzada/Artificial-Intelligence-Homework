import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(graph, coords, source, dest):
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)

    pos = {n: coords[n] for n in coords}
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green', label='Source')
    nx.draw_networkx_nodes(G, pos, nodelist=[dest], node_color='red', label='Destination')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Graph Visualization")
    plt.show()


"""
A* implementation (three modes) for Homework 1: A* (Three Modes) + CSP (Graph Coloring)
Includes:
 - parser for input graph files
 - A* implementation with UCS (h=0), Euclidean, Manhattan heuristics
 - deterministic tie-breaking
 - tracking: expanded, pushes, max_frontier, runtime

Usage:
  python Astar_three_modes.py <input_file>

Example:
  python Astar_three_modes.py astar_small.txt

The script prints results for each mode in the following format:

MODE: <UCS | A* Euclidean | A* Manhattan>
Optimal cost: <number | NO PATH>
Path: <S -> ... -> D | (omit if NO PATH)>
Expanded: <int>
Pushes: <int>
Max frontier: <int>
Runtime (s): <float>
"""

import sys
import time
import math
import heapq
from collections import defaultdict

# ------------------ Parser ------------------
def parse_graph_file(path):
    """Parse the graph input file."""
    coords = {}
    graph = defaultdict(list)
    nodes = set()
    source = None
    dest = None

    with open(path, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) == 2 and parts[0].upper() == 'S':
                source = int(parts[1])
                nodes.add(source)
            elif len(parts) == 2 and parts[0].upper() == 'D':
                dest = int(parts[1])
                nodes.add(dest)
            elif len(parts) == 2:
                vid = int(parts[0])
                cell = int(parts[1])
                nodes.add(vid)
                x = cell // 10
                y = cell % 10
                coords[vid] = (x, y)
            elif len(parts) == 3:
                u = int(parts[0])
                v = int(parts[1])
                w = float(parts[2])
                nodes.add(u)
                nodes.add(v)
                graph[u].append((v, w))
                graph[v].append((u, w))  # undirected
            else:
                continue

    for n in nodes:
        if n not in coords:
            coords[n] = (n // 10, n % 10)

    for n in nodes:
        if n not in graph:
            graph[n] = []

    return nodes, coords, graph, source, dest


# ------------------ Heuristics ------------------
def h_zero(n, goal, coords):
    return 0.0


def h_euclidean(n, goal, coords):
    xn, yn = coords[n]
    xg, yg = coords[goal]
    return math.hypot(xn - xg, yn - yg)


def h_manhattan(n, goal, coords):
    xn, yn = coords[n]
    xg, yg = coords[goal]
    return abs(xn - xg) + abs(yn - yg)


# ------------------ A* Implementation ------------------
def astar(nodes, graph, coords, source, dest, heuristic_fn):
    """Run A* from source to dest using heuristic_fn(n, goal, coords)."""
    start_time = time.perf_counter()

    g_cost = {n: math.inf for n in nodes}
    parent = {n: None for n in nodes}

    heap = []
    pushes = 0

    g_cost[source] = 0.0
    h0 = heuristic_fn(source, dest, coords)
    heapq.heappush(heap, (h0, source, 0.0, source))
    pushes += 1
    max_frontier = len(heap)
    expanded = 0

    while heap:
        if len(heap) > max_frontier:
            max_frontier = len(heap)
        f, tie_node, g_popped, node = heapq.heappop(heap)
        if abs(g_popped - g_cost[node]) > 1e-9:
            continue
        expanded += 1

        if node == dest:
            path = []
            cur = dest
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            runtime = time.perf_counter() - start_time
            stats = {
                'expanded': expanded,
                'pushes': pushes,
                'max_frontier': max_frontier,
                'runtime_s': runtime
            }
            return g_cost[dest], path, stats

        for (neighbor, w) in graph[node]:
            tentative_g = g_cost[node] + w
            if tentative_g + 1e-12 < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                parent[neighbor] = node
                h = heuristic_fn(neighbor, dest, coords)
                f_new = tentative_g + h
                heapq.heappush(heap, (f_new, neighbor, tentative_g, neighbor))
                pushes += 1

    runtime = time.perf_counter() - start_time
    stats = {
        'expanded': expanded,
        'pushes': pushes,
        'max_frontier': max_frontier,
        'runtime_s': runtime
    }
    return None, None, stats


# ------------------ Utilities ------------------
def print_mode_output(mode_name, cost, path, stats):
    print(f"MODE: {mode_name}")
    if cost is None:
        print("Optimal cost: NO PATH")
    else:
        if abs(cost - round(cost)) < 1e-9:
            cost_str = str(int(round(cost)))
        else:
            cost_str = f"{cost:.6f}"
        print(f"Optimal cost: {cost_str}")
    if path is not None:
        print("Path: " + " -> ".join(str(x) for x in path))
    print(f"Expanded: {stats['expanded']}")
    print(f"Pushes: {stats['pushes']}")
    print(f"Max frontier: {stats['max_frontier']}")
    print(f"Runtime (s): {stats['runtime_s']:.6f}")
    print()


# ------------------ Main ------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python Astar_three_modes.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    nodes, coords, graph, source, dest = parse_graph_file(input_file)

    if source is None or dest is None:
        print("Input file must specify source (S,id) and destination (D,id)")
        sys.exit(1)

    # Run UCS (h=0)
    cost_u, path_u, stats_u = astar(nodes, graph, coords, source, dest, lambda n, g, c: h_zero(n, g, c))
    print_mode_output('UCS', cost_u, path_u, stats_u)

    # Run A* Euclidean
    cost_e, path_e, stats_e = astar(nodes, graph, coords, source, dest, lambda n, g, c: h_euclidean(n, g, c))
    print_mode_output('A* Euclidean', cost_e, path_e, stats_e)

    # Run A* Manhattan
    cost_m, path_m, stats_m = astar(nodes, graph, coords, source, dest, lambda n, g, c: h_manhattan(n, g, c))
    print_mode_output('A* Manhattan', cost_m, path_m, stats_m)
