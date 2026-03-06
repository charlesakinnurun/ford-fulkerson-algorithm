import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class FordFulkerson:
    """
    A class to represent and solve the Maximum Flow problem using 
    the Ford-Fulkerson algorithm (specifically the Edmonds-Karp implementation
    when using BFS, but here implemented with a focus on clear pathfinding).
    """

    def __init__(self, graph_data):
        """
        Initializes the algorithm with a graph represented as an adjacency matrix.
        graph_data: List of lists representing the capacity of edges.
        """
        self.graph = graph_data  # The original capacity graph
        self.rows = len(graph_data)
        # We create a residual graph which initially is a copy of the original graph.
        # The residual graph tracks remaining capacities and reverse flows.
        self.residual_graph = [row[:] for row in graph_data]

    def _dfs(self, source, sink, parent):
        """
        A helper function using Depth First Search to find an augmenting path 
        from source to sink in the residual graph.
        """
        visited = [False] * self.rows
        stack = [source]
        visited[source] = True

        while stack:
            u = stack.pop()

            for v, capacity in enumerate(self.residual_graph[u]):
                # If the node v is not visited and there is available capacity
                if not visited[v] and capacity > 0:
                    stack.append(v)
                    visited[v] = True
                    parent[v] = u
                    # If we reached the sink, a path exists
                    if v == sink:
                        return True
        return False

    def compute_max_flow(self, source, sink):
        """
        Executes the Ford-Fulkerson algorithm.
        Finds augmenting paths and updates residual capacities until no more paths exist.
        """
        parent = [-1] * self.rows
        max_flow = 0
        iterations = []

        # While there is an augmenting path from source to sink
        while self._dfs(source, sink, parent):
            # 1. Find the bottleneck capacity (minimum capacity) along the path found by DFS
            path_flow = float("Inf")
            s = sink
            current_path = []
            
            while s != source:
                current_path.append(s)
                path_flow = min(path_flow, self.residual_graph[parent[s]][s])
                s = parent[s]
            current_path.append(source)
            current_path.reverse()

            # 2. Add bottleneck capacity to overall flow
            max_flow += path_flow

            # 3. Update residual capacities of the edges and reverse edges along the path
            v = sink
            while v != source:
                u = parent[v]
                self.residual_graph[u][v] -= path_flow
                self.residual_graph[v][u] += path_flow
                v = parent[v]
            
            # Store data for visualization
            iterations.append({
                'path': current_path,
                'flow_added': path_flow,
                'current_total': max_flow
            })

        return max_flow, iterations

def visualize_flow_network(capacity_matrix, flow_data=None, title="Flow Network"):
    """
    Uses NetworkX and Matplotlib to visualize the graph.
    If flow_data is provided, it highlights the final flow values.
    """
    G = nx.DiGraph()
    n = len(capacity_matrix)
    
    # Add edges to the networkx graph
    for i in range(n):
        for j in range(n):
            if capacity_matrix[i][j] > 0:
                G.add_edge(i, j, capacity=capacity_matrix[i][j])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
    nx.draw_networkx_labels(G, pos)
    
    # Draw edges
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        edge_labels[(u, v)] = f"Cap: {d['capacity']}"
    
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title(title)
    plt.axis('off')
    plt.show()

# ==========================================
# EXAMPLES AND ILLUSTRATIONS
# ==========================================

def run_demonstration():
    # Example 1: Standard Network
    # 0: Source, 5: Sink
    print("--- Example 1: Simple Pipeline ---")
    graph = [
        [0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0]
    ]

    ff = FordFulkerson(graph)
    source = 0
    sink = 5

    # Visualizing Initial State
    visualize_flow_network(graph, title="Initial Capacities (Example 1)")

    max_flow, steps = ff.compute_max_flow(source, sink)
    
    print(f"The maximum possible flow is: {max_flow}")
    print("\nAugmenting Paths Found:")
    for i, step in enumerate(steps):
        print(f"Step {i+1}: Path {step['path']} | Flow Added: {step['flow_added']} | Total: {step['current_total']}")

    # Example 2: Small Network with Bottleneck
    print("\n--- Example 2: Bottleneck Network ---")
    # 0 -> 1 (cap 100)
    # 0 -> 2 (cap 100)
    # 1 -> 3 (cap 1)  <-- Bottleneck
    # 2 -> 3 (cap 100)
    graph2 = [
        [0, 100, 100, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 100],
        [0, 0, 0, 0]
    ]
    ff2 = FordFulkerson(graph2)
    max_flow2, _ = ff2.compute_max_flow(0, 3)
    print(f"Max Flow (Bottleneck Example): {max_flow2}")
    visualize_flow_network(graph2, title="Bottleneck Network (Example 2)")

if __name__ == "__main__":
    run_demonstration()