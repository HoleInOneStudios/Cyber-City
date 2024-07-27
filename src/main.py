import json
import random
from enum import Enum, auto
from typing import List, Tuple


class Role(Enum):
    """
    Enum representing possible roles in the game for players, cards, or districts.

    Attributes:
        UNKNOWN (Enum): Represents an undefined role.
        OFFENSE (Enum): Represents an offensive role.
        DEFENSE (Enum): Represents a defensive role.
    """

    UNKNOWN = auto()
    OFFENSE = auto()
    DEFENSE = auto()

    def __str__(self) -> str:
        return self.name.capitalize()


class Player:
    """
    Represents a player in the game, managing their role, hand of cards, score points, and
    readiness status.

    Attributes:
        `role` (Role): Role of the player, either offensive or defensive.
        `hand` (List[Card]): List of cards in the player's hand.
        `points` (int): Points scored by the player.
        `ready` (bool): Indicates whether the player is ready to play a card

    Constants:
        MAX_HAND (int): Maximum number of cards a player can hold.
    """

    MAX_HAND = 5

    def __init__(self, role: Role):
        self.role = role
        self.hand: List[Card] = []
        self.points: int = 0
        self.ready: bool = False

    def __str__(self) -> str:
        return f"Player: {self.role} (Points: {self.points}, Ready: {self.ready}) \nHand: {', '.join(map(str, self.hand))}\n"


class Card:
    """
    Represents a card in the game, characterized by its role, name, value, and the odds of drawing
    it.

    Attributes:
        `role` (Role): Role of the card, either offensive or defensive.
        `name` (str): Name of the card.
        `value` (int): Value of the card.
        `odds` (float): Odds of drawing the card.
    """

    def __init__(self, role: Role, name: str, value: int, odds: float):
        self.role = role
        self.name = name
        self.value = value
        self.odds = odds

    def __str__(self) -> str:
        return f"{self.name} (Role: {self.role} Value: {self.value} Odds: {self.odds})"


class District:
    """
    Represents a district in the game, which can be owned by players based on offensive and
    defensive card plays.

    Attributes:
        `name` (str): Name of the district.
        `owner` (Role): Current owner of the district, defaults to Role.UNKNOWN.
        `levels` (dict): Tracks the cumulative levels of offense and defense in the district.
    """

    def __init__(self, name: str):
        self.name = name
        self.owner: Role = Role.UNKNOWN
        self.levels: dict = {Role.OFFENSE: 0, Role.DEFENSE: 0}

    def __str__(self) -> str:
        return f"{self.name} (Owner: {self.owner}, Offense: {self.levels[Role.OFFENSE]}, Defense: {self.levels[Role.DEFENSE]})"

    def add_card(self, card: Card) -> None:
        """
        Adds the value of the card to the corresponding level in the district. The card's role
        determines whether the value is added to offense or defense.

        Args:
            card (Card): The card to be added to the district.
        """
        self.levels[card.role] += card.value

    def calculate_owner(self) -> None:
        """
        Determines the owner of the district based on the levels of offense and defense. If the
        levels are equal, the district remains or becomes unowned.
        """
        o, d = self.levels[Role.OFFENSE], self.levels[Role.DEFENSE]
        new_owner = (
            Role.UNKNOWN if o == d else (Role.OFFENSE if o > d else Role.DEFENSE)
        )

        if new_owner != self.owner:
            self.owner = new_owner

            self.levels[Role.OFFENSE], self.levels[Role.DEFENSE] = max(0, o - d), max(
                0, d - o
            )


