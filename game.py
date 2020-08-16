from game_objects import *
from cards import *
import time


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

        print("Main phase starting...")

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

        while True:
            print("Type the index [1..] of the card you'd like to play. Or type x if you'd like to end your first main "
                  "phase.")
            user_input = input()
            if user_input == "x":
                print("Ending main phase.")
                return
            else:
                try:
                    card_to_play = self.current_player.hand[int(user_input) - 1]
                    # Player chose to play a Monster card
                    if isinstance(card_to_play, Monster):
                        if self.current_player.summoned_monster_this_turn is False:
                            slot_number = 0
                            ready_to_place = False
                            while not int(slot_number) in range(1, 6) and not ready_to_place:
                                slot_number = input(f"Which monster slot would you like to place {card_to_play.name}"
                                                    f" in? [1-5]")
                                ready_to_place = check_for_open_spot(abbrev, "monster", slot_number)
                            setattr(self.board, ready_to_place, card_to_play)
                    # Player chose to play a Trap card
                    elif isinstance(card_to_play, Magic):
                        print("You chose a magic card.")
                    # Player chose to play a Magic card
                    elif isinstance(card_to_play, Trap):
                        print("You chose a trap card.")
                except IndexError:
                    print("Please provide a valid index.")

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
        """Prepare for next player's turn, changing current player, incrementing turn count."""
        print("Your turn is over.")
        self.turn_count += 1
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1

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
            self.draw_phase()

            # Main Phase
            self.main_phase()

            # Battle Phase
            self.battle_phase()

            # Main Phase
            self.main_phase()

            # Update game state and then check for win
            self.update_game_state()
            if self.game_state != "In Progress...":
                print(self.game_state)
                break

            # Get ready for the opposite player's turn
            self.next_turn()



if __name__ == "__main__":
    game = Game()
    game.play_game()
