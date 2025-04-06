class Node:
    def __init__(self, value: str):
        self.value = value


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        self.length = n
        self.links = links


def main():
    loop = Loop(5, [(0, 1), (2, 3)])

    print(loop.links)


if __name__ == "__main__":
    main()
