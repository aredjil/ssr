import networkx as nx
import matplotlib.pyplot as plt

def build_ssr_graph(N: int):
    """Standard SSR graph: edges from s -> {1,...,s-1} with uniform probability."""
    G = nx.DiGraph()
    G.add_nodes_from(range(1, N + 1))

    for s in range(2, N + 1):
        for j in range(1, s):
            G.add_edge(s, j, prob=1 / (s - 1))
    return G

N = 3
G = build_ssr_graph(N)

# Circular layout
pos = nx.circular_layout(G)

plt.figure(figsize=(7, 7))

# Draw nodes, color node 1 red
node_colors = ["red" if node == 1 else "lightblue" for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_size=1200, node_color=node_colors, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=12)

# Draw edges with large arrowheads
nx.draw_networkx_edges(
    G, pos,
    arrows=True, arrowstyle='-|>', arrowsize=25,
    connectionstyle='arc3,rad=0.1',
    min_source_margin=25, min_target_margin=25
)

# Build edge labels as P(j|i)
edge_labels = {(i, j): f"P({j}|{i})={G[i][j]['prob']:.2f}" for i, j in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, label_pos=0.5)

plt.title(f"SSR Graph (N={N})")
plt.axis("off")
plt.tight_layout()
plt.savefig(f"./results/ssr_graph_{N}.png")
plt.show()
