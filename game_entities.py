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
        - # TODO Describe each instance attribute here

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.
    name: str
    id_num: int
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool
    availability: bool


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    start_position: int
    target_position: int
    target_points: int
    available: bool


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

class NPC:
    """A NPC in our text adventure game world.

        Instance Attributes:
            - self.options contains a mapping from the option number to the corresponding description

        Representation Invariants:
            - # TODO Describe any necessary representation invariants
        """

    name: str
    speech: list[str]
    options: list[dict[str, str]]
    results: list[dict[str, float]]
    location: int

    def __init__(
            self,
            name: str,
            location: int,
            speech: list[str],
            options: list[dict[str, str]],
            results: list[dict[str, float]]) -> None:

        """Initialize a new NPC."""
        self.name = name
        self.location = location
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
        # The "0" option is the "End conversation option"
        while player_input != "quit" or player_input != "0":
            print(self.speech[index])  # What the NPC say
            self.print_options()
            player_input = input("Select your option: ").strip()
            chosen_option = self.options[index].get(player_input)

            # Validate choice
            while not chosen_option:
                print("That was an invalid option: try again.\n")
                self.print_options()
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
            return 0.0, False
        elif player_input == "0":
            return 0.0, True
        return 0.0, True

    def print_options(self) -> None:
        """
        Handles printing the available options for the player to see
        """
        print("Available options below: ")
        for option in self.options:
            print(self.options[option])
        print()


if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })
