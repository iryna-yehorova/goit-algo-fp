import argparse
from collections import deque
import heapq

import matplotlib.pyplot as plt
import networkx as nx

from task_4 import heap_to_tree


def depth_first_search(root):
    if root is None:
        return []
    stack = [root]
    order = []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def breadth_first_search(root):
    if root is None:
        return []
    queue = deque([root])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


def visit_color(index, total):
    if total > 1000:
        raise ValueError("Для наочності можна малювати не більше 1000 вузлів")
    fraction = index / max(total - 1, 1)
    # Невелика зміна зеленого каналу розрізняє близькі відтінки.
    channels = (12 + int(212 * fraction),
                36 + int(200 * fraction) + index % 8,
                72 + int(183 * fraction))
    return "#{:02X}{:02X}{:02X}".format(*channels)


def tree_graph(root):
    graph = nx.DiGraph()
    positions = {root.id: (0, 0)}
    stack = [(root, 0, 0, 1)]
    while stack:
        node, x, y, layer = stack.pop()
        graph.add_node(node.id, label=node.val)
        for child, direction in ((node.left, -1), (node.right, 1)):
            if child is not None:
                graph.add_edge(node.id, child.id)
                child_x = x + direction / 2 ** layer
                positions[child.id] = (child_x, y - 1)
                stack.append((child, child_x, y - 1, layer + 1))
    return graph, positions


def draw_traversals(heap, output=None):
    root = heap_to_tree(heap)
    if root is None:
        raise ValueError("Неможливо обійти порожнє дерево")
    if len(heap) > 1000:
        raise ValueError("Для наочності можна малювати не більше 1000 вузлів")

    graph, positions = tree_graph(root)
    labels = nx.get_node_attributes(graph, "label")
    orders = (depth_first_search(root), breadth_first_search(root))
    node_ids = list(graph.nodes)
    colors = [visit_color(index, len(heap)) for index in range(len(heap))]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    for ax, order, title in zip(axes, orders, ("DFS — стек", "BFS — черга")):
        visited = {node.id: colors[index] for index, node in enumerate(order)}
        node_colors = [visited[node_id] for node_id in node_ids]
        nx.draw(graph, pos=positions, with_labels=False, arrows=False,
                node_size=1400, node_color=node_colors, ax=ax)
        dark_labels = {node_id: labels[node_id] for node_id in node_ids
                       if int(visited[node_id][1:3], 16) < 130}
        light_labels = {node_id: labels[node_id] for node_id in node_ids
                        if node_id not in dark_labels}
        nx.draw_networkx_labels(graph, positions, labels=dark_labels,
                                font_color="white", ax=ax)
        nx.draw_networkx_labels(graph, positions, labels=light_labels,
                                font_color="black", ax=ax)
        ax.set_title(title)

    if output:
        fig.savefig(output, bbox_inches="tight")
    else:
        plt.show()
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Візуалізація DFS та BFS бінарної купи")
    parser.add_argument("values", type=int, nargs="*", default=[12, 4, 15, 2, 9, 7, 20])
    parser.add_argument("-o", "--output", help="зберегти зображення у PNG-файл")
    args = parser.parse_args()
    if not args.values:
        parser.error("потрібне хоча б одне число")
    heapq.heapify(args.values)
    root = heap_to_tree(args.values)
    print("DFS:", [node.val for node in depth_first_search(root)])
    print("BFS:", [node.val for node in breadth_first_search(root)])
    draw_traversals(args.values, args.output)


if __name__ == "__main__":
    main()
