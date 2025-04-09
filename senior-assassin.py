import math


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        # TODO: Implement error checking
        self.length = n
        self.links = links
        self.loops: list[list[tuple[int, int]]] = []

        self.get_possible_loops(self.links)

    def get_possible_loops(self, links: list[tuple[int, int]]) -> None:
        # TODO: Provide an explanation for this function

        # TODO: Debug function

        # TODO: Implement error checking

        x, y = links[0]

        eliminated_columns = set()
        eliminated_rows = {x}

        for p, q in links:
            eliminated_columns.add(p)
            eliminated_rows.add(q)

        for i in range(self.length):
            if i == y or i in eliminated_rows:
                continue

            # TODO: Consider when the new_link is already in links
            new_link = (y, i)
            self.get_possible_loops([new_link] + links)

        if len(links) < self.length - 1:
            return

        total = self.length * (self.length - 1) // 2
        last_link = (
            total - sum(eliminated_columns),
            total - sum(eliminated_rows),
        )

        self.loops.append([last_link] + links)

    def number_of_loops(self) -> int:
        return math.factorial(self.length - len(self.links) - 1)


def main():
    # Debugging
    my_loop = Loop(5, [(0, 1), (2, 3)])

    print(my_loop.number_of_loops())


if __name__ == "__main__":
    main()
