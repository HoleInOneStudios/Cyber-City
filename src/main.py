import json
import random
from enum import Enum, auto
from typing import List, Tuple


class Role(Enum):
    UNKNOWN = auto()
    OFFENSE = auto()
    DEFENSE = auto()

    def __str__(self) -> str:
        return self.name.capitalize()


class Player:
    MAX_HAND = 5

    def __init__(self, role: Role):
        self.role = role
        self.hand: List[Card] = []
        self.points: int = 0
        self.ready: bool = False

    def __str__(self) -> str:
        return f"Player: {self.role} (Points: {self.points}, Ready: {self.ready}) \nHand: {', '.join(map(str, self.hand))}\n"


class Card:
    def __init__(self, role: Role, name: str, value: int, odds: float):
        self.role = role
        self.name = name
        self.value = value
        self.odds = odds

    def __str__(self) -> str:
        return f"{self.name} (Role: {self.role} Value: {self.value} Odds: {self.odds})"


class District:
    def __init__(self, name: str):
        self.name = name
        self.owner: Role = Role.UNKNOWN
        self.levels: dict = {Role.OFFENSE: 0, Role.DEFENSE: 0}

    def __str__(self) -> str:
        return f"{self.name} (Owner: {self.owner}, Offense: {self.levels[Role.OFFENSE]}, Defense: {self.levels[Role.DEFENSE]})"

    def add_card(self, card: Card) -> None:
        self.levels[card.role] += card.value

    def calculate_owner(self) -> None:
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
        eligible = [card for card in self.cards if card.role == role]
        return random.choices(eligible, weights=[card.odds for card in eligible])[0]

    def fill_hands(self) -> None:
        for player in self.players.values():
            while len(player.hand) < Player.MAX_HAND:
                player.hand.append(self.new_card(player.role))

    def update_districts(self) -> None:
        for district in self.districts:
            district.calculate_owner()

    def update_points(self) -> None:
        for district in self.districts:
            if district.owner in self.players:
                self.players[district.owner].points += 1

    def play_round(self) -> None:
        pass  # TODO: Placeholder for actual game logic

    def start_game(self) -> Role:
        while self.current_round <= Game.MAX_ROUNDS:
            self.players[Role.OFFENSE].ready = False
            self.players[Role.DEFENSE].ready = False

            self.play_round()
            self.update_districts()
            self.update_points()
            self.current_round += 1

        return self.determine_winner()

    def determine_winner(self) -> Role:
        if self.players[Role.OFFENSE].points > self.players[Role.DEFENSE].points:
            return Role.OFFENSE
        elif self.players[Role.OFFENSE].points < self.players[Role.DEFENSE].points:
            return Role.DEFENSE
        else:
            return Role.UNKNOWN


def load_game_data(filepath: str) -> Tuple[List[Card], List[District]]:
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
