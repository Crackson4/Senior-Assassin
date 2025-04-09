info_file = "./info.txt"
players = open(info_file, "r").readline(1).split()


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
    elif newinfo.split()[0] not in players or newinfo.split()[1] not in players:
        print(
            f"Invalid input: {newinfo.split()[0] if newinfo.split()[0] not in players else newinfo.split()[1]} is not a player\n"
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
        print(f"CONFLICT:\n Link already exist\n")
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


def main():
    ui()
    exit()


if __name__ == "__main__":
    main()
