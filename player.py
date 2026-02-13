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
    """

    _current_items: list[Item]
    _visited_locations: list[int]
    _points: float
    _remaining_moves: int
    _won: bool

    # Getters
    def get_current_items(self) -> list[Item]:
        return self._current_items

    def get_visited_locations(self) -> list[int]:
        return self._visited_locations

    def get_points(self) -> float:
        return float(self._points)

    def get_remaining_moves(self) -> int:
        return self._remaining_moves

    def get_won(self) -> bool:
        return self._won

    # Setters
    def set_current_items(self, items: list[Item]) -> None:
        self._current_items = items

    def visit_location(self, location_id: int) -> None:
        if location_id not in self._visited_locations:
            self._visited_locations.append(location_id)

    def add_points(self, points: float) -> None:
        self._points += float(points)

    def decrement_remaining_moves(self) -> None:
        self._remaining_moves -= 1

    def set_won(self, won: bool) -> None:
        self._won = won