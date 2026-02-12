import json

class Leaderboard:
    """

    Instance Attributes:
        - filename: the JSON file storing the leaderboard
        - entries: list of [username, score] pairs sorted in descending score order


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
