import numpy as np


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        self.length = n
        self.links = links

        # Map of possible locations for links
        self.bool_matrix = np.ones((self.length, self.length), dtype=bool)

        for link in self.links:
            self.strike_row_and_column(*link)

        # Map of links
        self.link_matrix = np.full((self.length, self.length), -1, dtype="i, i")

    def strike_row_and_column(self, x: int, y: int) -> None:
        self.bool_matrix[y, :] = False
        self.bool_matrix[:, x] = False
        self.bool_matrix[y, x] = True

    def get_possible_loops(self) -> list[tuple[int, int]]:
        if len(self.links) == self.length:
            return self.links

        for x, y in self.links:
            self.strike_row_and_column(x, y)

        link = self.links[0]
        while link != (-1, -1):
            link = self.link_matrix[link[1], link[0]]

        loops = []

        for i in range(self.length):
            if not self.bool_matrix[i, y]:
                continue

            new_loop = Loop(self.length, self.links + [(y, i)])
            loops += new_loop.get_possible_loops()

        return loops


def main():
    loop = Loop(5, [(0, 1), (2, 3)])

    print(loop.links)


if __name__ == "__main__":
    main()
