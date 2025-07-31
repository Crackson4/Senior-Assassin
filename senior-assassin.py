import math


info_file = "./info.txt"


class Loop:
    def __init__(self, n: int, links: list[tuple[int, int]]) -> None:
        # TODO: Implement error checking

        self.length = n
        self.links = links
        self.links_dict = {link[0]: link[1] for link in self.links}
        self.loops: list[list[tuple[int, int]]] = []

    def number_of_loops(self) -> int:
        return math.factorial(self.length - len(self.links) - 1)

    def update_possible_loops(
        self, curr_loop: list[tuple[int, int]], eliminated_rows: set[int]
    ) -> None:
        """
        Calculates all possible loops containing the given links.

        Args:
            curr_loop (link[tuple[int, int]]): The current state of the loop.
            eliminated_rows (set[int]): The rows that already contain links.
        """

        # TODO: Provide a detailed explanation for this function

        # TODO: Implement error checking

        _, y = curr_loop[-1]

        # If all connections have been explored, add the last link and return the loop

        if len(curr_loop) == self.length - 2:
            n = self.length * (self.length - 1) // 2
            last_row = (
                n - sum([link[0] for link in curr_loop]) - curr_loop[-1][1]
            )

            curr_loop.append((y, last_row))
            curr_loop.append((last_row, curr_loop[0][0]))

            self.loops.append(curr_loop)

            return

        # Check if the next link is already known

        if y in self.links_dict:
            n = self.links_dict[y]
            new_link = (y, n)
            self.update_possible_loops(
                curr_loop + [(y, n)], eliminated_rows.union({n})
            )

            return

        # Explore all possible connections from the current link

        for i in range(self.length):
            if i == y or i in eliminated_rows:
                continue

            # Add a link and recursively explore the next links

            new_link = (y, i)
            self.update_possible_loops(
                curr_loop + [new_link], eliminated_rows.union({i})
            )


class UI:
    def __init__(self) -> None:
        file = open(info_file, "r")
        data = file.readlines()
        file.close()

        self.players = data[0].split() if data else []

        self.player_dict = {
            self.players[i]: i for i in range(len(self.players))
        }

        self.links = (
            [tuple(line.split()) for line in data[1:]] if len(data) > 1 else []
        )

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
        if link not in self.links:
            print("Invalid input: Link does not exist")
            return

        self.links.remove(link)

    def add_link(self, link: tuple[str, str]) -> None:
        self.validate_link(link)
        self.links.append(link)

    # A function which determines if the proposed link is valid, or whether it needs to override another
    # TODO: Replace ValueErrors with regular prints

    def validate_link(self, link: tuple[str, str]) -> None:
        # Checking that the link is in the correct format
        if len(link) != 2 or link[0] == link[1]:
            raise ValueError("Ensure the input is in the form 'name_1 name_2'")

        if self.players == []:
            return

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

    def print_links(self) -> None:
        for link in self.links:
            print(f"{link[0]} -> {link[1]}")

    def print_loops(self) -> None:
        loop_finder = Loop(
            len(self.players),
            [self.link_string_to_int(link) for link in self.links],
        )

        n = loop_finder.number_of_loops()

        if n > 24:
            if not self.prompt(
                f"There are {n} possible loops. Continue? [y/N] "
            ):
                return

        eliminated_rows = set(y for _, y in loop_finder.links)
        eliminated_rows.add(loop_finder.links[0][0])

        loop_finder.update_possible_loops(
            [loop_finder.links[0]], eliminated_rows
        )

        for loop in loop_finder.loops:
            print(
                "\t".join(
                    f"{link[0]} -> {link[1]} "
                    for link in map(self.link_int_to_string, loop)
                )
            )

    # TODO: Clean up output of UI methods

    def ui_home(self) -> None:
        while True:
            choice = input("1: Edit\n2: View\n3: Exit\n")

            if not (choice.isdigit() and 1 <= int(choice) <= 3):
                print("Invalid input: Input must be a number between 1 and 3")
                continue

            if choice == "1":
                self.ui_edit()

            if choice == "2":
                self.ui_view()

            if choice == "3":
                if self.prompt("Save changes? [Y/n] ", True):
                    self.save_info()

                exit(0)

    # TODO: Enable the user to add nodes

    def ui_edit(self) -> None:
        while True:
            choice = input("1: Add link\n2: Remove link\n3: Back\n")

            if not (choice.isdigit() and 1 <= int(choice) <= 4):
                print("Invalid input: Input must be a number between 1 and 4")
                continue

            if choice == "1":
                user_input = input("Enter a link in the form 'name_1 name_2': ")
                link = tuple(user_input.split())

                self.add_link(link)

            # TODO: Display known links above prompt

            if choice == "2":
                user_input = input("Enter a link in the form 'name_1 name_2': ")
                link = tuple(user_input.split())

                self.remove_link(link)

            if choice == "3":
                break

    def ui_view(self) -> None:
        while True:
            choice = input("1: Current links\n2: Possible loops\n3: Back\n")

            if not (choice.isdigit() and 1 <= int(choice) <= 3):
                print("Invalid input: Input must be a number between 1 and 3")
                continue

            if choice == "1":
                self.print_links()

            if choice == "2":
                self.print_loops()

            if choice == "3":
                break

    def save_info(self) -> None:
        file = open(info_file, "w")

        file.write(" ".join(self.players) + "\n")
        file.writelines([" ".join(link) + "\n" for link in self.links])

        file.close()


def main():
    ui = UI()
    ui.ui_home()


if __name__ == "__main__":
    main()