class Game:
    """
    This class represents the game itself. It contains the players, cards, districts, and the
    current round. The game logic is implemented in the `play_round` method, which should be
    overriden by a subclass.

    Attributes:
        `players` (dict): Dictionary containing the offensive and defensive players.
        `districts` (List[District]): List of districts in the game.
        `cards` (List[Card]): List of cards in the game.
        `current_round` (int): Current round number.

    Constants:
        MAX_ROUNDS (int): Maximum number of rounds in the game.
    """

    MAX_ROUNDS = 10

    def __init__(self, cards: List[Card], districts: List[District]):
        if cards is None or districts is None:
            raise ValueError("Invalid game data")
        self.players: dict = {
            Role.OFFENSE: Player(Role.OFFENSE),
            Role.DEFENSE: Player(Role.DEFENSE),
        }
        self.districts = districts
        self.cards = cards
        self.current_round: int = 1

    def new_card(self, role: Role) -> Card:
        """
        Randomly selects a card based on the role and the odds of drawing it. The odds are used as
        weights for the random selection.

        Args:
            role (Role): Role of the card to be drawn.

        Returns:
            Card: The randomly selected card.
        """
        eligible = [card for card in self.cards if card.role == role]
        return random.choices(eligible, weights=[card.odds for card in eligible])[0]

    def fill_hands(self) -> None:
        """
        For each player, fill their hand with cards until it reaches the maximum hand size.
        """
        for player in self.players.values():
            while len(player.hand) < Player.MAX_HAND:
                player.hand.append(self.new_card(player.role))

    def update_districts(self) -> None:
        """
        For each district, run the `calculate_owner` method to determine the owner based on the
        levels of offense and defense in the district.
        """
        for district in self.districts:
            district.calculate_owner()

    def update_points(self) -> None:
        """
        Check the owner of each district and award points to the corresponding player. If the
        district is unowned, no points are awarded.
        """
        for district in self.districts:
            if district.owner in self.players:
                self.players[district.owner].points += 1

    def play_round(self) -> None:
        """
        TODO: Placeholder method that should be overriden by a subclass to implement game logic.

        This method should handle the players' card plays, set the readiness status, and update the
        districts' levels based on the played cards when both players are ready.

        The current implementation does nothing.
        """

    def start_game(self) -> None | Role:
        """
        Starts the game and plays rounds until the maximum number of rounds is reached. The winner
        is then determined based on the points scored by the players and printed to the console.

        It may be beneficial to override this method in a subclass to implement custom game logic,
        such as handling player input or displaying game state to the user.

        Returns:
            None | Role: In this implementation, the role of the winning player is printed, but it
            could be returned instead.
        """
        while self.current_round <= Game.MAX_ROUNDS:
            self.players[Role.OFFENSE].ready = False
            self.players[Role.DEFENSE].ready = False

            self.play_round()
            self.update_districts()
            self.update_points()
            self.current_round += 1

        winner = self.determine_winner()
        print(f"Game over! Winner: {winner}")

    def determine_winner(self) -> Role:
        """
        Determines the game winner based on points. If the points are equal, the winner is
        undetermined.

        Returns:
            Role: The role of the winning player or Role.UNKNOWN if the game is a tie.
        """
        if self.players[Role.OFFENSE].points > self.players[Role.DEFENSE].points:
            return Role.OFFENSE
        elif self.players[Role.OFFENSE].points < self.players[Role.DEFENSE].points:
            return Role.DEFENSE
        else:
            return Role.UNKNOWN


def load_game_data(filepath: str) -> Tuple[List[Card], List[District]]:
    """
    Loads game data from a specified JSON file containing card and district details.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        Tuple containing a list of Card objects and a list of District objects, or None for each if
        loading fails.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        cards = [
            Card(
                Role[card["role"].upper()],
                card["name"],
                card["value"],
                card["odds"],
            )
            for card in data["Cards"]
        ]
        districts = [District(name) for name in data["Districts"]]
        return cards, districts
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None, None
    except json.JSONDecodeError:
        print(f"Invalid JSON file: {filepath}")
        return None, None


game = Game(*load_game_data("data.json"))
game.fill_hands()

print(game.players[Role.OFFENSE])
print(game.players[Role.DEFENSE])
print("\n".join(map(str, game.districts)))
