import random
import argparse
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt


def create_test_list(n) -> list:
    level = 1
    nodes = [
            {"job_name": "root", "level": 0, "index": 0},
    ]
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
                self.set_parent_cache(self.ROOT_LEVEL, node)
                node.update({"parent_name": None, "parent_id": None})
            elif level > self.previous_level:
                parent_info = self.parent_cache.get(self.previous_level)
                node.update(parent_info)
                self.set_parent_cache(level, node)
            elif level < self.previous_level:
                parent_info = self.parent_cache.get(level-1)
                node.update(parent_info)
                self.set_parent_cache(level, node)
            else:
                parent_info = self.parent_cache.get(level-1)
                node.update(parent_info)
                self.set_parent_cache(level, node)
            self.previous_level = level
        return nodes

    def set_parent_cache(self, level, node) -> None:
        parent_info = {"parent_name": node["job_name"], "parent_id": node["index"]}
        self.parent_cache[level] = parent_info

    def visualize_parents(self):
        nodes = self.build_nodes()

        for node in nodes:
            print(node)

        edges = [(node["index"], node["parent_id"]) for node in nodes if node["level"]]
        labels = {node["index"]: node["job_name"] for node in nodes}

        fig = plt.figure(figsize=(20, 10))
        g = nx.Graph()
        g.add_edges_from(edges)
        nx.draw_networkx(g, arrows=True, labels=labels)
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
