import sys
from collections import defaultdict, deque
import time

# ----------------------
# Parsing
# ----------------------
def parse_input(path):
    k = None
    edges_set = set()
    nodes = set()
    with open(path, 'r') as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if line.lower().startswith('colors='):
                # parse colors
                try:
                    k = int(line.split('=')[1])
                except Exception:
                    print("failure")
                    sys.exit(0)
                continue
            # else edge line: u,v
            parts = [p.strip() for p in line.split(',') if p.strip()!='']
            if len(parts) != 2:
                # ignore malformed lines
                continue
            try:
                u = int(parts[0])
                v = int(parts[1])
            except:
                # non-integer nodes -> failure as inputs expected integers
                print("failure")
                sys.exit(0)
            # normalize edge as unordered pair
            if u == v:
                # self-loop with != constraint -> immediate failure
                return k, None, None, "self-loop"
            a,b = (u,v) if u <= v else (v,u)
            edges_set.add((a,b))
            nodes.add(u); nodes.add(v)
    if k is None:
        # no colors line
        print("failure")
        sys.exit(0)
    return k, nodes, edges_set, None

# ----------------------
# Utilities for CSP
# ----------------------
def build_adjacency(nodes, edges_set):
    adj = defaultdict(set)
    for (u,v) in edges_set:
        adj[u].add(v)
        adj[v].add(u)
    # ensure isolated nodes (if any) have empty neighbor sets
    for n in nodes:
        adj.setdefault(n, set())
    return adj

# AC-3 revise: remove values from Dom[X] that have no support in Dom[Y]
# For binary constraint X != Y
def revise(dom, X, Y, trail):
    removed_any = False
    to_remove = []
    # For each value x in Dom[X], check if there exists y in Dom[Y] such that x != y
    for x in set(dom[X]):
        # support exists if Dom[Y] has any value != x
        has_support = any((y != x) for y in dom[Y])
        if not has_support:
            to_remove.append(x)
    if to_remove:
        for val in to_remove:
            dom[X].remove(val)
            trail.append((X, val))
        removed_any = True
    return removed_any

# AC-3 main: queue initial arcs list of (Xi, Xj)
def ac3(dom, adj, initial_arcs, trail):
    q = deque(initial_arcs)
    while q:
        Xi, Xj = q.popleft()
        if revise(dom, Xi, Xj, trail):
            if len(dom[Xi]) == 0:
                return False
            # add all neighbors Xk of Xi except Xj
            for Xk in adj[Xi]:
                if Xk != Xj:
                    q.append((Xk, Xi))
    return True

# ----------------------
# Heuristics: MRV & LCV
# ----------------------
def select_var_mrv(dom, assignment):
    # unassigned vars
    unassigned = [v for v in dom if v not in assignment]
    # choose var with smallest domain size, tie-break by variable id (deterministic)
    best = min(unassigned, key=lambda v: (len(dom[v]), v))
    return best

def order_values_lcv(var, dom, adj, assignment):
    # For each value in dom[var], compute how many values it would eliminate from neighbors
    # elimination count = sum over neighbors not yet assigned of (1 if value in dom[neighbor] else 0)
    val_elim = []
    for val in dom[var]:
        elim = 0
        for nb in adj[var]:
            if nb in assignment:
                continue
            if val in dom[nb]:
                elim += 1
        val_elim.append((elim, val))
    # sort ascending by elimination count, tie-break by value
    val_elim.sort(key=lambda x: (x[0], x[1]))
    ordered = [v for (_, v) in val_elim]
    return ordered

# ----------------------
# Backtracking search with trail undo, MRV, LCV, AC-3
# ----------------------
def backtrack(dom, adj, k, assignment, trail, stats):
    # stats is a dict for optional debugging/performance counting
    if len(assignment) == len(dom):
        return True
    var = select_var_mrv(dom, assignment)
    ordered_values = order_values_lcv(var, dom, adj, assignment)
    for val in ordered_values:
        stats['attempts'] += 1
        # make a marker for trail to undo later
        trail_marker_len = len(trail)
        # assign var := val by pruning other values from dom[var]
        other_vals = [v for v in set(dom[var]) if v != val]
        for ov in other_vals:
            dom[var].remove(ov)
            trail.append((var, ov))
        # also set assignment now
        assignment[var] = val
        # AC-3 initialization: add arcs (neighbor, var) for all neighbors
        initial_arcs = [(nb, var) for nb in adj[var]]
        ac3_ok = ac3(dom, adj, initial_arcs, trail)
        # If AC-3 left any domain empty -> failure for this branch
        if ac3_ok:
            # Additionally check that no assigned neighbor violates constraint (shouldn't happen since we prune)
            violated = False
            for nb in adj[var]:
                if nb in assignment and assignment[nb] == assignment[var]:
                    violated = True
                    break
            if not violated:
                result = backtrack(dom, adj, k, assignment, trail, stats)
                if result:
                    return True
        # undo all domain prunings up to marker
        while len(trail) > trail_marker_len:
            v_restore, val_restore = trail.pop()
            dom[v_restore].add(val_restore)
        # undo assignment
        del assignment[var]
    stats['backtracks'] += 1
    return False

# ----------------------
# Driver
# ----------------------
def solve(filename):
    k, nodes, edges_set, error = parse_input(filename)
    if error == "self-loop":
        print("failure")
        return
    # build adjacency
    adj = build_adjacency(nodes, edges_set)
    # Quick failure: if k < 1 impossible
    if k < 1:
        print("failure")
        return
    # Quick failure: if there is an edge but k==1 and any edge exists -> impossible
    if k == 1 and len(edges_set) > 0:
        print("failure")
        return
    # Create domains: 1..k for each variable (vertex)
    dom = dict()
    for v in adj:
        dom[v] = set(range(1, k+1))
    # prepare trail for prunings
    trail = []
    # initial AC-3 on all arcs to prune obvious inconsistency
    initial_arcs = []
    for u in adj:
        for v in adj[u]:
            initial_arcs.append((u, v))
    # Run AC-3 before search
    if not ac3(dom, adj, initial_arcs, trail):
        print("failure")
        return
    # Check for empty domain
    for v in dom:
        if len(dom[v]) == 0:
            print("failure")
            return
    assignment = {}
    stats = {'attempts': 0, 'backtracks': 0}
    start = time.time()
    ok = backtrack(dom, adj, k, assignment, trail, stats)
    end = time.time()
    if ok:
        # produce mapping as dict sorted by key, keys and values ints
        out_map = {v: assignment[v] for v in sorted(assignment.keys())}
        print("SOLUTION: " + str(out_map))
    else:
        print("failure")

# ----------------------
# Main
# ----------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("failure")
        sys.exit(0)
    input_file = sys.argv[1]
    solve(input_file)
