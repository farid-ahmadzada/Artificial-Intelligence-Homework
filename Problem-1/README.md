# A* Search (Three Modes) – AI Homework Problem 1

### Overview
This project implements the **A\*** search algorithm in three different modes:
1. **Uniform Cost Search (UCS)** – A\* with `h(n) = 0`
2. **A\* Euclidean Heuristic**
3. **A\* Manhattan Heuristic**

Each mode reports:
- Optimal path cost
- Path (sequence of nodes)
- Number of expanded nodes
- Number of pushes into the priority queue
- Maximum frontier size
- Runtime (in seconds)

---



### Input File Format

Each input `.txt` file defines:
1. **Vertices** → `<id>,<cell>`  
   (Cell used to assign approximate x/y coordinates for heuristic)
2. **Edges** → `<from>,<to>,<weight>`  
   (Bidirectional connection with non-negative cost)
3. **Source/Destination** → `S,<id>` and `D,<id>`

#### Example:
```txt
# vertices
1,11
2,12
3,22
4,32
5,33

# edges
1,2,7
2,3,4
3,4,3
2,5,6
5,4,2

# source and destination
S,1
D,4
