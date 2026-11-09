import argparse
import heapq
import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def heap_to_tree(heap):
    if not heap:
        return None

    nodes = [Node(value) for value in heap]
    for index, node in enumerate(nodes):
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < len(nodes):
            node.left = nodes[left_index]
        if right_index < len(nodes):
            node.right = nodes[right_index]
    return nodes[0]


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    graph.add_node(node.id, color=node.color, label=node.val)
    for child, direction in ((node.left, -1), (node.right, 1)):
        if child is not None:
            graph.add_edge(node.id, child.id)
            child_x = x + direction / 2 ** layer
            pos[child.id] = (child_x, y - 1)
            add_edges(graph, child, pos, child_x, y - 1, layer + 1)
    return graph


def draw_heap(heap, output=None):
    root = heap_to_tree(heap)
    if root is None:
        raise ValueError("Неможливо намалювати порожню купу")

    graph = nx.DiGraph()
    positions = {root.id: (0, 0)}
    add_edges(graph, root, positions)
    colors = [data["color"] for _, data in graph.nodes(data=True)]
    labels = {node_id: data["label"] for node_id, data in graph.nodes(data=True)}

    levels = len(heap).bit_length()
    fig, ax = plt.subplots(figsize=(max(8, 2 ** (levels - 1) * 1.4), max(5, levels * 1.5)))
    nx.draw(graph, pos=positions, labels=labels, arrows=False,
            node_size=1800, node_color=colors, ax=ax)
    ax.set_title("Бінарна мін-купа")
    if output:
        fig.savefig(output, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Візуалізація бінарної мін-купи")
    parser.add_argument("values", type=int, nargs="*", default=[12, 4, 15, 2, 9, 7, 20])
    parser.add_argument("-o", "--output", help="зберегти зображення замість показу у вікні")
    args = parser.parse_args()
    if not args.values:
        parser.error("потрібне хоча б одне число")
    heapq.heapify(args.values)
    print("Купа у вигляді масиву:", args.values)
    draw_heap(args.values, args.output)


if __name__ == "__main__":
    main()
