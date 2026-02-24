"""CSC111 Project 1: Text Adventure Game - Simulator

Instructions (READ THIS FIRST!)
===============================

This Python module contains code for Project 1 that allows a user to simulate
an entire playthrough of the game. Please consult the project handout for
instructions and details.

You can copy/paste your code from Assignment 1 into this file, and modify it as
needed to work with your game.

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
from event_logger import Event, EventList
from adventure import AdventureGame
from game_entities import Location


class AdventureGameSimulation:
    """A simulation of an adventure game playthrough.
    """
    # Private Instance Attributes:
    #   - _game: The AdventureGame instance that this simulation uses.
    #   - _events: A collection of the events to process during the simulation.
    _game: AdventureGame
    _events: EventList

    def __init__(self, game_data_file: str, initial_location_id: int, commands: list[str]) -> None:
        """
        Initialize a new game simulation based on the given game data, that runs through the given commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from the location at initial_location_id
        """
        self._events = EventList()
        self._game = AdventureGame(game_data_file, initial_location_id)

        first_location = self._game.get_location()
        first_event = Event(first_location.id_num, first_location.long_description)
        self._events.add_event(first_event, None)

        self.generate_events(commands, first_location)

    def generate_events(self, commands: list[str], current_location: Location) -> None:
        """
        Generate events in this simulation, based on current_location and commands, a valid list of commands.

        Preconditions:
        - len(commands) > 0
        - all commands in the given list are valid commands when starting from current_location
        """
        for c in commands:
            if (not (c.startswith("pick") or c.startswith("drop")
                     or c in ["inventory", "look", "score", "talk", "submit assignment"])
                    and not "0" <= c <= "9" and not c == commands[-1] or c.startswith("exit") or c.startswith("enter")):
                new_location = self._game.get_location(current_location.available_commands[c])
                new_event = Event(new_location.id_num, new_location.long_description)
                self._events.add_event(new_event, c)
                current_location = new_location
            elif (c not in ["inventory", "look", "submit assignment", "talk"]
                  and not "0" <= c <= "9" and c != commands[-1]):
                new_event = Event(current_location.id_num, current_location.long_description)
                self._events.add_event(new_event, c)

    def get_id_log(self) -> list[int]:
        """
        Get back a list of all location IDs in the order that they are visited within a game simulation
        that follows the given commands.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        return self._events.get_id_log()

    def run(self) -> None:
        """
        Run the game simulation and log location descriptions.
        """
        # Note: We have completed this method for you. Do NOT modify it for A1.

        current_event = self._events.first  # Start from the first event in the list

        while current_event:
            print(current_event.description)
            if current_event is not self._events.last:
                print("You choose:", current_event.next_command)

            # Move to the next event in the linked list
            current_event = current_event.next


