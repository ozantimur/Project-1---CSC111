"""

Helper file which contains relevant information of the player

"""


from __future__ import annotations
from dataclasses import dataclass
from game_entities import Item


@dataclass
class Player:
    """A player in the text adventure game.

    Instance Attributes:
        - _current_items: The list of items currently held by the player.
        - _visited_locations: The list of location ids the player has visited.
        - _points: The player's current point total.
        - _remaining_moves: The number of moves the player has remaining.

    Representation Invariants:

        - all(isinstance(item, Item) for item in _current_items)
        - all(isinstance(loc, int) and loc >= 0 for loc in _visited_locations)
        - _remaining_moves >= 0
        - _points >= 0
        - _min_points_to_win > 3.0
    """

    _current_items: list[Item]
    _visited_locations: list[int]
    _points: float
    _remaining_moves: int
    _won: bool
    _min_points_to_win: float = 3.0
    _dorm_location_id: int = 2

    # Getters
    def get_current_items(self) -> list[Item]:
        """
        Return current items the player carries
        """
        return self._current_items

    def get_visited_locations(self) -> list[int]:
        """
        Return all visited locations
        """
        return self._visited_locations

    def get_points(self) -> float:
        """
        Return the number of points the player has
        """
        return float(self._points)

    def get_remaining_moves(self) -> int:
        """
        Return the remaining moves the player has
        """
        return self._remaining_moves

    def get_won(self) -> bool:
        """
        Return whether the player has won
        """
        return self._won

    def get_min_points_to_win(self) -> float:
        """
        Return the minimum points for the player to obtain in order to pass the game
        """
        return self._min_points_to_win

    def get_dorm_location_id(self) -> int:
        """
        Return the id of dorm
        """
        return self._dorm_location_id

    # Setters
    def set_current_items(self, items: list[Item]) -> None:
        """
        Mutate the list of items which represents the player's inventory
        """
        self._current_items = items

    def visit_location(self, location_id: int) -> None:
        """
        Mutating the location list based on the player's visited locations
        """
        if location_id not in self._visited_locations:
            self._visited_locations.append(location_id)

    def add_points(self, points: float) -> None:
        """
        Mutate the points variable
        """
        self._points += float(points)

    def decrement_remaining_moves(self) -> None:
        """
        Mutate the remaining number of moves the player has by 1
        """
        self._remaining_moves -= 1

    def set_won(self, won: bool) -> None:
        """
        Mutate the _won variable
        """
        self._won = won

    def remove_item(self, item: Item) -> None:
        """
        Remove the item from the player's inventory
        """
        if item in self._current_items:
            self._current_items.remove(item)
