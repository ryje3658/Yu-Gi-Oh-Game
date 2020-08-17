from game_objects import *
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
        print(f"Your hand:", self.current_player.hand)

    def main_phase(self):
        """Players are able to place cards onto the field according to the rules."""

        if self.current_player == self.p1:
            abbrev = "p1"
        else:
            abbrev = "p2"

        def check_for_open_spot(player_abbrev, card_type, slot_num):
            """Checks if a space is occupied by a card."""
            slot = player_abbrev + f"_{card_type}_" + slot_num
            if getattr(self.board, slot) == self.board.empty_placeholder:
                return slot
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

        def activate_magic_or_trap(mag_trap):
            pass

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

        def change_monster_position():
            pass

        while True:
            print(f"Type [1-{len(self.current_player.hand)}]: to play a card your hand.\n"
                  f"Type 'f': to activate or change the position of a card on the field.\n"
                  f"Type 'x': to end the main phase.\n")
            user_input = input()
            if user_input == "x":
                print("Ending main phase.")
                return
            elif user_input == "f":
                # user must select a card on the field to either activate or change positions
                # select a card given the options of cards the current player has on field
                # depending on what card it is - call function to change position or activate effect
                # BOOM
                pass
            else:
                try:
                    card_to_play = self.current_player.hand[int(user_input) - 1]
                    # Player chose to play a Monster card
                    if isinstance(card_to_play, Monster):
                        summon_monster(card_to_play)
                    # Player chose to play a Trap or Magic Card
                    else:
                        set_or_activate = input("Type s if you would like to set the magic/trap card or a if you would "
                                                "like to activate the card now.")
                        # Set a magic or trap card.
                        if set_or_activate == "s":
                            set_magic_or_trap(card_to_play)
                        # Activate a magic or trap card.
                        elif set_or_activate == "a":
                            activate_magic_or_trap(card_to_play)
                        else:
                            print(colored("Invalid input...please try again!", "red"))
                except IndexError:
                    print(colored("Please provide a valid index.", "red"))

    def battle_phase(self):
        print("PLACEHOLDER BATTLE PHASE")
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
        """Prepare for next player's turn, changing current player, incrementing turn count, and resetting ability to
        summon a monster."""
        self.turn_count += 1
        self.current_player.summoned_monster_this_turn = False
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

    def update_board(self):
        """Before switching between players, updates the board so that the opposing player can only see cards that
        should be visible to them.
        """
        pass

    def play_game(self):
        """Handles playing the game. Provides instructions turn by turn, accepting player input from terminal via
        keystrokes.
        """
        self.start_game()

        # Main loop to run game.
        while True:
            # Display board and inform player of whose turn it is.
            self.board.display_board()
            print(f"It is {self.current_player}'s turn.")

            # Draw phase
            print("Starting draw phase...")
            self.draw_phase()

            # Main Phase
            print("Starting main phase 1...")
            self.main_phase()

            # Battle Phase
            print("Starting battle phase...")
            self.battle_phase()

            # Main Phase
            print("Starting main phase 2...")
            print(self.board)
            print(self.current_player.hand)
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
