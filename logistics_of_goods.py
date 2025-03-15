import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

# Create the directed graph
G = nx.DiGraph()

# Add the nodes to the graph
edges = [
    (0, 2, 25),  # terminal 1 -> warehouse 1 -> 25
    (0, 3, 20),  # terminal 1 -> warehouse 2 -> 20
    (0, 4, 15),  # terminal 1 -> warehouse 3 -> 15
    (1, 4, 15),  # terminal 2 -> warehouse 3 -> 15
    (1, 5, 30),  # terminal 2 -> warehouse 4 -> 30
    (1, 3, 10),  # terminal 2 -> warehouse 2 -> 10
    (2, 6, 15),  # warehouse 1 -> shop 1 -> 15
    (2, 7, 10),  # warehouse 1 -> shop 2 -> 10
    (2, 8, 20),  # warehouse 1 -> shop 3 -> 20
    (3, 9, 15),  # warehouse 2 -> shop 4 -> 15
    (3, 10, 10),  # warehouse 2 -> shop 5 -> 10
    (3, 11, 25),  # warehouse 2 -> shop 6 -> 25
    (4, 12, 20),  # warehouse 3 -> shop 7 -> 20
    (4, 13, 15),  # warehouse 3 -> shop 8 -> 15
    (4, 14, 10),  # warehouse 3 -> shop 9 -> 10
    (5, 15, 20),  # warehouse 4 -> shop 10 -> 20
    (5, 16, 10),  # warehouse 4 -> shop 11 -> 10
    (5, 17, 15),  # warehouse 4 -> shop 12 -> 15
    (5, 18, 5),  # warehouse 4 -> shop 13 -> 5
    (5, 19, 10),  # warehouse 4 -> shop 14 -> 10
]

# Add the edges to the graph
G.add_weighted_edges_from(edges)

# Position of the nodes in the graph for the plot
pos = {
    0: (2, 5.5),
    1: (10, 5.5),
    2: (4, 7),
    3: (8, 7),
    4: (4, 4),
    5: (8, 4),
    6: (0, 10),
    7: (2, 10),
    8: (4, 10),
    9: (6, 10),
    10: (8, 10),
    11: (10, 10),
    12: (0, 2),
    13: (2, 2),
    14: (4, 2),
    15: (6, 2),
    16: (8, 2),
    17: (10, 2),
    18: (12, 2),
    19: (14, 2),
}

# Name of the nodes
labels_nodes = {
    0: "Terminal 1",
    1: "Terminal 2",
    2: "Warehouse 1",
    3: "Warehouse 2",
    4: "Warehouse 3",
    5: "Warehouse 4",
    6: "Shop 1",
    7: "Shop 2",
    8: "Shop 3",
    9: "Shop 4",
    10: "Shop 5",
    11: "Shop 6",
    12: "Shop 7",
    13: "Shop 8",
    14: "Shop 9",
    15: "Shop 10",
    16: "Shop 11",
    17: "Shop 12",
    18: "Shop 13",
    19: "Shop 14",
}
plt.figure(figsize=(10, 7))
nx.draw(
    G,
    pos,
    with_labels=True,
    labels=labels_nodes,
    node_size=1000,
    node_color="lightblue",
    font_size=6,
    font_weight="bold",
    arrows=True,
    arrowstyle="-|>",
    arrowsize=20,
)

edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)


capacity_matrix = [
    [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 Terminal 1
    [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 1 Terminal 2
    [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 2 Warehouse 1
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0],  # 3 Warehouse 2
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0],  # 4 Warehouse 3
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10],  # 5 Warehouse 4
    [0] * 20,  # 6 Shop 1
    [0] * 20,  # 7 Shop 2
    [0] * 20,  # 8 Shop 3
    [0] * 20,  # 9 Shop 4
    [0] * 20,  # 10 Shop 5
    [0] * 20,  # 11 Shop 6
    [0] * 20,  # 12 Shop 7
    [0] * 20,  # 13 Shop 8
    [0] * 20,  # 14 Shop 9
    [0] * 20,  # 15 Shop 10
    [0] * 20,  # 16 Shop 11
    [0] * 20,  # 17 Shop 12
    [0] * 20,  # 18 Shop 13
    [0] * 20,  # 19 Shop 14
]


def bfs(capacity_matrix, flow_matrix, source, sink, parent):
    visited = [False] * len(capacity_matrix)
    queue = deque([source])
    visited[source] = True

    while queue:
        current_node = queue.popleft()

        for neighbor in range(len(capacity_matrix)):
            if (
                not visited[neighbor]
                and capacity_matrix[current_node][neighbor]
                - flow_matrix[current_node][neighbor]
                > 0
            ):
                parent[neighbor] = current_node
                visited[neighbor] = True
                if neighbor == sink:
                    return True
                queue.append(neighbor)

    return False


def edmonds_karp(capacity_matrix, source, sink):
    num_nodes = len(capacity_matrix)
    flow_matrix = [[0] * num_nodes for _ in range(num_nodes)]
    parent = [-1] * num_nodes
    max_flow = 0

    while bfs(capacity_matrix, flow_matrix, source, sink, parent):
        path_flow = float("Inf")
        current_node = sink

        while current_node != source:
            previous_node = parent[current_node]
            path_flow = min(
                path_flow,
                capacity_matrix[previous_node][current_node]
                - flow_matrix[previous_node][current_node],
            )
            current_node = previous_node

        current_node = sink
        while current_node != source:
            previous_node = parent[current_node]
            flow_matrix[previous_node][current_node] += path_flow
            flow_matrix[current_node][previous_node] -= path_flow
            current_node = previous_node

        max_flow += path_flow

    return max_flow


def print_max_flow_table(capacity_matrix, labels_nodes):
    print(f"{'Store':<10}|", end="")
    for source in range(2):
        print(f"{labels_nodes[source]:^12}|", end="")
    print()

    print("-" * (11 + 2 * 13))

    for sink in range(6, 20):
        print(f"{labels_nodes[sink]:<10}|", end="")
        for source in range(2):
            max_flow = edmonds_karp(capacity_matrix, source, sink)
            print(f"{str(max_flow):^12}|", end="")
        print()


if __name__ == "__main__":
    plt.title("Directed Graph with Flow Capacities", fontsize=14)
    plt.axis("off")
    plt.show()
    print_max_flow_table(capacity_matrix, labels_nodes)
