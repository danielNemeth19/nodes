import networkx as nx
import matplotlib.pyplot as plt


def create_test_list() -> list:
    test_data = [
            {"job_name": "root", "level": 0},
            {"job_name": "A", "level": 1},
            {"job_name": "A1", "level": 2},
            {"job_name": "A2", "level": 2},
            {"job_name": "B", "level": 1},
            {"job_name": "B1", "level": 2},
            {"job_name": "BB1", "level": 3},
            {"job_name": "BB2", "level": 3},
            {"job_name": "C", "level": 1}
    ]

    for i, data in enumerate(test_data):
        data['index'] = i
    return test_data


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
            elif level == self.previous_level:
                parent_info = self.parent_cache.get(level-1)
                node.update(parent_info)
            self.previous_level = level
        return nodes

    def set_parent_cache(self, level, node) -> None:
        parent_info = {"parent_name": node["job_name"], "parent_id": node["index"]}
        self.parent_cache[level] = parent_info

    def visualize_parents(self):
        nodes = self.build_nodes()
        edges = [(node["index"], node["parent_id"]) for node in nodes if node["level"]]
        labels = {node["index"]: node["job_name"] for node in nodes}
        g = nx.Graph()
        g.add_edges_from(edges)
        nx.draw_networkx(g, labels=labels)
        plt.show()


def main():
    data = create_test_list()
    builder = TreeBuilder(data=data)
    builder.visualize_parents()


if __name__ == '__main__':
    main()
