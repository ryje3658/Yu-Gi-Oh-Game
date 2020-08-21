# Yu-Gi-Oh! Game

<!-- ABOUT THE PROJECT -->
## About The Project


A terminal playable yu-gi-oh game based on the first iteration of the trading card game released in America, 
featuring the two original characters and their decks (collection of cards). Players take turns placing
magic, trap, and monster cards, and choosing actions within the rules of the game. The first player to reduce
the other's lifepoints to 0, wins!


### Built With

* [Python]()


<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple steps.

1. Clone the repo
```sh
git clone https://github.com/ryje3658/yu_gi_oh_game
```
2. Install termcolor (the only necessary module not included in Python standard library.)
```sh
pip install termcolor
```
3. Run the game!


(The two decks are included in the cards.py file and are created by making instances of the Monster, Magic,
and Trap classes defined in game_objects.py. You could create any cards you wanted by creating instances of
these classes, though any unique card effects would have to be defined in the cards.py file and added to the
card_effects attribute of the Game class.)


![alt text](https://github.com/ryje3658/yu_gi_oh_game/blob/master/yugioh_demo_smaller.gif "Game Demo")
