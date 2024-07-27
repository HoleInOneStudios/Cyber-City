import json
import random
from enum import Enum, auto
from typing import List, Tuple


class Role(Enum):
    """
    Enum class for the roles in the game. The roles are `UNKNOWN`, `OFFENSE`, and `DEFENSE`.
    """

    UNKNOWN = auto()
    OFFENSE = auto()
    DEFENSE = auto()

    def __str__(self) -> str:
        return self.name.capitalize()


class Player:
    """
    Class representing a player in the game. Each player has a role, a hand of cards, points, and a
    ready flag to indicate if they are ready to move to the next round.
    """

    MAX_HAND = 5

    def __init__(self, role: Role):
        self.role = role
        self.hand: List[Card] = []
        self.points: int = 0
        self.ready: bool = False

    def __str__(self) -> str:
        hand = ", ".join(map(str, self.hand))
        return f"Player {self.role}: {self.points} pts, Ready: {self.ready} \nHand: {hand} \n"


class Card:
    """
    Class representing a card in the game. Each card has a role, a name, a value, and odds.
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
    Class representing a district in the game. Each district has a name, an owner, and levels for
    offense and defense.
    """

    def __init__(self, name: str):
        self.name = name
        self.owner: Role = Role.UNKNOWN
        self.levels: dict = {Role.OFFENSE: 0, Role.DEFENSE: 0}

    def __str__(self) -> str:
        o_l = self.levels[Role.OFFENSE]
        d_l = self.levels[Role.DEFENSE]
        return f"{self.name} - {self.owner} (Offense: {o_l}, Defense: {d_l})"

    def add_card(self, card: Card) -> None:
        """
        Takes a card and adds its value to the corresponding level of the district. (`OFFENSE` or
        `DEFENSE`)
        """
        self.levels[card.role] += card.value

    def calculate_owner(self) -> None:
        """
        Calculates the owner of the district based on the difference between the offense and defense
        levels. If the difference is 0, the owner is `UNKNOWN`.

        If the owner changes, the levels are updated accordingly by subtracting the lower level from
        the higher level.
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
    The main class representing the game. It contains the players, cards, districts, and the current
    round.
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
        Returns a new card based on the given role. The card is randomly selected from the list of
        cards that match the role, with the odds of each card being used as the weights for the
        random choice.
        """
        eligible = [card for card in self.cards if card.role == role]
        return random.choices(eligible, weights=[card.odds for card in eligible])[0]

    def fill_hands(self) -> None:
        """
        Fills the hands of each player with cards until they have `Player.MAX_HAND` cards.
        """
        for player in self.players.values():
            while len(player.hand) < Player.MAX_HAND:
                player.hand.append(self.new_card(player.role))

    def update_districts(self) -> None:
        """
        For each district, it runs the `calculate_owner` method to determine the owner of the
        district based on the levels of offense and defense.
        """
        for district in self.districts:
            district.calculate_owner()

    def update_points(self) -> None:
        """
        For each district, it checks which player is the owner and gives them 1 point. If the owner
        is `UNKNOWN`, no points are awarded.
        """
        for district in self.districts:
            if district.owner in self.players:
                self.players[district.owner].points += 1

    def play_round(self) -> None:
        """
        This method is called during each round of the game and is responsible for holding the
        interactive parts of the game, by allowing the players to play their cards.

        ! WARNING: This method is not implemented and should be implemented in the subclass.
        """

    def play_card(self, player: Player, card: Card, district: District) -> None:
        """
        This method allows a player to play a card from their hand to a district. It does handle
        checking if the player has the card in their hand and if the district is valid. If the card
        is played successfully, it is removed from the player's hand and added to the district.
        """
        if player.hand.count(card) > 0 and self.districts.count(district) > 0:
            player.hand.remove(card)
            district.add_card(card)
        else:
            raise ValueError("Invalid card or district")

    def start_game(self) -> None | Role:
        """
        This is the main game loop that runs until the maximum number of rounds is reached. It
        fills the hands of the players, plays the rounds, updates the districts, and calculates the
        points.

        At the end it calls the `determine_winner` method to determine the winner of the game and
        returns it.
        """
        while self.current_round <= Game.MAX_ROUNDS:
            self.players[Role.OFFENSE].ready = False
            self.players[Role.DEFENSE].ready = False
            self.fill_hands()

            self.play_round()

            self.update_districts()
            self.update_points()
            self.current_round += 1

        return self.determine_winner()

    def reset_game(self) -> None:
        """
        Resets the game by setting the points of each player to 0, clearing their hands, and setting
        the `ready` flag to `False`. It also resets the owner and levels of each district. Finally,
        it sets the current round back to 1.
        """
        for player in self.players.values():
            player.points = 0
            player.hand = []
            player.ready = False

        for district in self.districts:
            district.owner = Role.UNKNOWN
            district.levels = {Role.OFFENSE: 0, Role.DEFENSE: 0}

        self.current_round = 1

    def determine_winner(self) -> Role:
        """
        Returns the winner of the game based on the points of the offense and defense players. If
        the points are equal, it returns `UNKNOWN`.
        """
        if self.players[Role.OFFENSE].points > self.players[Role.DEFENSE].points:
            return Role.OFFENSE
        elif self.players[Role.OFFENSE].points < self.players[Role.DEFENSE].points:
            return Role.DEFENSE
        else:
            return Role.UNKNOWN


def load_game_data(filepath: str) -> Tuple[List[Card], List[District]]:
    """
    Loads the game data from a JSON file and returns a tuple containing the list of cards and
    districts. If the file is not found or the JSON is invalid, it returns `None` for both lists.
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
