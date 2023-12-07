import random
import argparse
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt


def create_test_list(n) -> list:
    level = 1
    nodes = [{"job_name": "root", "level": 0, "index": 0}]
    for i in range(n):
        if i == 0:
            level = 1
        else:
            level -= random.randint(-1, 1)
        if level == 0:
            level += 1
        node = {"job_name": f"{i}-{level}", "level": level, "index": i+1}
        nodes.append(node)
    return nodes


class TreeBuilder:
    ROOT_LEVEL = 0

    def __init__(self, data):
        self.data = data
        self.previous_level = self.ROOT_LEVEL
        self.parent_cache = {}

    def build_nodes(self):
        nodes = self.data.copy()
        for node in nodes:
            level = node["level"]
            if level == self.ROOT_LEVEL:
                self.set_parent_for_level(self.ROOT_LEVEL, node)
                node.update({"parent_name": None, "parent_id": None})
            elif level > self.previous_level:
                parent_info = self.get_parent_for_level(self.previous_level)
                node.update(parent_info)
                self.set_parent_for_level(level, node)
            elif level < self.previous_level:
                parent_info = self.get_parent_for_level(level-1)
                node.update(parent_info)
                self.set_parent_for_level(level, node)
            else:
                parent_info = self.get_parent_for_level(level-1)
                node.update(parent_info)
                self.set_parent_for_level(level, node)
            self.previous_level = level
        return nodes

    def set_parent_for_level(self, level: int, node: dict) -> None:
        parent_info = {"id": node["index"], "name": node["job_name"]}
        self.parent_cache[level] = parent_info

    def get_parent_for_level(self, level_to_get: int) -> dict:
        parent = self.parent_cache.get(level_to_get)
        return {"parent_id": parent["id"], "parent_name": parent["name"]}

    def visualize_parents(self):
        nodes = self.build_nodes()

        for node in nodes:
            print(node)

        edges = [(node["index"], node["parent_id"]) for node in nodes if node["level"]]
        labels = {node["index"]: node["job_name"] for node in nodes}

        fig = plt.figure(figsize=(20, 10))
        g = nx.DiGraph()
        g.add_edges_from(edges)
        root_edges = [(edge[0], edge[1]) for edge in edges if edge[1] == 0]
        non_root_edges = [(edge[0], edge[1]) for edge in edges if edge[1] != 0]
        print(root_edges)
        print(non_root_edges)

        pos = nx.spring_layout(g)
        nx.draw_networkx_nodes(g, pos, node_size=900)
        nx.draw_networkx_labels(g, pos, labels=labels)
        nx.draw_networkx_edges(
                g, pos,
                edgelist=root_edges, edge_color='red', width=3,
                arrowstyle="<|-", arrows=True, arrowsize=20
        )
        nx.draw_networkx_edges(
                g, pos,
                edgelist=non_root_edges, edge_color='green', width=2,
                arrowstyle="<|-", arrows=True, arrowsize=20
        )

        plt.show()
        plt.tight_layout()
        fp = Path(Path.cwd(), "nodes.pdf")
        fig.savefig(fp)
        plt.close(fig)


def pars_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=int, default=10, help="Number of nodes to test with")
    args = parser.parse_args()
    return args.nodes


def main():
    number_of_nodes = pars_args()
    data = create_test_list(number_of_nodes)
    builder = TreeBuilder(data=data)
    builder.visualize_parents()


if __name__ == '__main__':
    main()
