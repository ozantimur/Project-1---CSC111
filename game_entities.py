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
        - visited: Whether or not the player has visited this location before.
        - availability: Whether this location is currently accessible to the player.

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
        - 

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
            - # TODO Describe each instance attribute here

        Representation Invariants:
            - # TODO Describe any necessary representation invariants
        """

    name: str
    conversations: list[str]
    location: int
    plus_points: float
    minus_points: float

    def __init__(
        self,
        name: str,
        conversations: list[str],
        location: int,
        plus_points: float,
        minus_points: float
    ) -> None:
        """Initialize a new NPC."""
        self.name = name
        self.conversations = conversations
        self.location = location
        self.plus_points = plus_points
        self.minus_points = minus_points


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
