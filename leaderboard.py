import json

class Leaderboard:
    """
    A leaderboard that keeps the top 5 player scores and saves them in a JSON file.

    Instance Attributes:
        - filename: the JSON file storing the leaderboard
        - leaderboard: list of [username, score] pairs sorted in descending score order

    Representation Invariants:
        - len(self.leaderboard) <= 5
        - all(len(entry) == 2 for entry in self.leaderboard)
        - all(isinstance(entry[0], str) for entry in self.leaderboard)
        - all(isinstance(entry[1], float) for entry in self.leaderboard)
        - self.leaderboard is sorted in descending order by score
    """
    filename: str
    leaderboard: list[list]

    def __init__(self, filename: str = "leaderboard.json") -> None:
        """Initialize this leaderboard by loading from filename."""
        self.filename = filename
        self.leaderboard = self._load()

    def _load(self) -> list[list]:
        """Return the leaderboard list from filename."""
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            return data.get("leaderboard", [])
        except FileNotFoundError:
            return []

    def save(self) -> None:
        """Save the leaderboard list to filename."""
        with open(self.filename, "w") as f:
            json.dump({"leaderboard": self.leaderboard}, f)

    def update(self, username: str, score: float) -> None:
        """Return a new leaderboard updated with (username, score).
        """
        inserted = False

        skip_updating = False
        for i in range(len(self.leaderboard)):
            if username == self.leaderboard[i][0]:
                if score > self.leaderboard[i][1]:
                    self.leaderboard.pop(i)
                else:
                    skip_updating = True
                break

        if not skip_updating:
            for i in range(len(self.leaderboard)):
                if score > self.leaderboard[i][1]:
                    self.leaderboard.insert(i, [username, score])
                    inserted = True
                    break

            if not inserted and len(self.leaderboard) < 5:
                self.leaderboard.append([username, score])

        if len(self.leaderboard) > 5:
            self.leaderboard.pop()

    def print(self) -> None:
        """Print the leaderboard in ranked order."""
        print("\n*** LEADERBOARD ***")
        for i in range(len(self.leaderboard)):
            print(f"{i + 1}. {self.leaderboard[i][0]} - {self.leaderboard[i][1]}")
