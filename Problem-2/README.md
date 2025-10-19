# Problem 2 — Graph Coloring via CSP

This project solves the **Graph Coloring Problem** using **Constraint Satisfaction Problem (CSP)** techniques.

The goal is to assign a color (represented by a number) to each vertex of a graph so that **no two connected vertices share the same color**.

The algorithm uses:
- **Backtracking Search**
- **MRV (Minimum Remaining Values)** heuristic
- **LCV (Least Constraining Value)** ordering
- **AC-3 (Arc Consistency)** for domain pruning
- **Trail & Undo** for efficient backtracking

---


## Example Input Files

### csp_small.txt
```text
colors=3
1,2
2,3
3,4
4,1
1,5
```

### csp_tight.txt
```text
colors=4
1,2
1,3
1,4
2,3
2,4
3,4
```

---

## How to Run in Terminal

1. Place all files in the same folder:
   ```
   CSP_GraphColoring_AC3.py
   csp_small.txt
   csp_tight.txt
   ```
2. Open a terminal or command prompt in that folder.
3. Run the following command:

   ```bash
   python CSP_GraphColoring_AC3.py csp_small.txt
   ```

   To test another file (for example, the tight graph):
   ```bash
   python CSP_GraphColoring_AC3.py csp_tight.txt
   ```

---

## Example Outputs

| Input File | Command | Output |
|-------------|----------|---------|
| `csp_small.txt` | `python CSP_GraphColoring_AC3.py csp_small.txt` | `SOLUTION: {1: 1, 2: 2, 3: 1, 4: 3, 5: 2}` |
| `csp_tight.txt` | `python CSP_GraphColoring_AC3.py csp_tight.txt` | `SOLUTION: {1: 1, 2: 2, 3: 3, 4: 4}` |

If no valid coloring exists, the output will be:
```
failure
```


