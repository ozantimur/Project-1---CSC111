"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from dataclasses import dataclass


@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - name: The name of this location.
        - id_num: A unique integer identifier value for this location.
        - brief_description: A brief description shown when the player revisits the location.
        - long_description: A detailed and description shown the first time the player enters the location.
        - available_commands: A dictionary that maps command strings to the id_num of the destination location.
        - items: A list of item names present at this location.
        - visited: Whether the player has visited this location before.
        - availability: Whether this location is currently accessible to the player.

    Representation Invariants:
        - name != ""
        - id_num >= 0
        - brief_description != ""
        - long_description != ""
        - all(cmd != "" for cmd in available_commands)
        - all(isinstance(dest, int) and dest >= 0 for dest in available_commands.values())
        - all(isinstance(item, str) and item != "" for item in items)
    """
    name: str
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited_availability: dict[str, bool]
    # visited: bool
    # availability: bool


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: The name of this item.
        - start_position: The id number of the location where this item spawns in.
        - target_position: The id number of the location where this item is used.
        - available: Whether this item is currently available in the game.

    Representation Invariants:
        - name != ""
        - start_position >= 0
        - target_position >= 0
    """

    name: str
    start_position: int
    target_position: int
    target_points: int
    available: bool


class NPC:
    """A NPC in our text adventure game world.

    Instance Attributes:
        - name: The name of this NPC.
        - location: The id number of the location where this NPC is found.
        - speech: A list of dialogue strings spoken by the NPC in order.
        - options: A list of dictionaries mapping option numbers (as strings)
          to the corresponding option description shown to the player.
        - results: A list of dictionaries mapping option numbers (as strings)
          to a tuple of (response string, points earned).
        - interacted: Whether the player has already completed dialogue with this NPC.

    Representation Invariants:
        # TODO
        - name != ""
        - location >= 0
        - len(speech) == len(options) == len(results)
        - all(isinstance(line, str) and line != "" for line in speech)
        - all(isinstance(opt, dict) for opt in options)
        - all(isinstance(res, dict) for res in results)
        - for every index i, options[i].keys() == results[i].keys()
    """

    basic_info: dict[str, str | int | bool]
    speech: list[str]
    options: list[dict[str, str]]
    results: list[dict[str, float]]
    location: int

    def __init__(
            self,
            basic_info: tuple[str, int],
            speech: list[str],
            options: list[dict[str, str]],
            results: list[dict[str, float]]) -> None:

        """Initialize a new NPC."""
        self.basic_info = {"name": basic_info[0], "location": basic_info[1], "interacted": False}
        self.speech = speech
        self.options = options
        self.results = results

    def dialogue(self) -> tuple[float, bool]:
        """
        Handle the process of dialogue with NPC
        """
        # tracks the total score the player has earned through interacting with the NPC
        total_earned_score = 0
        player_input = "this is a place holder"
        index = 0
        if self.basic_info["interacted"]:
            print("You have already interacted with " + self.basic_info["name"] + ".")
            return 0.0, True

        # The "0" option is the "End conversation option"
        while (player_input != "quit" or player_input != "0") and index < len(self.speech):
            self.basic_info["interacted"] = True
            print(self.speech[index])  # What the NPC says
            print("Available options below: ")
            for option in self.options[index]:
                print(self.options[index][option])
            print()
            player_input = input("Select your option: ").strip()
            chosen_option = self.options[index].get(player_input)
            # Validate choice
            while not chosen_option:
                print("That was an invalid option: try again.\n")
                print("Available options below: ")
                for option in self.options[index]:
                    print(self.options[index][option])
                print()
                player_input = input("Select your option: ").strip()
                chosen_option = self.options[index].get(player_input)

            response, earned_score = self.results[index][player_input]
            print(response)
            total_earned_score += earned_score
            if player_input == "0":
                break
            index += 1
        print("\nDialogue is over.\n")

        if player_input == "quit":
            return total_earned_score, False
        elif player_input == "0":
            return total_earned_score, True
        return total_earned_score, True


if __name__ == "__main__":
    # pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })
