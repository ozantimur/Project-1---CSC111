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
from typing import Optional

from game_entities import Location, Item, NPC
from event_logger import Event, EventList
from leaderboard import Leaderboard
from player import Player


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - current_location_id: The id of the player's current Location.
        - npcs: A list of all NPC objects in the game.
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
    npcs: list[NPC]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    auto_print: bool
    player: Player

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
        self._locations, self._items, self.npcs = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location

        self.ongoing = True  # whether the game is ongoing
        self.auto_print = False
        self.player = Player([], [], 0.0, 50, False)

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item], list[NPC]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        # this is a dictionary
        locations = {}
        items2 = []
        npcs = []

        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            locations[loc_data['id']] = Location(loc_data['name'], loc_data['id'], loc_data['brief_description'],
                                                 loc_data['long_description'], loc_data['available_commands'],
                                                 loc_data['items'], False, (loc_data['availability'] == "True"))

        for item_data in data["items"]:
            items2.append(Item(item_data['name'], item_data['start_position'], item_data['target_position'], True))

        for npc in data["npcs"]:
            speech = list(npc["speech"].values())
            options = list(npc["options"].values())
            # results: list[dict[str, float]]
            results = []

            for result_block in npc["results"].values():
                responses_scores = {response: (result_block["response"][response],
                                               float(result_block["earned_score"][response]))
                                    for response in result_block["response"]}

                results.append(responses_scores)

            npcs.append(NPC(npc["name"], npc["location"], speech, options, results))

        return locations, items2, npcs

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # YOUR CODE BELOW
        if loc_id is not None:
            return self._locations[loc_id]
        else:
            return self._locations[self.current_location_id]

    def inventory(self) -> str:
        """Return the current inventory of the player while the game is played.
        """
        items3 = [item5.name for item5 in self.player.get_current_items()]
        items_string = ""
        for item1 in items3:
            items_string += item1 + ", "
        if items_string != "":
            items_string = items_string[:-2]

        return "[" + items_string + "]"

    def move(self, desired_command: str) -> None:
        """Move the player to the new location based on the command
        Return True if the destination is valid, otherwise False
        """
        current_location = self._locations[self.current_location_id]

        if desired_command in current_location.available_commands:
            # current_location.availability marks whether the player needs an item to enter the location
            desired_destination = self._locations[current_location.available_commands[desired_command]]
            if desired_destination.availability:
                self.current_location_id = current_location.available_commands[desired_command]
                return
            else:
                # Note that id 2 is the id for the dorm room
                if current_location.available_commands[desired_command] == 2:
                    self._unlock(desired_command)
                else:
                    self._swipe(self._locations[current_location.available_commands[desired_command]])

        return

    def _unlock(self, desired_command: str) -> None:
        """
        Handle the unlocking process
        """
        # Check if the player has a key or not
        key = None
        for my_item in self.player.get_current_items():
            if my_item.name.endswith('key'):
                key = my_item
        if key:
            print(f"You have unlocked the door using your {key.name}. ", sep="", end="")
            self.current_location_id = self._locations[self.current_location_id].available_commands[desired_command]
            return
        else:
            print("Oh no! You have forgot to take your room key! "
                  "(If you left the key in your dorm, then you will not be able to to recover.)")
            return

    def _swipe(self, destination: Location) -> None:
        """
        Handle the process of scanning t-card
        """
        # Checks whether the player has the t-card on themselves
        if any([item1.name == 't card' for item1 in self.player.get_current_items()]):
            print(f"You have swiped your t-card to enter {destination.name}. ", sep="", end="")
            self.current_location_id = destination.id_num
            return
        else:
            print(f"{destination.name} requires you to swipe your t-card to enter. However, you do not have it on you.")
            return

    def pick_up(self, desired_item: str) -> bool:

        """
        Pick up the item the player wants.
        If the desired item is within the player's current location, mutate self.player.get_current_items() by appending the item,
            and return True to represent a successful interaction
        If the desired item is NOT within the player's current location, self.player.get_current_items() remains unmutated,
            and return False to represent an unsuccessful interaction

        Mutate the item's availability correspondingly
        """
        if desired_item == '':
            return False
        # print(desired_item in self._locations[self.current_location_id].items)
        # if desired_item in self._locations[self.current_location_id].items:
        for i in range(len(self._items)):
            # finding the correct item using its name
            if self._items[i].name == desired_item:
                self.player.get_current_items().append(self._items[i])
                self._items[i].available = False
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

        for i in range(len(self._items)):
            if self._items[i].name == desired_item:
                # update the availability of the item
                self._items[i].available = True
                self._items[i].start_position = self.current_location_id
                self.player.remove_item(self._items[i])
                return True
        return False

    def score(self) -> float:
        """Return the player's score so far
        """
        return self.player.get_points()

    def look(self) -> str:
        """
        Return the full description of the current location
        """
        return self._locations[self.current_location_id].long_description

    def get_items(self) -> list[Item]:
        """
        Return all items the game
        """
        return self._items

    def check_win(self) -> tuple[bool, bool]:
        """Return True if the player has won."""
        in_dorm = self.current_location_id == 2
        has_all_items = len(self.player.get_current_items()) == len(self._items)
        has_positive_points = self.player.get_points() > 0
        return in_dorm and has_all_items, has_positive_points


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 2)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "log", "quit"]  # Regular menu options available at each location
    choice = None
    print("You woke up in panic...")
    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your mark will be based on how well-organized your code is.

        location = game.get_location()

        game_log.add_event(Event(location.id_num, location.long_description), choice)

        # YOUR CODE HERE
        if not game.auto_print:
            if location.id_num in game.player.get_visited_locations():
                print(location.brief_description)
            else:
                print(location.long_description)
                game.player.visit_location(location.id_num)
        else:
            game.auto_print = False
        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        my_items = game.get_items()
        for item in my_items:
            if item.available and item.start_position == game.current_location_id and item.name != 't card':
                print("- pick up", item.name)

        for item in my_items:
            if not item.available and item.name != 't card':
                print("- drop", item.name)

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and not choice.startswith("pick up") and not choice.startswith("drop"):
            if choice.startswith("pick up") and len(location.items) == 0:
                print("That was an invalid option; try again.")
                choice = input("\nEnter action: ").lower().strip()
            elif len(choice) >= 5 and choice.startswith("drop") and not any(obj.name.endswith(choice[5::]) for obj in game.player.get_current_items()):
                print("That was an invalid option; try again.")
                choice = input("\nEnter action: ").lower().strip()
            else:
                print("That was an invalid option; try again.")
                choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            game.auto_print = True

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

            game.player.decrement_remaining_moves()

            if choice.startswith("go") or choice == "exit" or choice.startswith("enter"):
                game.move(choice)
            elif choice.startswith('talk'):
                for curr_npc in game.npcs:
                    if curr_npc.location == game.current_location_id:
                        earned_points, game.ongoing = curr_npc.dialogue()
                        game.player.add_points(earned_points)
                        if earned_points < 0:
                            print("You have lost " + str(-1 * earned_points) + " points through this interaction.")
                        else:
                            print("You have gained " + str(earned_points) + " points through this interaction.")
                        if curr_npc.name == "Arnab Kumar":
                            game.pick_up('t card')

            elif choice.startswith("pick up"):
                items = game.get_items()
                for item in items:
                    if item.start_position == game.current_location_id:
                        game.pick_up(item.name)

            elif choice.startswith("drop"):
                game.drop(choice[5::])

            elif choice.startswith("submit"):
                submit_met, positive_points = game.check_win()
                if submit_met and not positive_points:
                    game.player.set_won(False)
                    game.ongoing = False
                    print("You have successfully submitted the assignment. However, you have disappointed your professors! ")
                elif submit_met and positive_points:
                    game.player.set_won(True)
                    game.ongoing = False
                else:
                    print("You are not met the requirements to submit the assignment!")

            else:
                result = location.available_commands[choice]
                game.current_location_id = result

        if game.player.get_remaining_moves() <= 0:
            print("Out of moves!")  # The player run out of moves so the game ends automatically
            game.ongoing = False

        elif game.player.get_remaining_moves() <= 0:
            game.ongoing = False

    if game.player.get_won():
        print("You won!")
        username = input("Enter your username for the leaderboard: ").strip()
        final_score = float(game.score())
        leaderboard = Leaderboard()
        leaderboard.update(username, final_score)
        leaderboard.save()
        leaderboard.print()
    else:
        if game.player.get_remaining_moves() == 0:
            print("Game over — you ran out of moves.")
        else:
            print("Game over")

        leaderboard = Leaderboard()
        leaderboard.print()
