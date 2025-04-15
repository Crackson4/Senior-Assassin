import math


info_file = "./info.txt"


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]) -> None:
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


class UI:
    def __init__(self) -> None:
        file = open(info_file, "r")
        data = file.readlines()
        file.close()

        self.players = data[0].split()
        self.links = [tuple(line.split()) for line in data[1:]]

        self.player_dict = {self.players[i]: i for i in range(len(self.players))}

    def prompt(self, message: str, default_yes=False) -> bool:
        response = input(message)

        if default_yes:
            return response.lower() != "n"

        return response.lower() == "y"

    def link_string_to_int(self, link: tuple[str, str]) -> tuple[int, int]:
        return self.player_dict[link[0]], self.player_dict[link[1]]

    def link_int_to_string(self, link: tuple[int, int]) -> tuple[str, str]:
        return self.players[link[0]], self.players[link[1]]

    def remove_link(self, link: tuple[str, str]) -> None:
        self.links.remove(link)

    # TODO: Allow user input in referencing function
    def add_link(self, link: tuple[str, str]) -> None:
        self.validate_link(link)
        self.links.append(link)

    def replace_link(self, link: tuple[str, str], new_link: tuple[str, str]) -> None:
        self.remove_link(link)
        self.add_link(new_link)

    # A function which determines if the proposed link is valid, or whether it needs to override another
    def validate_link(self, link: tuple[str, str]) -> None:
        # Checking that the link is in the correct format
        if len(link) != 2 or link[0] == link[1]:
            raise ValueError("Ensure the input is in the form 'name_1 name_2'")

        x, y = link

        # Checking if the players exist
        if x not in self.players:
            raise ValueError(f"{x} is not a player")
        if y not in self.players:
            raise ValueError(f"{y} is not a player")

        # Checking if the link already exists
        if link in self.links:
            raise ValueError("Link already exists")

        # Converts the known links into lists of assassins and targets, with respective indices
        assassin_dict = {link[0]: link for link in self.links}
        target_dict = {link[1]: link for link in self.links}

        if x in assassin_dict:
            if not self.prompt(f"{x} already has a target. Override? [y/N] "):
                raise ValueError(f"{x} already has a target")

            self.remove_link(assassin_dict[x])

        if y in target_dict:
            if not self.prompt(f"{y} is already a target. Override? [y/N] "):
                raise ValueError(f"{y} is already a target")

            self.remove_link(target_dict[y])


# UI
def ui_view_links() -> None:
    input(f"{get_info()}")


def ui_view_chains() -> None:
    info = get_info()


def ui_view_loops() -> None:
    if num_of_possible_loops() > 24:
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
        ui_view_loops()
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


def get_all_players() -> list[str]:
    _infofile = open(info_file, "r")
    players = _infofile.readlines()[0]
    _infofile.close()
    return players.split()


def main():
    # Debugging
    ui = UI()

    print("Players:", ui.players, sep="\t")

    for link in [("b", "c"), ("h", "d"), ("b", "d")]:
        ui.add_link(link)
        print("Links:\t", ui.links, sep="\t")


if __name__ == "__main__":
    main()
