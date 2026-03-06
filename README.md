<h1 align="center">Floyd–Warshall Algorithm</h1>

## Overview

The **Floyd–Warshall Algorithm** is a **dynamic programming algorithm** used to find the **shortest paths between all pairs of vertices** in a **weighted graph**.

Key features:

* ✅ Computes **all-pairs shortest paths**
* ✅ Handles **negative edge weights**
* ❌ Inefficient for very large graphs due to **O(V³) time complexity**

Unlike single-source shortest path algorithms (like Dijkstra or Bellman–Ford), Floyd–Warshall finds the shortest path **between every pair of vertices**.

---

## 📌 Key Concepts

* **Weighted Graph:** A graph where edges have numerical costs (weights).
* **Shortest Path:** Path between two vertices with the **minimum total weight**.
* **Distance Matrix:** A 2D matrix storing shortest distances between all pairs of vertices.
* **Negative Edge:** An edge with weight < 0.
* **Negative Cycle:** A cycle whose total weight is negative, which makes shortest paths undefined.

<a href="/src/main.py">Check out for source code</a>

---

## ⚙️ How Floyd–Warshall Works

1. Initialize a **distance matrix** with direct edge weights, and 0 for the diagonal.
2. For each vertex **k**, consider it as an intermediate vertex and update distances:

```text
distance[i][j] = min(distance[i][j], distance[i][k] + distance[k][j])
```

3. Repeat for all vertices **k = 1 to V**.
4. The matrix at the end contains **shortest paths between all vertex pairs**.

---

## 🧩 Example Graph

```
      (3)
  A ------- B
  |         |
 (8)       (2)
  |         |
  C ------- D
      (1)
```

### Edge Weights

| Edge  | Weight |
| ----- | ------ |
| A → B | 3      |
| A → C | 8      |
| B → D | 2      |
| C → D | 1      |

---

## 🧪 Initial Distance Matrix

```
      A    B    C    D
A     0    3    8    ∞
B     ∞    0    ∞    2
C     ∞    ∞    0    1
D     ∞    ∞    ∞    0
```

---

## 🔄 Iteration Example

If we consider **B as an intermediate vertex**:

* Path A → B → D has distance 3 + 2 = 5
* Update A → D = min(∞, 5) = 5

Updated matrix:

```
      A    B    C    D
A     0    3    8    5
B     ∞    0    ∞    2
C     ∞    ∞    0    1
D     ∞    ∞    ∞    0
```

Continue considering all vertices as intermediates until matrix stabilizes.

---

## ⏱️ Time & Space Complexity

| Metric | Complexity |
| ------ | ---------- |
| Time   | O(V³)      |
| Space  | O(V²)      |

Where **V = number of vertices**.

---

## 🧠 Python Implementation

```python
INF = float('inf')

def floyd_warshall(graph):
    V = len(graph)
    dist = [row[:] for row in graph]

    for k in range(V):
        for i in range(V):
            for j in range(V):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist

graph = [
    [0, 3, 8, INF],
    [INF, 0, INF, 2],
    [INF, INF, 0, 1],
    [INF, INF, INF, 0]
]

result = floyd_warshall(graph)

for row in result:
    print(row)
```

### Output

```
[0, 3, 8, 5]
[inf, 0, inf, 2]
[inf, inf, 0, 1]
[inf, inf, inf, 0]
```

---

## 👍 Advantages

* Finds **shortest paths for all vertex pairs**
* Handles **negative edge weights**
* Simple **matrix-based implementation**
* Suitable for **dense graphs**

---

## 👎 Disadvantages

* Time complexity O(V³) → slow for large graphs
* Space complexity O(V²)
* Not suitable for **very sparse graphs**

---

## 📌 Applications

* Network routing analysis
* Transport system shortest paths
* Transitive closure of graphs
* Graph theory and dynamic programming problems

---

## 🏁 Summary

The **Floyd–Warshall Algorithm** efficiently computes **all-pairs shortest paths** using a simple **dynamic programming approach**. While its cubic time complexity makes it impractical for very large graphs, it is ideal for dense graphs and graphs with negative edge weights.