if __name__ == "__main__":
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker']
    })

    win_walkthrough = ['pick up dorm key', 'exit dorm', 'go west', 'exit building', 'go north', 'talk arnab kumar',
                       '0', 'enter robarts library', 'pick up usb drive', 'exit building', 'go south', 'go south',
                       'talk boris khesin', '3', '3', 'score', 'go south', 'enter bahen centre',
                       'go west', 'talk paul he', '1', '1',
                       'score', 'go south', 'pick up lucky uoft mug', 'go north', 'go east',
                       'exit building', 'enter myhal centre', 'pick up laptop charger', 'exit building',
                       'go north', 'go north', 'enter morrison hall', 'go east', 'enter dorm',
                       'drop usb drive', 'score', 'drop laptop charger', 'score',
                       'drop lucky uoft mug', 'score', 'submit assignment', 'fake_username']

    expected_log = [2, 2, 3, 4, 5, 7, 7, 0, 0, 7, 5, 10, 10, 10, 6, 1, 9, 9, 9, 12, 12, 9, 1, 6, 8, 8, 6, 10, 5, 4,
                    3, 2, 2, 2, 2, 2, 2, 2]

    sim = AdventureGameSimulation('game_data.json', 2, win_walkthrough)
    assert expected_log == sim.get_id_log()

    # Create a list of all the commands needed to walk through your game to reach a 'game over' state
    lose_demo = ["pick up dorm key"] + ["exit dorm", "enter dorm"] * 19 + ["exit dorm"]
    expected_log = [2, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3,
                    2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3]
    # Uncomment the line below to test your demo
    sim = AdventureGameSimulation('game_data.json', 2, lose_demo)
    assert expected_log == sim.get_id_log()

    # TODO: Add code below to provide walkthroughs that show off certain features of the game
    # TODO: Create a list of commands involving visiting locations, picking up items, and then
    #   checking the inventory, your list must include the "inventory" command at least once
    # inventory_demo = [..., "inventory", ...]
    # expected_log = []
    # sim = AdventureGameSimulation(...)
    # assert expected_log == sim.get_id_log()

    inventory_demo = [
        'pick up dorm key',
        'exit dorm',
        'enter dorm',
        'inventory',
        'exit dorm',
        'go west',
        'exit building',
        'go south',
        'go south',
        'enter myhal centre',
        'pick up laptop charger',
        'inventory',
        'exit building',
        'go north',
        'go north',
        'go north',
        'talk arnab kumar',
        '0',
        'enter robarts library',
        'pick up usb drive',
        'inventory'
    ]
    expected_log = [2, 2, 3, 2, 3, 4, 5, 10, 6, 8, 8, 6, 10, 5, 7, 7, 0, 0]
    sim = AdventureGameSimulation('game_data.json', 2, inventory_demo)
    assert expected_log == sim.get_id_log()

    scores_demo = [
        'pick up dorm key',
        'exit dorm',
        'go west',
        'exit building',
        'go north',
        'talk arnab kumar',
        '0',
        'enter robarts library',
        'pick up usb drive',
        'score',
        'exit building',
        'go south',
        'go south',
        'go south',
        'enter bahen centre',
        'go west',
        'go south',
        'pick up lucky uoft mug',
        'score',
        'go north',
        'go east',
        'exit building',
        'enter myhal centre',
        'pick up laptop charger',
        'score',
        'exit building',
        'go north',
        'go north',
        'go north',
        'go south',
        'enter morrison hall',
        'go east',
        'enter dorm',
        'drop usb drive',
        'score',
        'drop laptop charger',
        'score',
        'drop lucky uoft mug',
        'score',
        'inventory'
    ]
    expected_log = [2, 2, 3, 4, 5, 7, 7, 0, 0, 0, 7, 5, 10, 6, 1, 9, 12, 12, 12, 9, 1, 6, 8, 8, 8,
                    6, 10, 5, 7, 5, 4, 3, 2, 2, 2, 2, 2, 2, 2, 2]
    sim = AdventureGameSimulation('game_data.json', 2, scores_demo)
    assert expected_log == sim.get_id_log()

    # Enhancement demo: shows NPC dialogue + scoring + T-card interaction
    enhancement1_demo = [
        'pick up dorm key',
        'exit dorm',
        'go west',
        'exit building',
        'go north',
        'talk arnab kumar',
        '0',
        'score',
        'go south',
        'go south',
        'talk boris khesin',
        '3',
        '3',
        'score',
        'go south',
        'enter bahen centre',
        'go west',
        'talk paul he',
        '2',
        '1',
        'score',
        'inventory'
    ]
    expected_log = [2, 2, 3, 4, 5, 7, 7, 7, 5, 10, 10, 10, 6, 1, 9, 9, 9]
    sim = AdventureGameSimulation('game_data.json', 2, enhancement1_demo)
    assert expected_log == sim.get_id_log()

    # scores_demo = [..., "score", ...]
    # expected_log = []
    # sim = AdventureGameSimulation(...)
    # assert expected_log == sim.get_id_log()

    # Add more enhancement_demos if you have more enhancements
    # enhancement1_demo = [...]
    # expected_log = []
    # sim = AdventureGameSimulation(...)
    # assert expected_log == sim.get_id_log()

    # Note: You can add more code below for your own testing purposes
