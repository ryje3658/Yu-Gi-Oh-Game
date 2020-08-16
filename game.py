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

        while True:
            print("Main phase starting...")
            print("Type the index [1..] of the card you'd like to play. Or type x if you'd like to end your first main "
                  "phase.")
            user_input = input()
            if user_input == "x":
                print("Ending main phase.")
                return
            else:
                try:
                    card_to_play = self.current_player.hand[int(user_input) - 1]
                    # Player choose to play a Monster card
                    if isinstance(card_to_play, Monster):
                        print("You chose a monster card.")
                    elif isinstance(card_to_play, Magic):
                        print("You chose a magic card.")
                    elif isinstance(card_to_play, Trap):
                        print("You chose a trap card.")
                except IndexError:
                    print("Please provide a valid index.")

    def battle_phase(self):
        pass

    def check_for_win(self):
        """Checks if either player has ran out of life points or if either player is unable to draw a card. Updates the
        game state if either condition is met.
        """
        if self.p1.life_points <= 0 or self.p1.player_deck.is_empty():
            self.game_state = "Kaiba won!"
        elif self.p2.life_points <= 0 or self.p2.player_deck.is_empty():
            self.game_state = "Yugi won!"
        else:
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
            self.draw_phase()

            # Main Phase
            self.main_phase()

            # Battle Phase
            self.battle_phase()

            # Main Phase
            self.main_phase()

            # Check for win
            self.check_for_win()
            if self.game_state != "In Progress...":
                print(self.game_state)
                break

            # Prepare for next player's turn, changing current player, incrementing turn count
            self.turn_count += 1
            if self.current_player == self.p1:
                self.current_player = self.p2
            else:
                self.current_player = self.p1


if __name__ == "__main__":
    game = Game()
    game.play_game()
