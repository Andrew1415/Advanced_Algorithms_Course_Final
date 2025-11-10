import networkx as nx
import matplotlib.pyplot as plt

# ------------------------------------------------
# 1) Tinklo kūrimas
# ------------------------------------------------
G = nx.DiGraph()

# Pridedam briaunas: (šaltinis, tikslas, cost, capacity)
edges = [
    ("A", "B", {"weight": 4, "capacity": 5}),
    ("A", "C", {"weight": 2, "capacity": 7}),
    ("B", "C", {"weight": -1, "capacity": 3}),
    ("B", "D", {"weight": 2, "capacity": 4}),
    ("C", "D", {"weight": 3, "capacity": 6}),
    ("C", "E", {"weight": 2, "capacity": 3}),
    ("D", "E", {"weight": -2, "capacity": 8}),
]

G.add_edges_from(edges)

source = "A"
target = "E"

# ------------------------------------------------
# 2) Bellman–Ford algoritmas – trumpiausi keliai
# ------------------------------------------------
try:
    lengths, paths = nx.single_source_bellman_ford(G, source, weight="weight")
    print("=== Bellman–Ford trumpiausi keliai nuo", source, "===")
    for node in G.nodes:
        if node in lengths:
            print(f"{source} → {node}: atstumas = {lengths[node]}, kelias = {paths[node]}")
        else:
            print(f"{source} → {node}: nėra kelio")
except nx.NetworkXUnbounded:
    print("Tinkle yra neigiamas ciklas!")

# ------------------------------------------------
# 3) Edmonds–Karp algoritmas (maksimalus srautas)
# ------------------------------------------------
flow_value, flow_dict = nx.maximum_flow(G, source, target, capacity="capacity")
print("\n=== Edmonds–Karp maksimalus srautas ===")
print(f"Maksimalus srautas iš {source} į {target}: {flow_value}")
for u, flows in flow_dict.items():
    for v, f in flows.items():
        if f > 0:
            print(f"  {u} → {v}: srautas = {f}")

# ------------------------------------------------
# 4) Vizualizacija su NetworkX
# ------------------------------------------------

# Bendras tinklas
pos = nx.spring_layout(G, seed=42)  # gražesnis išdėstymas

# Pavaizduojam visas briaunas su svoriais
edge_labels = { (u,v): f"{d['weight']}/{d['capacity']}" for u,v,d in G.edges(data=True) }

plt.figure(figsize=(10,7))
nx.draw_networkx_nodes(G, pos, node_color="#8fd3f4", node_size=1200, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

# Paryškinam trumpiausią kelią nuo source iki target
if target in paths:
    shortest_path_edges = list(zip(paths[target], paths[target][1:]))
else:
    shortest_path_edges = []

nx.draw_networkx_edges(G, pos, width=2, edge_color="#999999", arrows=True, alpha=0.6)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black")

# Paryškinam trumpiausio kelio briaunas
if shortest_path_edges:
    nx.draw_networkx_edges(G, pos, edgelist=shortest_path_edges, width=3, edge_color="red", arrows=True)

plt.title("Tinklo vizualizacija: cost/capacity (raudona – trumpiausias kelias)", fontsize=13)
plt.axis("off")
plt.show()

# ------------------------------------------------
# 5) Papildoma vizualizacija – srauto dydžiai
# ------------------------------------------------
plt.figure(figsize=(10,7))
flow_edges = [(u,v) for u in flow_dict for v in flow_dict[u] if flow_dict[u][v] > 0]
flow_values = [flow_dict[u][v] for u,v in flow_edges]

nx.draw_networkx_nodes(G, pos, node_color="#baffc9", node_size=1200, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
nx.draw_networkx_edges(G, pos, edgelist=flow_edges, width=3, edge_color="green", arrows=True)
nx.draw_networkx_edge_labels(G, pos, edge_labels={e: f"{flow_dict[e[0]][e[1]]}" for e in flow_edges}, font_color="darkgreen")

plt.title(f"Maksimalus srautas iš {source} į {target}: {flow_value}", fontsize=13)
plt.axis("off")
plt.show()
