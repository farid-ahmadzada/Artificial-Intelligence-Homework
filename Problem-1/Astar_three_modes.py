import sys
import time
import math
import heapq
from collections import defaultdict

# Optional visualization
try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VIS_AVAILABLE = True
except ImportError:
    VIS_AVAILABLE = False


def parse_graph_file(path):
    coords = {}
    graph = defaultdict(list)
    nodes = set()
    source = dest = None

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
                coords[vid] = (cell // 10, cell % 10)
            elif len(parts) == 3:
                u, v, w = int(parts[0]), int(parts[1]), float(parts[2])
                nodes.update([u, v])
                graph[u].append((v, w))
                graph[v].append((u, w))

    for n in nodes:
        coords.setdefault(n, (n // 10, n % 10))
        graph.setdefault(n, [])

    return nodes, coords, graph, source, dest


def h_zero(n, goal, coords): 
    return 0.0

def h_euclidean(n, goal, coords):
    xn, yn = coords[n]; xg, yg = coords[goal]
    return math.hypot(xn - xg, yn - yg)

def h_manhattan(n, goal, coords):
    xn, yn = coords[n]; xg, yg = coords[goal]
    return abs(xn - xg) + abs(yn - yg)


def astar(nodes, graph, coords, source, dest, heuristic_fn):
    start_time = time.perf_counter()
    g_cost = {n: math.inf for n in nodes}
    parent = {n: None for n in nodes}
    heap = []
    pushes = expanded = 0
    g_cost[source] = 0.0
    heapq.heappush(heap, (heuristic_fn(source, dest, coords), source, 0.0, source))
    pushes += 1
    max_frontier = 1

    while heap:
        max_frontier = max(max_frontier, len(heap))
        f, tie, g_val, node = heapq.heappop(heap)
        if abs(g_val - g_cost[node]) > 1e-9:
            continue
        expanded += 1
        if node == dest:
            path, cur = [], dest
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return g_cost[dest], path, {
                'expanded': expanded,
                'pushes': pushes,
                'max_frontier': max_frontier,
                'runtime_s': time.perf_counter() - start_time
            }
        for (nbr, w) in graph[node]:
            new_g = g_cost[node] + w
            if new_g < g_cost[nbr]:
                g_cost[nbr] = new_g
                parent[nbr] = node
                f_new = new_g + heuristic_fn(nbr, dest, coords)
                heapq.heappush(heap, (f_new, nbr, new_g, nbr))
                pushes += 1
    return None, None, {
        'expanded': expanded, 'pushes': pushes,
        'max_frontier': max_frontier,
        'runtime_s': time.perf_counter() - start_time
    }


def print_mode_output(name, cost, path, stats):
    print(f"MODE: {name}")
    print(f"Optimal cost: {'NO PATH' if cost is None else int(cost) if abs(cost - round(cost)) < 1e-9 else f'{cost:.6f}'}")
    if path: 
        print("Path: " + " -> ".join(map(str, path)))
    print(f"Expanded: {stats['expanded']}")
    print(f"Pushes: {stats['pushes']}")
    print(f"Max frontier: {stats['max_frontier']}")
    print(f"Runtime (s): {stats['runtime_s']:.6f}\n")


def visualize_graph(graph, coords, source, dest):
    if not VIS_AVAILABLE:
        print("Visualization requires networkx and matplotlib.")
        print("Install them using: pip install networkx matplotlib\n")
        return
    G = nx.Graph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)
    pos = {n: coords[n] for n in coords}
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600, font_size=9)
    nx.draw_networkx_nodes(G, pos, nodelist=[source], node_color='green')
    nx.draw_networkx_nodes(G, pos, nodelist=[dest], node_color='red')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Graph Visualization")
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python Astar_three_modes.py <input_file> [--show]")
        sys.exit(1)
    
    show_graph = len(sys.argv) >= 3 and sys.argv[2] == '--show'
    nodes, coords, graph, s, d = parse_graph_file(sys.argv[1])
    if s is None or d is None:
        print("Input file must specify S and D")
        sys.exit(1)

    if show_graph:
        visualize_graph(graph, coords, s, d)

    for name, fn in [('UCS', h_zero), ('A* Euclidean', h_euclidean), ('A* Manhattan', h_manhattan)]:
        c, p, st = astar(nodes, graph, coords, s, d, fn)
        print_mode_output(name, c, p, st)
