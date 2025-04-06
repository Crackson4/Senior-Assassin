import numpy as np


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        self.length = n
        self.links = links
        self.bool_matrix = np.ones((self.length, self.length), dtype=bool)
        self.link_matrix = np.full((self.length, self.length), -1, dtype="i, i")

    def strike_row_and_column(self, x, y):
        self.bool_matrix[y, :] = False
        self.bool_matrix[:, x] = False
        self.bool_matrix[y, x] = True


def main():
    loop = Loop(5, [(0, 1), (2, 3)])

    print(loop.links)


if __name__ == "__main__":
    main()
