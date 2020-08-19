import random
from termcolor import colored


class Card:
    """A Card object in the game."""

    """Overarching class encompassing all card types in the game. Each card has attributes of name, ten character name,
    position (on field), location, and effect. No cards in game are purely Card objects, rather the various types of 
    cards that inherit from this class (Monster, Magic, Trap, Equip, Field) are the objects that are interacted with in
    the playing of the game.
    """

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

    """Inherits from Card class, name, ten character name, and effect. Further attributes unique to the Monster class
    are defined. These include attack, defense, level, monster_type, and attribute. Instances also contain attributes
    of attacked_this_turn and sent_to_grave_this_turn which are set to False and are used in gameplay to track what
    actions monsters can perform at various stages of play.
    
    Monster are represented differently on the game board based on their position attribute and all monsters are 
    represented with blue text for clarity.
    """

    def __init__(self, name, ten_char_name, effect, attack, defense, level, monster_type, attribute):
        super().__init__(name, ten_char_name, effect)
        self.attack = attack
        self.defense = defense
        self.level = level
        self.monster_type = monster_type
        self.attribute = attribute
        self.effect = effect
        self.attacked_this_turn = False
        self.sent_to_grave_this_turn = False

    def __repr__(self):
        if self.position == "FD":
            return colored("Face Down Monster", "blue")
        elif self.position is not None:
            return colored(f"{self.name}/{self.position}", "blue")
        else:
            return colored(self.name, "blue")


class Trap(Card):
    """Trap Card object."""

    """Inherits from Card class, name, ten character name, and effect. A further attribute of trap_type is defined. 
    Traps are represented in red text in the game for clarity.
    """

    def __init__(self, name, ten_char_name, effect, trap_type):
        super().__init__(name, ten_char_name, effect)
        self.trap_type = trap_type

    def __repr__(self):
        return colored(self.name, "red")


class Magic(Card):
    """Magic Card object."""

    """Inherits from Card class, name, ten character name, and effect. Magic are represented in green text in the game 
    for clarity.
    """

    def __init__(self, name, ten_char_name, effect):
        super().__init__(name, ten_char_name, effect)

    def __repr__(self):
        return colored(self.name, "green")


# class Equip(Magic):
#     """Equip Magic Card object."""
#
#     """Inherits from Magic class, name, ten character name, effect. Equip are represented in green text in the game
#     for clarity.
#     """
#
#     def __init__(self, name, ten_char_name, effect):
#         super().__init__(name, ten_char_name, effect)
#         self.target_monster = None
#
#     def __repr__(self):
#         return colored(self.name, "green")
#
#
# class Field(Card):
#     """Field Magic Card object."""
#
#     """Inherits from Magic class, name, ten character name, effect. Magic are represented in green text in the game
#     for clarity.
#     """
#
#     def __init__(self, name, ten_char_name, effect):
#         super().__init__(name, ten_char_name, effect)
#
#     def __repr__(self):
#         return colored(self.name, "green")


class Deck:
    """Player's deck of Cards."""

    """Deck is a list of Card objects (50 cards per deck). Contains methods to shuffle the deck, pop the top card from
    the deck, retrieve the length of the deck, and check if the deck has no cards left.
    """

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
    """Game board object."""

    """Board contains spaces for each players 5 monster spots, 5 magic/trap spots, a field zone, and two
    graveyard spaces to match the aesthetic of a physical board. Contains a method to display the board to the screen
    and to change the empty placeholder to user preference, for clarity purposes.
    """

    def __init__(self):
        """Set all game spaces to the empty placeholder, to be changed by user according to their preferences, and the
        graveyard spots and field zone spot to text descriptors.
        """
        self.empty_placeholder = "----------"
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
        print([self.empty_placeholder, self.p2_monster_1, self.p2_monster_2, self.p2_monster_3,
               self.p2_monster_4, self.p2_monster_5])
        print("\n\n")
        print([self.field_zone, self.p1_monster_1, self.p1_monster_2, self.p1_monster_3, self.p1_monster_4,
              self.p1_monster_5])
        print([self.p1_graveyard_display, self.p1_magic_1, self.p1_magic_2, self.p1_magic_3, self.p1_magic_4,
               self.p1_magic_5])
        print("\n                                -----Yugi-----\n")


class Player:
    """Player objects represent the two players in the game."""

    """Each player has a name, player_deck which is a Deck object, life points, a hand and graveyard which are empty
    lists which are populated with cards as the game progresses, and a summon_monster_this_turn attribute to keep 
    track of their ability to perform certain actions. Contains a method to shuffle their deck and deal a starting hand
    of 5 cards, which is called at the beginning of the game.
    """

    def __init__(self, name, player_deck: Deck):
        """Players initialized with a unique deck and 4000 life points."""
        self.name = name
        self.player_deck = player_deck
        self.life_points = 4000
        self.hand = []
        self.graveyard = []
        self.summoned_monster_this_turn = False
        self.damage_taken_this_turn = 0

    def shuffle_and_start_hand(self):
        """Shuffles player's deck then deals 5 cards to create their starting hand."""
        self.player_deck.shuffle()
        for i in range(5):
            self.hand.append(self.player_deck.pop())

    def __repr__(self):
        return self.name
