import math


info_file = "./info.txt"


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]):
        # TODO: Implement error checking
        self.length = n
        self.links = links
        self.loops: list[list[tuple[int, int]]] = []

        self.get_possible_loops(self.links)

    def number_of_loops(self) -> int:
        return math.factorial(self.length - len(self.links) - 1)

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


def override(index: int):
    file = open(info_file, "r")
    overridden = file.readlines()
    file.close()
    overridden.remove(overridden[index + 1])

    # Re-write the file, ommitting the overridden link
    _file = open("./info.txt", "w")
    _file.writelines(overridden)
    _file.close()


# A function which determines if the proposed link is valid, or whether it needs to override another
def validate_added_link(newinfo: str) -> bool:
    if len(newinfo.split()) != 2 or newinfo.split()[0] == newinfo.split()[1]:
        print("Invalid input: Ensure the input is in the form 'A B'\n")
        return False
    # Checking if the players exist
    elif (
        newinfo.split()[0] not in get_all_players()
        or newinfo.split()[1] not in get_all_players()
    ):
        print(
            f"Invalid input: {newinfo.split()[0] if newinfo.split()[0] not in get_all_players() else newinfo.split()[1]} is not a player\n"
        )
        return False

    # Converts the known links into lists of assassins and targets, with respective indices
    assassins, targets = [], []
    file = open(info_file, "r")
    for i in file.readlines()[1:]:  # First line of info.txt is a list of all players
        assassins.append(i.split()[0])
        targets.append(i.split()[1])
    file.close()

    if newinfo.split()[0] in assassins and newinfo.split()[1] in targets:
        print("CONFLICT:\n Link already exist\n")
        return False
    elif newinfo.split()[0] in assassins:
        ans = input(
            f"CONFLICT:\n{newinfo.split()[0]}'s target is {targets[assassins.index(newinfo.split()[0])]}.\nOverride? y/n\n"
        ).lower()
        if ans != "y":
            return False
        override(assassins.index(newinfo.split()[0]))
    elif newinfo.split()[1] in targets:
        ans = input(
            f"CONFLICT:\n{newinfo.split()[1]}'s assassin is {assassins[targets.index(newinfo.split()[1])]}.\nOverride? y/n\n"
        ).lower()
        if ans != "y":
            return False
        override(targets.index(newinfo.split()[1]))

    print("Validated successfully\n")
    return True


def add() -> None:
    newinfo = input(
        'Enter new information in the form of "A B", where A is the assassin and B is the target:\n'
    ).lower()
    if validate_added_link(newinfo):
        file = open(info_file, "a")
        file.write(newinfo + "\n")
        file.close()
    ui()


def num_of_possible_loops() -> int:
    # TODO: Determine the number of chains then use formula (n-1)!
    return "x"


# UI
def ui_view_links() -> None:
    input(f"{get_info()}")


def ui_view_chains() -> None:
    info = get_info()


def ui_view_loops() -> None:
    if num_of_possible_loops() > 20:
        print(f"There are {num_of_possible_loops()} possible loops, continue? y/n")
        ans = input().lower()
        if ans != "y":
            return


def ui_view() -> None:
    a = input(
        "1: View all chains\n2: Print all possible loops\n3: View all links\n4: Exit\n"
    )

    if a == "1":
        ui_view_chains()
    elif a == "2":
        num_of_possible_loops()
    elif a == "3":
        ui()
    elif a == "4":
        return
    else:
        print("Invalid input")
    ui_view()


def ui() -> None:
    a = input("1: Add information\n2: View information\n3: Save and Exit\n")

    if a == "1":
        print("\nADD INFORMATION\n\n")
        add()
    elif a == "2":
        print("\nVIEW INFORMATION\n\n")
        ui_view()
    elif a == "3":
        return
    else:
        print("Invalid input")
        ui()


def get_info() -> list[tuple[str, str]]:
    return [
        (line.split()[0], line.split()[1]) for line in open(info_file, "r").readlines()
    ]


def input_chain() -> Chain:
    values = input("Type a list of names (separated by spaces):\n").split()

    return Chain(values)


def get_all_players() -> list[str]:
    _infofile = open(info_file, "r")
    players = _infofile.readlines()[0]
    _infofile.close()
    return players.split()


def main():
    # Debugging
    my_loop = Loop(5, [(0, 1), (2, 3)])
    # Debugging
    my_loop = Loop(5, [(0, 1), (2, 3)])

    print(my_loop.number_of_loops())
    ui()
    exit()


if __name__ == "__main__":
    main()
