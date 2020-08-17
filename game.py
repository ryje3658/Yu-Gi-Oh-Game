from cards import *
import time
from termcolor import colored


class Game:
    """Handles the playing of a Yu-gi-oh duel."""

    def __init__(self):
        """Initializes two players with unique decks and a new game board, setting the game state to in
        progress, the turn count to 0, and randomly determining which player moves first.
        """
        self.game_state = "In Progress..."
        self.phase = None
        self.p1 = Player("Yugi", yugis_deck)
        self.p2 = Player("Kaiba", kaibas_deck)
        self.current_player = (self.p1 if random.randint(0, 1) else self.p2)
        self.opposing_player = (self.p1 if self.current_player == self.p2 else self.p2)
        self.board = Board()
        self.turn_count = 0

    def start_game(self):
        """Shuffles both player decks, deals hands, and provides a welcome message that says whose turn it is."""
        for player in [self.p1, self.p2]:
            player.shuffle_and_start_hand()
        print(f"\nWelcome! Each player starts with {self.p1.life_points} life points. A coin has been flipped and it "
              f"has been decided that {self.current_player.name} will go first!")

    def draw_phase(self):
        """Player draws one card from their deck and adds it to their hand. Displays new hand to player. First player '
        to move does not draw a card.
        """
        if self.turn_count != 0:
            print("Drawing a card...")
            time.sleep(1.25)
            self.current_player.hand.append(self.current_player.player_deck.pop())

    def main_phase(self):
        """Players are able to place cards onto the field according to the rules."""

        if self.current_player == self.p1:
            abbrev = "p1"
        else:
            abbrev = "p2"

        def main_phase_user_input():
            """Prompts user to enter input based on potential actions they can take. Returns that input."""
            print(colored("Possible actions to take...", "blue"))
            print(f"Type [1-{len(self.current_player.hand)}]: to play a card your hand.\n"
                  f"Type 'f': to activate a magic or trap card on the field or change the position of a monster.\n"
                  f"Type 'x': to end the main phase.\n")
            action_input = input()
            return action_input

        def check_for_open_spot(player_abbrev, card_type, slot_num):
            """Checks if a space is occupied by a card."""
            slot = player_abbrev + f"_{card_type}_" + slot_num
            if getattr(self.board, slot) == self.board.empty_placeholder:
                return slot
            else:
                return False

        def check_for_monster(player_abbrev, card_type, slot_num):
            """Checks if a space is occupied by a monster. Returns that Monster object if so."""
            slot = player_abbrev + f"_{card_type}_" + slot_num
            if isinstance(getattr(self.board, slot), Monster):
                return getattr(self.board, slot)
            else:
                return False

        def check_for_set_magic_or_trap(player_abbrev, card_type, slot_num):
            """Checks if the player has a set magic or trap card in the specified location, returns it if so."""
            slot = player_abbrev + f"_{card_type}_" + slot_num
            if isinstance(getattr(self.board, slot), Magic or Trap):
                return getattr(self.board, slot)
            else:
                return False

        def set_magic_or_trap(mag_trap):
            slot_number = input(f"Which magic or trap slot would you like to place {mag_trap.name} in? [1-5]")
            ready_to_place = check_for_open_spot(abbrev, "magic", slot_number)
            if not ready_to_place:
                print(colored("Invalid location, try again!", "red"))
            # Set magic or trap position to "SET"
            mag_trap.position = "SET"
            # Place magic or trap card on board
            setattr(self.board, ready_to_place, mag_trap)
            # Remove card from hand after card is placed on field.
            self.current_player.hand.remove(mag_trap)

        def activate_magic_or_trap():
            """Activates the effect of a magic or trap card on the field."""
            slot_number = input(f"Which magic or trap card on the field would you like to activate? [1-5]")
            card_to_activate = check_for_set_magic_or_trap(abbrev, "magic", slot_number)
            if not card_to_activate:
                print(colored("Invalid location, try again!", "red"))
            # Set magic or trap position to "FACEUP"
            card_to_activate.position = "FACEUP"
            # Activate card's specific effect
            card_to_activate.effect()
            print(card_to_activate, "effect activated!")

        def activate_magic_or_trap_from_hand(card_from_hand):
            """Activates the effect of a magic or trap card directly from the hand."""
            card_to_activate = card_from_hand
            if isinstance(card_to_activate, Magic or Trap):
                # Activate card's specific effect
                card_to_activate.effect()
                print(card_to_activate, "effect activated!")
                # Move card to graveyard
                self.current_player.graveyard.append(card_to_activate)
                # Remove card from hand
                self.current_player.hand.remove(card_to_activate)
            else:
                print(colored("Invalid card, try again!", "red"))

        def summon_monster(monster):
            """Summons a monster from player's hand to the field."""
            if self.current_player.summoned_monster_this_turn is False:
                slot_number = 0
                ready_to_place = False
                while not int(slot_number) in range(1, 6) and not ready_to_place:
                    # Choose where to place monster on board
                    slot_number = input(f"Which monster slot would you like to place {monster.name} in? [1-5]")
                    ready_to_place = check_for_open_spot(abbrev, "monster", slot_number)

                    # Choose position of monster (attack, defence, face down defence)
                    monster_position = input("What position would you like your monster in? a for attack, d for defence"
                                             " or f for face-down defence.")
                    if monster_position == "a":
                        monster.position = "ATK"
                    elif monster_position == "d":
                        monster.position = "DEF"
                    elif monster_position == "f":
                        monster.position = "FD"
                    else:
                        print("Invalid input try again!")
                        return
                # Place monster on the board
                setattr(self.board, ready_to_place, monster)
                self.current_player.summoned_monster_this_turn = True
            # Prevent player from summoning multiple monsters in a turn
            elif self.current_player.summoned_monster_this_turn:
                print(colored("You can't summon another monster this turn!", "red"))
            # Remove card from hand after card is placed on field.
            self.current_player.hand.remove(monster)

        def change_monster_position():
            """Changes the position attribute of a Monster on the field. (To attack or defense.)"""
            monster_slot_num = input("Please enter 1-5 to choose the monster you'd like to alter.")
            monster_on_field = check_for_monster(abbrev, "monster", monster_slot_num)
            if monster_on_field is not False:
                desired_position = input("What position would you like the monster in?\n"
                                         "'a' : attack\n"
                                         "'d' : defense\n")
                if desired_position == "a":
                    monster_on_field.position = "ATK"
                elif desired_position == "d":
                    monster_on_field.position = "DEF"
                else:
                    print(colored("Invalid input. Please try again!", "red"))

        def change_card_on_field():
            """Prompts user to specify what kind of action they want to take on a card on the field."""
            magic_or_monster = input("Type 'm' to select a monster card or 's' to select a magic or trap card.")
            # Change the position of a monster on the field.
            if magic_or_monster == 'm':
                change_monster_position()
            # Activate a magic or trap card on the field.
            elif magic_or_monster == 's':
                activate_magic_or_trap()
            else:
                print(colored("Invalid input. Please try again!", "red"))

        def play_card_from_hand(hand_input):
            """Player chose to play a card from their hand. Prompts for input of which card and what they would like
            to do.
            """
            try:
                card_to_play = self.current_player.hand[int(hand_input) - 1]
                # Player chose to play a Monster card
                if isinstance(card_to_play, Monster):
                    summon_monster(card_to_play)
                # Player chose to play a Trap or Magic Card
                else:
                    set_or_activate = input("Type s if you would like to set the magic/trap card or a if you would "
                                            "like to activate the card now.")
                    # Set a magic or trap card on the field.
                    if set_or_activate == "s":
                        set_magic_or_trap(card_to_play)
                    # Activate a magic or trap card from the hand.
                    elif set_or_activate == "a":
                        activate_magic_or_trap_from_hand(card_to_play)
                    else:
                        print(colored("Invalid input...please try again!", "red"))
            except IndexError:
                print(colored("Please provide a valid index.", "red"))

        def check_valid_hand_and_play(user_input_hand):
            """Checks if user input a value index to play a card from their hand, then plays that card or informs the
            user they've provided invalid input.
            """
            try:
                if 1 <= int(user_input_hand) <= len(self.current_player.hand):
                    play_card_from_hand(int(user_input_hand))
                else:
                    print(colored("Invalid index. Please enter a valid index!", "red"))
            except ValueError:
                print(colored("Invalid input. Please try again!", "red"))

        # -- Main Phase -- Main Loop Logic --
        while True:
            # Display the board, players' life points, and the current player's hand after each action
            print("\n")
            self.display_life_points()
            self.board.display_board()
            print("Your hand:", self.current_player.hand)

            # Determine action to take depending on user input
            user_input = main_phase_user_input()
            if user_input == "x":
                print("Ending main phase.")
                return
            # Change card on the field
            elif user_input == "f":
                change_card_on_field()
            # Play card from hand/catch invalid input
            else:
                check_valid_hand_and_play(user_input)

    def battle_phase(self):
        pass

    def update_game_state(self):
        """Checks if either player has ran out of life points or if either player is unable to draw a card. Updates the
        game state if either condition is met.
        """
        if self.p1.life_points <= 0 or self.p1.player_deck.is_empty():
            self.game_state = "Kaiba won!"
        elif self.p2.life_points <= 0 or self.p2.player_deck.is_empty():
            self.game_state = "Yugi won!"
        else:
            pass

    def next_turn(self):
        """Prepare for next player's turn, changing current player, opposing player, incrementing turn count, and
        resetting player's ability to summon a monster for their next turn.
        """
        self.turn_count += 1
        self.current_player.summoned_monster_this_turn = False
        if self.current_player == self.p1:
            self.current_player = self.p2
            self.opposing_player = self.p1
        else:
            self.current_player = self.p1
            self.opposing_player = self.p2

    def update_board(self):
        """Before switching between players, updates the board so that the opposing player can only see cards that
        should be visible to them.
        """
        pass

    def display_life_points(self):
        """Displays both players' life points to the terminal."""

        current_lp_str = f"{self.current_player.name}: {self.current_player.life_points} life points"
        opposing_lp_str = f"{self.opposing_player.name}: {self.opposing_player.life_points} life points"

        print(colored(current_lp_str, "magenta"))
        print(colored(opposing_lp_str, "magenta"))

    def play_game(self):
        """Handles playing the game. Provides instructions turn by turn, accepting player input from terminal via
        keystrokes.
        """
        self.start_game()

        # Main loop to run game.
        while True:
            # Display board and inform player of whose turn it is.
            print(f"It is {self.current_player}'s turn.")

            # Draw phase
            self.draw_phase()

            # Main Phase
            self.main_phase()

            # Battle Phase
            self.battle_phase()

            # Main Phase 2
            self.main_phase()

            # Update game state and then check for win, display message if win
            self.update_game_state()
            if self.game_state != "In Progress...":
                print(self.game_state)
                break

            # Get ready for the opposite player's turn
            print("Your turn is over...")
            self.next_turn()


if __name__ == "__main__":
    game = Game()
    game.play_game()
