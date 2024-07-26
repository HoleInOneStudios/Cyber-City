"""
This is a simple card game where two players, offense and defense, compete to control districts
by playing cards with offense and defense values. The game consists of multiple rounds, and the
player with the most points at the end of the game wins.
"""

import random
import json


class ROLE:
    """
    This is an enumeration class that defines the roles of the players, cards, and anything else
    that needs to be categorized as either offense or defense.

    Attributes:
        OFFENSE (int): The value of the offense role.
        DEFENSE (int): The value of the defense role
    """

    OFFENSE = 0
    DEFENSE = 1

    @staticmethod
    def to_string(role: int) -> str:
        """
        Convert a role value to a string representation.

        Args:
            role (int): The role value to be converted.

        Returns:
            str: The string representation of the role.
        """
        if role == ROLE.OFFENSE:
            return "Offense"
        elif role == ROLE.DEFENSE:
            return "Defense"
        else:
            return "Unknown"


class Player:
    """
    This class represents a player in the game. Each player has a role, hand, points, and a ready
    status.

    It also has a MAX_HAND attribute that defines the maximum number of cards a player can hold in
    their hand.
    """

    MAX_HAND = 5

    def __init__(self, role):
        self.role = role
        self.hand = []
        self.points = 0
        self.ready = False

    def __str__(self):
        return (
            f"Player: {ROLE.to_string(self.role)} (Points: {self.points}, Ready: {self.ready}) \n"
            f"Hand: {', '.join([str(card) for card in self.hand])} \n"
        )


class Card:
    """
    This class represents a card in the game. Each card has a role, name, value, and odds.
    """

    def __init__(self, role, name, value, odds):
        self.role = role
        self.name = name
        self.value = value
        self.odds = odds

    def __str__(self):
        return f"{self.name} (R: {ROLE.to_string(self.role)} V: {self.value} O: {self.odds})"


class District:
    """
    This class represents a district in the game. Each district has a name, owner, offense level,
    and defense level.
    """

    def __init__(self, name):
        self.name = name
        self.owner = None
        self.o_lvl = 0
        self.d_lvl = 0

    def __str__(self):
        return f"{self.name} ({ROLE.to_string(self.owner)}, O: {self.o_lvl} D: {self.d_lvl})"

    def add_card(self, new_card: Card):
        """
        Add a card to the district and update the offense and defense levels.

        Args:
            new_card (Card): The card to be added to the district.
        """
        if new_card.role == ROLE.OFFENSE:
            self.o_lvl += new_card.value
        elif new_card.role == ROLE.DEFENSE:
            self.d_lvl += new_card.value

    def calculate_owner(self):
        """
        Calculate the owner of the district based on the offense and defense levels.
        """

        # Store the offense and defense levels in temporary variables
        _o_lvl = self.o_lvl
        _d_lvl = self.d_lvl
        _new_owner = None

        # Determine the new owner based on the offense and defense levels
        if _o_lvl > _d_lvl:
            _new_owner = ROLE.OFFENSE
        elif _d_lvl > _o_lvl:
            _new_owner = ROLE.DEFENSE
        else:
            _new_owner = None

        # Update the owner and offense/defense levels if the owner has changed
        if _new_owner != self.owner:
            self.owner = _new_owner
            self.o_lvl = self.o_lvl - _d_lvl
            self.d_lvl = self.d_lvl - _o_lvl

            self.o_lvl = max(0, self.o_lvl)
            self.d_lvl = max(0, self.d_lvl)


class Game:
    """
    This class represents the game itself. It contains the offense and defense players, the
    districts, and the cards in the game.

    It also has a MAX_ROUNDS attribute that defines the maximum number of rounds in the game.
    """

    MAX_ROUNDS = 10

    def __init__(self):
        self.offense = Player(ROLE.OFFENSE)
        self.defense = Player(ROLE.DEFENSE)
        self.districts = []
        self.cards = []

        self.current_round = 1

    def new_card(self, role: int) -> Card:
        """
        Gets a randomly weighted card of a specific role from the game's card pool.

        Args:
            role (int): The role of the card to be selected. Can be either ROLE.OFFENSE or
                        ROLE.DEFENSE.

        Returns:
            Card: A randomly selected card of the specified role.
        """
        # Filter the cards based on the role
        _cards = [card for card in self.cards if card.role == role]
        # Get the odds of each card
        _odds = [card.odds for card in _cards]
        # Select a card randomly based on the odds using the random.choices method from the random
        # module
        _card = random.choices(_cards, _odds)[0]
        return _card

    def fill_hands(self):
        """
        Fill the hands of the offense and defense players with cards up to the maximum hand size.
        """
        while len(self.offense.hand) < Player.MAX_HAND:
            self.offense.hand.append(self.new_card(ROLE.OFFENSE))
        while len(self.defense.hand) < Player.MAX_HAND:
            self.defense.hand.append(self.new_card(ROLE.DEFENSE))

    def calculate_districts(self):
        """
        Run the calculate_owner method for each district to determine the owner of each district.
        """
        for district in self.districts:
            district.calculate_owner()

    def increase_points(self):
        """
        Increase the points of the offense and defense players based on the districts they own.
        """
        for district in self.districts:
            if district.owner == ROLE.OFFENSE:
                self.offense.points += 1
            elif district.owner == ROLE.DEFENSE:
                self.defense.points += 1

    def play_card(self, player_role: int, card_index: int, district_index: int) -> None:
        """
        Play a card from the player's hand to a district.

        Warning:
            This method currently does not handle invalid inputs. It is up to the caller to ensure
            that the inputs are valid

        Args:
            player_role (int): The role of the player. Can be either ROLE.OFFENSE or ROLE.DEFENSE.
            card_index (int): The index of the card in the player's hand.
            district_index (int): The index of the district where the card will be played.
        """
        # Get the player and card based on the role
        _player = self.offense if player_role == ROLE.OFFENSE else self.defense
        _card = _player.hand.pop(card_index)
        # Add the card to the district
        self.districts[district_index].add_card(_card)

    def player_turn(self, player):
        """
        TODO: Implement the player's turn logic. This method should handle the player's actions
        """
        while not player.ready:
            _card_index = None  # TODO: Get the card index from the player
            _district_index = None  # TODO: Get the district index from the player

            if not player.hand or _card_index is None or _district_index is None:
                player.ready = True
            else:
                self.play_card(player.role, _card_index, _district_index)


# Load the data from the JSON file and create the cards and districts
data = json.load(open("data.json", "r", encoding="utf-8"))
cards = []
for card in data["Cards_good"]:
    cards.append(Card(ROLE.DEFENSE, card["name"], card["value"], card["odds"]))
for card in data["Cards_bad"]:
    cards.append(Card(ROLE.OFFENSE, card["name"], card["value"], card["odds"]))
districts = [District(district) for district in data["Districts"]]

# Create a new game and set the cards and districts
game = Game()
game.cards = cards
game.districts = districts
game.fill_hands()

print(game.offense)
print(game.defense)

print(game.districts[0])
print(game.districts[1])
