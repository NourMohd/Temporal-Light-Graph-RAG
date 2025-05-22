import pipmaster as pm

# Ensure dependencies
for pkg in ("pyvis", "networkx"):
    if not pm.is_installed(pkg):
        pm.install(pkg)

import argparse
import random
import networkx as nx
from pyvis.network import Network

def main(graph_path: str, k: int, top_n: int, seed: int = None):
    # Optional: seed the RNG for reproducibility
    if seed is not None:
        random.seed(seed)

    # Load the full graph
    G = nx.read_graphml(graph_path)

    # 1. Compute and sort node degrees descending
    deg_list = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    top_nodes = [node for node, deg in deg_list[:top_n]]

    # 2. Choose a random root among those top N
    root = random.choice(top_nodes)
    print(f"Selected root node (from top {top_n} by degree): {root!r}")

    # 3. Extract its k-hop ego subgraph
    subG = nx.ego_graph(G, root, radius=k)

    # 4. Create a Pyvis network for that subgraph
    net = Network(height="100vh", notebook=True)
    net.from_nx(subG)

    # 5. Style nodes and edges
    for node in net.nodes:
        node["color"] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        desc = G.nodes[node["id"]].get("description")
        if desc:
            node["title"] = desc

    for edge in net.edges:
        # Force every edge to a fixed thin width
        edge["width"] = 1

        # If you still want titles from your original descriptions:
        src, dst = edge["from"], edge["to"]
        desc = G.edges[src, dst].get("description")
        if desc:
            edge["title"] = desc

    # 6. Save and display
    out_file = "knowledge_graph_subgraph.html"
    net.show(out_file)
    print(f"Subgraph visualization written to {out_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Plot a k-hop subgraph around a random high-degree node."
    )
    parser.add_argument(
        "--graph_path", "-g",
        default="/content/LightRAGTest/LightRAG/news_index/graph_chunk_entity_relation.graphml",
        help="Path to your GraphML file."
    )
    parser.add_argument(
        "--k", "-k",
        type=int,
        default=2,
        help="Number of hops for the ego subgraph."
    )
    parser.add_argument(
        "--top_n", "-n",
        type=int,
        default=100,
        help="Number of highest-degree nodes to choose from."
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        default=None,
        help="Random seed (optional) for reproducibility."
    )

    args = parser.parse_args()
    main(args.graph_path, args.k, args.top_n, args.seed)
