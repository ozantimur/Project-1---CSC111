"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2026 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from os import remove
from typing import Optional

from game_entities import Location, Item, NPC
from event_logger import Event, EventList
from leaderboard import Leaderboard


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The id of the player's current Location.
        - ongoing: Whether or not the game is currently active.
        - _locations: A mapping from location id numbers to Location objects.
        - _items: A list of all item objects in the game.
        - _npcs: A list of all NPC objects in the game.
        - _current_items: A list of items currently in the player's inventory.
        - _visited_locations: A list of locations the player has visited.
        - _points: The player's current point score.
        - _remaining_moves: The number of moves the player has remaining.

    Representation Invariants:
        - current_location_id in _locations
        - all(item in _items for item in _current_items)
        - _remaining_moves >= 0
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    _npcs: list[NPC]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    _current_items: list[Item]
    _visited_locations = list[Location]
    _points: int  # the points the player has
    remaining_moves: int

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing
        self._points = 0
        self.remaining_moves = 100

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], list[NPC]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        # this is a dictionary
        locations = {}
        items = []
        npcs = []

        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['name'], loc_data['id'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'],
                                    loc_data['availability'] == "True")
            locations[loc_data['id']] = location_obj

        for item_data in data["items"]:
            item_obj = Item(item_data['name'], item_data['start_position'], item_data['target_position'],
                            item_data['target_points'], True)
            items.append(item_obj)

        for npc_data in data["npcs"]:
            npc_obj = NPC(npc_data['name'], npc_data['conversations'], npc_data['location'],
                            npc_data['plus_points'], npc_data['minus_points'])
            npcs.append(npc_obj)

        return locations, items, npcs

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # YOUR CODE BELOW
        if loc_id is not None:
            return self._locations[loc_id]
        else:
            return self._locations[self.current_location_id]

    def inventory(self) -> list[Item]:
        """Return the current inventory of the player while the game is played.
        """
        return self._current_items

    def move(self, desired_command: str) -> None:
        """Move the player to the new location based on the command
        Return True if the destination is valid, otherwise False
        """
        current_location = self._locations[self.current_location_id]
        if desired_command in current_location.available_commands:
            # current_location.availability marks whether the player needs an item to enter the location
            if current_location.availability:
                self.current_location_id = current_location.available_commands[desired_command]
                return
            else:
                # Note that id 2 is the id for the dorm room
                if current_location.available_commands[desired_command] == 2:
                    self._unlock()
                else:
                    self._swipe(self._locations[current_location.available_commands[desired_command]])
        return

    def _unlock(self) -> None:
        """
        Handle the unlocking process
        """
        # Check if the player has a key or not
        key = None
        for item in self._current_items:
            if item.name.endswith('key'):
                key = item
        if key:
            print(f"You have unlocked the door using your {key.name}. ", sep="", end="")
        else:
            print("Oh no! You have forgot to take your room key! Head down to front desk to ask for a temporary key. ")

    def _swipe(self, destination: Location) -> None:
        """
        Handle the process of scanning t-card
        """
        # Checks whether the player has the t-card on themselves
        if any([item.name == 't-card' for item in self._current_items]):
            print(f"You have swiped your t-card to enter {destination.name}. ", sep="", end="")
            return
        else:
            print(f"{destination.name} requires you to swipe your t-card to enter. However, you do not have it on you.")
            return

    def pick_up(self, desired_item: str) -> bool:

        """
        Pick up the item the player wants.
        If the desired item is within the player's current location, mutate self._current_items by appending the item,
            and return True to represent a successful interaction
        If the desired item is NOT within the player's current location, self._current_items remains unmuated,
            and return False to represent an unsuccessful interaction

        Mutate the item's availability correspondingly
        """
        if desired_item == '':
            return False
        else:
            if desired_item in self._locations[self.current_location_id].items:
                for i in range(len(self._items)):
                    # finding the correct item using its name
                    if self._items[i].name == desired_item:
                        self._current_items.append(self._items[i])
                        self._items[i].available = False

                        # check if the player has picked up items that are already dropped at the target position,
                        # if so, then the appropriate points will be deducted as the player must have received the
                        # same amount of points by dropping the item at the target position
                        if self._items[i].target_position == self.current_location_id:
                            self._points -= self._items[i].target_points
                        return True
        return False

    def drop(self, desired_item: str) -> bool:
        """
        Drop the item the player wants to.
        If the desired item is in the player's inventory, mutate self._current_items by popping the item,
            and return True to represent a successful interaction.
        If the desired item is NOT in the player's inventory, self._current_items remains unmutated,
            and return False to represent an unsuccessful interaction

        Update points correspondingly
        """
        if desired_item == '':
            return False
        else:
            if desired_item in self._current_items:
                for i in range(len(self._items)):
                    if self._items[i].name == desired_item:
                        # update the availability of the item
                        self._items[i].available = True
                        # check if the player has dropped the item at the target location
                        if self.current_location_id == self._items[i]:
                            # if so, reward the player with the corresponding amount of points
                            self._points += self._items[i].target_points

                        self._current_items.remove(self._items[i])
                        return True
            return False

    def score(self) -> float:
        """Return the player's score so far
        """
        return self._points

    def look(self) -> str:
        """
        Return the full description of the current location
        """
        return self._locations[self.current_location_id].long_description
    # drop method, update points




if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    # })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 2)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None

    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        game_log.add_event(Event(location.id_num, location.long_description))

        # YOUR CODE HERE
        if location.visited:
            print(location.long_description)
        else:
            print(location.brief_description)
            location.visited = True

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu:
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            if choice == "log":
                game_log.display_events()
                
            elif choice == "score":
                print(game.score())
            elif choice == "look":
                print(game.look())
            elif choice == "inventory":
                print(game.inventory())
            elif choice == "quit":
                game.ongoing = False

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result
            game.remaining_moves -= 1

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            if choice.startswith("go") or choice == "exit" or choice.startswith("enter"):
                game.move(choice)
            """
            # TODO: Make sure to include the case to subtract points for some NPC interactions. It has to be done here,
            by constructing the NPC method such that it returns a value of how much points the player gets 
            Positive for earning points, negative for losing points. 
            """
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game

        if game.remaining_moves <= 0:
            print("Out of moves!") #The player run out of moves so the game ends automatically
            game.ongoing = False

    username = input("Enter your username for the leaderboard: ").strip()
    final_score = int(game.score())
    leaderboard = Leaderboard()
    leaderboard.update(username, final_score)
    leaderboard.save()
    leaderboard.print()