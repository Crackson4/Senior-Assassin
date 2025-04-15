import math


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        # TODO: Implement error checking
        self.length = n
        self.links = links
        self.loops: list[list[tuple[int, int]]] = []

        eliminated_rows = set(y for _, y in self.links)
        eliminated_rows.add(self.links[0][0])
        self.get_possible_loops([self.links[0]], eliminated_rows)

    def number_of_loops(self) -> int:
        return math.factorial(self.length - len(self.links) - 1)

    def get_possible_loops(
        self, curr_loop: list[tuple[int, int]], eliminated_rows: set[int]
    ) -> None:
        """
        Calculates all possible loops containing the given links.

        Args:
            curr_loop (link[tuple[int, int]]): The current state of the loop.
            eliminated_rows (set[int]): The rows that already contain links.
        """

        # TODO: Provide a detailed explanation for this function

        # TODO: Debug function

        # TODO: Implement error checking

        # If all connections have been explored, add the last link and return the loop

        if len(curr_loop) == self.length - 1:
            total = self.length * (self.length - 1) // 2
            last_link = (
                total - sum(x for x, _ in curr_loop),
                total - sum(y for _, y in curr_loop),
            )
            self.loops.append(curr_loop + [last_link])
            return

        _, y = curr_loop[-1]

        # Explore all possible connections from the current node

        for i in range(self.length):
            if i == y or i in eliminated_rows:
                continue

            # Add a link and recursively explore the next node

            new_link = (y, i)
            eliminated_rows.add(i)
            self.get_possible_loops(curr_loop + [new_link], eliminated_rows)


def main():
    # Debugging
    my_loop = Loop(5, [(0, 1), (2, 3)])

    print(my_loop.loops)


if __name__ == "__main__":
    main()
