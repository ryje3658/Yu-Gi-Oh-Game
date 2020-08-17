import random
from termcolor import colored


class Card:
    """A Card object."""

    def __init__(self, name, ten_char_name, effect):
        self.name = name
        self.ten_char_name = ten_char_name
        self.position = None
        self.location = "Deck"
        self.effect = effect

    def __repr__(self):
        return self.name


class Monster(Card):
    """Monster Card object."""

    def __init__(self, name, ten_char_name, effect, attack, defence, level, monster_type, attribute):
        super().__init__(name, ten_char_name, effect)
        self.attack = attack
        self.defence = defence
        self.level = level
        self.monster_type = monster_type
        self.attribute = attribute
        self.effect = effect

    def __repr__(self):
        if self.position == "FD":
            return colored("Face Down Monster", "blue")
        elif self.position is not None:
            return colored(f"{self.name}/{self.position}", "blue")
        else:
            return colored(self.name, "blue")


class Trap(Card):
    """Trap Card object."""

    def __init__(self, name, ten_char_name, effect, trap_type):
        super().__init__(name, ten_char_name, effect)
        self.trap_type = trap_type

    def __repr__(self):
        return colored(self.name, "red")


class Magic(Card):
    """Magic Card object."""

    def __init__(self, name, ten_char_name, effect):
        super().__init__(name, ten_char_name, effect)

    def __repr__(self):
        return colored(self.name, "green")


class Equip(Magic):
    """Equip Magic Card object."""

    def __init__(self, name, ten_char_name, effect):
        super().__init__(name, ten_char_name, effect)
        self.target_monster = None

    def __repr__(self):
        return colored(self.name, "green")


class Field(Magic):
    """Field Magic Card object."""

    def __init__(self, name, ten_char_name, effect):
        super().__init__(name, ten_char_name, effect)

    def __repr__(self):
        return colored(self.name, "green")


class Deck:
    """Player's deck of cards, consisting of Card objects, with methods to pop and shuffle."""

    def __init__(self, card_list: list):
        self.card_list = card_list

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.card_list)

    def pop(self):
        """Remove top card from the deck and return it."""
        card = self.card_list.pop()
        return card

    def get_length(self):
        """Returns the number of cards left in the player's deck."""
        return len(self.card_list)

    def is_empty(self):
        """Check if the deck has no cards left."""
        if len(self.card_list) == 0:
            return True
        return False


class Board:
    """Game board containing spaces for each players 5 monster spots, 5 magic/trap spots, a field zone, and two
    graveyard spaces to match the aesthetic of the physical board.
    """

    def __init__(self):
        """Set all game spaces to the empty placeholder, to be changed by user according to their preferences, and the
        graveyard spots and field zone spot to text descriptors.
        """
        self.empty_placeholder = "-----------"
        self.field_zone = self.empty_placeholder
        self.p1_monster_1 = self.empty_placeholder
        self.p1_monster_2 = self.empty_placeholder
        self.p1_monster_3 = self.empty_placeholder
        self.p1_monster_4 = self.empty_placeholder
        self.p1_monster_5 = self.empty_placeholder
        self.p1_magic_1 = self.empty_placeholder
        self.p1_magic_2 = self.empty_placeholder
        self.p1_magic_3 = self.empty_placeholder
        self.p1_magic_4 = self.empty_placeholder
        self.p1_magic_5 = self.empty_placeholder
        self.p1_graveyard_display = "Graveyard"
        self.p2_monster_1 = self.empty_placeholder
        self.p2_monster_2 = self.empty_placeholder
        self.p2_monster_3 = self.empty_placeholder
        self.p2_monster_4 = self.empty_placeholder
        self.p2_monster_5 = self.empty_placeholder
        self.p2_magic_1 = self.empty_placeholder
        self.p2_magic_2 = self.empty_placeholder
        self.p2_magic_3 = self.empty_placeholder
        self.p2_magic_4 = self.empty_placeholder
        self.p2_magic_5 = self.empty_placeholder
        self.p2_graveyard_display = "Graveyard"
        self.p1_slots = [self.p1_monster_1, self.p1_monster_2, self.p1_monster_3, self.p1_monster_4, self.p1_monster_5,
                         self.p1_magic_1, self.p1_magic_2, self.p1_magic_3, self.p1_magic_4, self.p1_magic_5]
        self.p2_slots = [self.p2_monster_1, self.p2_monster_2, self.p2_monster_3, self.p2_monster_4, self.p2_monster_5,
                         self.p2_magic_1, self.p2_magic_2, self.p2_magic_3, self.p2_magic_4, self.p2_magic_5]

    def change_empty_placeholder(self, new_placeholder):
        """Allows user to change placeholder according to preference in order to visualize the game more clearly."""
        # Add logic to prevent bad input
        self.empty_placeholder = new_placeholder

    def display_board(self):
        """Prints terminal representation of the game board."""

        print("                               -----Kaiba-----\n")
        print([self.p2_graveyard_display, self.p2_magic_1, self.p2_magic_2, self.p2_magic_3, self.p2_magic_4,
               self.p2_magic_5])
        print(["         ", self.p2_monster_1, self.p2_monster_2, self.p2_monster_3,
               self.p2_monster_4, self.p2_monster_5])
        print("\n\n")
        print(["  " + self.field_zone + "  ", self.p1_monster_1, self.p1_monster_2, self.p1_monster_3,
               self.p1_monster_4, self.p1_monster_5])
        print([self.p1_graveyard_display, self.p1_magic_1, self.p1_magic_2, self.p1_magic_3, self.p1_magic_4,
               self.p1_magic_5])
        print("\n                             -----Yugi-----\n")


class Player:
    """Player objects represent the two players in the game."""

    def __init__(self, name, player_deck: Deck):
        """Players initialized with a unique deck and 4000 life points."""
        self.name = name
        self.player_deck = player_deck
        self.life_points = 4000
        self.hand = []
        self.graveyard = []
        self.summoned_monster_this_turn = False

    def shuffle_and_start_hand(self):
        """Shuffles player's deck then deals 5 cards to create their starting hand."""
        self.player_deck.shuffle()
        for i in range(5):
            self.hand.append(self.player_deck.pop())

    def __repr__(self):
        return self.name
