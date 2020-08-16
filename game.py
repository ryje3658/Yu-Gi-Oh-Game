from game_objects import *
from cards import *


class Game:
    """Handles the playing of a Yu-gi-oh duel."""

    def __init__(self):
        """Initializes two players with unique decks and a new game board, setting the game state to in
        progress, and randomly determines which player moves first.
        """
        self.game_state = "In Progress..."
        self.phase = None
        self.p1 = Player("Yugi", yugis_deck)
        self.p2 = Player("Kaiba", kaibas_deck)
        self.player_turn = (self.p1 if random.randint(0, 1) else self.p2)
        self.current_players_hand = self.player_turn.hand
        self.board = Board()

    def start_game(self):
        """Shuffles both player decks, deals hands, and provides a welcome message that says whose turn it is."""
        for player in [self.p1, self.p2]:
            player.shuffle_and_start_hand()
        print(f"\nWelcome! Each player starts with {self.p1.life_points} life points. A coin has been flipped and it "
              f"has been decided that {self.player_turn.name} will go first!")

    def play_game(self):
        """Handles playing the game. Provides instructions turn by turn, accepting player input from terminal via
        keystrokes.
        """
        self.start_game()


if __name__ == "__main__":
    game = Game()
    game.play_game()
