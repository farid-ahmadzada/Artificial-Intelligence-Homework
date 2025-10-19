# 🧠 Problem 2 — Graph Coloring via CSP

This project solves the **Graph Coloring Problem** using **Constraint Satisfaction Problem (CSP)** techniques.

The goal is to assign a color (represented by a number) to each vertex of a graph so that **no two connected vertices share the same color**.

The algorithm uses:
- **Backtracking Search**
- **MRV (Minimum Remaining Values)** heuristic
- **LCV (Least Constraining Value)** ordering
- **AC-3 (Arc Consistency)** for domain pruning
- **Trail & Undo** for efficient backtracking

---

## ⚙️ What the Program Does
This program:
1. Reads a text file describing the graph and number of colors.
2. Builds a CSP model (variables, domains, constraints).
3. Uses MRV, LCV, and AC-3 to search for a valid color assignment.
4. Prints either a valid coloring or `failure` if unsolvable.

---

## 📄 Input Format
The input file must follow this structure:

```
colors=<k>        # number of available colors (integer ≥ 1)
u,v               # undirected edges between integer vertices
...
```

- Lines starting with `#` or blank lines are ignored.
- Self-loops `(u,u)` are not allowed (immediate failure).
- Vertices are inferred from all edge endpoints.

---

## ✅ Example Input Files

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

## 💻 How to Run in Terminal

1. Make sure you have **Python 3.8+** installed.
2. Place all files in the same folder:
   ```
   CSP_GraphColoring_AC3.py
   csp_small.txt
   csp_tight.txt
   ```
3. Open a terminal or command prompt in that folder.
4. Run the following command:

   ```bash
   python CSP_GraphColoring_AC3.py csp_small.txt
   ```

   To test another file (for example, the tight graph):
   ```bash
   python CSP_GraphColoring_AC3.py csp_tight.txt
   ```

---

## 📊 Example Outputs

| Input File | Command | Output |
|-------------|----------|---------|
| `csp_small.txt` | `python CSP_GraphColoring_AC3.py csp_small.txt` | `SOLUTION: {1: 1, 2: 2, 3: 1, 4: 3, 5: 2}` |
| `csp_tight.txt` | `python CSP_GraphColoring_AC3.py csp_tight.txt` | `SOLUTION: {1: 1, 2: 2, 3: 3, 4: 4}` |

If no valid coloring exists, the output will be:
```
failure
```

---

## 🧮 Algorithm Summary

| Component | Description |
|------------|--------------|
| **Variables** | Vertices appearing in any edge |
| **Domains** | `{1, 2, …, k}` where `k` is from `colors=<k>` |
| **Constraint** | For each edge `(u,v)`: `color[u] ≠ color[v]` |
| **MRV** | Choose the variable with the smallest domain first |
| **LCV** | Order colors that eliminate the fewest neighbor options |
| **AC-3** | Maintains consistency between variables after each assignment |
| **Trail & Undo** | Reverts domain changes during backtracking |

---

## 🚫 Edge Cases Handled

- Self-loops `(u,u)` → immediate `failure`
- Duplicate edges → ignored automatically
- `k = 1` with connected nodes → `failure`
- Isolated vertices → automatically assigned a color

---

## 📁 Example Folder Structure

```
📂 CSP_Project/
 ┣ 📜 CSP_GraphColoring_AC3.py
 ┣ 📜 csp_small.txt
 ┣ 📜 csp_tight.txt
 ┗ 📜 README.md
```

---

## 🧑‍💻 Author Notes

- Created for **Artificial Intelligence — Homework 1, Problem 2**  
- Demonstrates a CSP solver combining **Backtracking + MRV + LCV + AC-3**  
- No external libraries required (only standard Python modules)  
- Works well for small to medium graphs  

---

### 🚀 Quick Demo

Run this command in your terminal:
```bash
python CSP_GraphColoring_AC3.py csp_small.txt
```

Expected Output:
```
SOLUTION: {1: 1, 2: 2, 3: 3, 4: 1, 5: 2}
```

If the problem is unsolvable, the output will simply be:
```
failure
```
