class Node:
    def __init__(self, value: str):
        self.value = value


class Chain:
    def __init__(self, values: list[str]):
        self.nodes = [Node(value) for value in values]
        self.links = self.nodes_to_links(self.nodes)

    def nodes_to_links(self, nodes: list[Node]) -> list[tuple]:
        """
        Args:
            nodes (list[Node]): A chain in the form (A, B, C, ...).

        Returns:
            list[tuple]: A chain in the form [(A, B), (B, C), ...].
        """

        return [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]

    def links_to_nodes(self, links: list[tuple]) -> list[Node]:
        """
        Args:
            links (list[tuple]): A chain in the form [(A, B), (B, C), ...].

        Returns:
            list[Node]: A chain in the form (A, B, C, ...).
        """

        return [link[0] for link in links] + [links[-1][1]]

    def get_values(self):
        return [node.value for node in self.nodes]

    def update_nodes(self):
        self.nodes = self.links_to_nodes(self.links)

    def update_links(self):
        self.links = self.nodes_to_links(self.nodes)


def input_chain() -> Chain:
    values = input("Type a list of names (separated by spaces):\n").split()

    return Chain(values)


def main():
    chain = Chain(["1", "2", "3", "4"])

    print(chain.get_values())


if __name__ == "__main__":
    main()
