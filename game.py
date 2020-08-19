from cards import *
import time
from termcolor import colored


class Game:
    """A Yu-Gi-Oh Game object."""

    """Handles the playing of a Yu-gi-oh duel by keeping track of the game state, turn count, current player and 
    opposing player relative to the turn. Game is handled with a nested series of while loops representing the overall 
    flow of the game, then the flow of a player's turn, the the flow of each phase (Draw, Main 1, Battle, Main 2) in 
    that turn and then the set of steps within that phase. Game class also has an attribute card_effects that is a 
    dictionary containing functions representing the unique effects of each card which has an effect.
    """

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
        self.card_effects = {"The Wicked Worm Beast": the_wicked_worm_beast_eff, "Lord of D.": lord_of_d_eff,
                             "Mysterious Puppeteer": mysterious_puppeteer_eff, "Hane-Hane": hane_hane_eff, "Sogen":
                                 sogen_eff, "Flute of Summoning Dragon":
                                 flute_of_summoning_dragon_eff, "Ancient Telescope": ancient_telescope_eff,
                             "Inexperienced Spy": inexperienced_spy_eff, "De-Spell": de_spell_eff, "Fissure":
                                 fissure_eff, "Oozaki": oozaki_eff, "Dark Hole": dark_hole_eff, "Invigoration":
                                 invigoration_eff, "Dark Energy": dark_energy_eff, "Ultimate Offering":
                                 ultimate_offering_eff, "Castle Walls": castle_walls_eff, "Reverse Trap":
                                 reverse_trap_eff, "Just Desserts": just_desserts_eff, "The Stern Mystic":
                                 the_stern_mystic_eff, "Wall of Illusion": wall_of_illusion_eff, "Trap Master":
                                 trap_master_eff, "Man-Eater Bug": man_eater_bug_eff, "Monster Reborn":
                                 monster_reborn_eff, "Remove Trap": remove_trap_eff, "Sword of Dark Destruction":
                                 sword_of_dark_destruction_eff, "Book of Secret Arts": book_of_secret_arts_eff,
                             "Dian Keto the Cure Master": dian_keto_the_cure_master_eff, "Change of Heart":
                                 change_of_heart_eff, "Last Will": last_will_eff, "Soul Exchange": soul_exchange_eff,
                             "Card Destruction": card_destruction_eff, "Yami": yami_eff, "Reinforcements":
                                 reinforcements_eff, "Two-Pronged Attack": two_pronged_attack_eff, "Trap Hole":
                                 trap_hole_eff, "Dragon Capture Jar": dragon_capture_jar_eff, "Waboku": waboku_eff}

    def start_game(self):
        """Shuffles both player decks, deals hands, and provides a welcome message explaining the basic gameplay."""
        for player in [self.p1, self.p2]:
            player.shuffle_and_start_hand()
        print(colored("________________________________________________", "green"))
        print(colored("________________________________________________", "green"))
        print(colored("________________________________________________", "green"))
        print(colored(f"\nWelcome! Each player starts with {self.p1.life_points} life points. A coin has been flipped "
                      f"and it has\nbeen decided that {self.current_player.name} will go first! Each turn, players will"
                      f" have a drawing phase, main\nphase 1, battle phase, then main phase 2,"
                      " where they will provide input according to the\nactions they'd like to take. The player who "
                      "reduces their opponent's life points to 0 or\ncauses their opponent to no longer have any cards "
                      "to draw wins.\n", "green"))
        print(colored("________________________________________________", "green"))
        print(colored("________________________________________________", "green"))
        print(colored("________________________________________________", "green"))
        print("\n")

    def draw_phase(self):
        """Player draws one card from their deck and adds it to their hand. Displays new hand to player. First player '
        to move does not draw a card.
        """
        if self.turn_count != 0:
            print(colored("Drawing a card...", "blue"))
            time.sleep(1.25)
            self.current_player.hand.append(self.current_player.player_deck.pop())

    def main_phase(self):
        """Players are able to place cards onto the field according to the rules. Players are also able to manipulate
        their cards on the field by changing their positions or activating card effects.
        """

        if self.current_player == self.p1:
            abbrev = "p1"
        else:
            abbrev = "p2"

        def main_phase_user_input():
            """Prompts user to enter input based on potential actions they can take. Returns that input."""
            print("\n")
            self.display_life_points()
            self.board.display_board()
            print(f"{self.current_player}'s hand: {self.current_player.hand}\n")
            print(colored("MAIN PHASE -- Possible actions to take...", "magenta"))
            print(colored(f"Type [1-{len(self.current_player.hand)}]: to play a card your hand.\n"
                          f"Type 'f': to activate a magic or trap card on the field or change the position of "
                          f"a monster.", "green"))
            print(colored(f"Type 'x': to end the main phase.\n", "red"))
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
            slot_number = input(colored(f"Which magic or trap slot would you like to place {mag_trap.name} in? [1-5]",
                                        "green"))
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
            slot_number = input(colored(f"Which magic or trap card on the field would you like to activate? [1-5]",
                                        "green"))
            card_to_activate = check_for_set_magic_or_trap(abbrev, "magic", slot_number)
            if not card_to_activate:
                print(colored("Invalid location, try again!", "red"))
            # Set magic or trap position to "FACEUP"
            card_to_activate.position = "FACEUP"
            # Activate card's specific effect by calling function
            card_effect_function = self.card_effects[card_to_activate.name]
            card_effect_function(self)
            print(card_to_activate, "effect activated!", card_effect_function.__doc__)

        def activate_magic_or_trap_from_hand(card_from_hand):
            """Activates the effect of a magic or trap card directly from the hand."""
            card_to_activate = card_from_hand
            if isinstance(card_to_activate, Magic) or isinstance(card_to_activate, Trap):
                # Activate card's specific effect by calling function
                card_effect_function = self.card_effects[card_to_activate.name]
                card_effect_function(self)
                print(card_to_activate, "effect activated!", card_effect_function.__doc__)
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
                    slot_number = input(colored(f"Which monster slot would you like to place {monster.name} in? [1-5]",
                                                "green"))
                    ready_to_place = check_for_open_spot(abbrev, "monster", slot_number)

                    # Choose position of monster (attack, defense, face down defense)
                    monster_position = input(colored("What position would you like your monster in? a for attack, d for"
                                                     " defense or f for face-down defense.", "green"))
                    if monster_position == "a":
                        monster.position = "ATK"
                    elif monster_position == "d":
                        monster.position = "DEF"
                    elif monster_position == "f":
                        monster.position = "FD"
                    else:
                        print(colored("Invalid input try again!", "red"))
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
                desired_position = input(colored("What position would you like the monster in?\n"
                                                 "'a' : attack\n"
                                                 "'d' : defense\n", "green"))
                if desired_position == "a":
                    monster_on_field.position = "ATK"
                elif desired_position == "d":
                    monster_on_field.position = "DEF"
                else:
                    print(colored("Invalid input. Please try again!", "red"))

        def change_card_on_field():
            """Prompts user to specify what kind of action they want to take on a card on the field."""
            magic_or_monster = input(colored("Type 'm' to select a monster card or 's' to select a magic or trap card."
                                             , "green"))
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
            except IndexError:
                print(colored("Please provide a valid index.", "red"))
            else:
                # Player chose to play a Monster card
                if isinstance(card_to_play, Monster):
                    summon_monster(card_to_play)
                # Player chose to play a Trap or Magic Card
                else:
                    set_or_activate = input(colored("Type s if you would like to set the magic/trap card or a if you "
                                                    "would like to activate the card now.", "green"))
                    # Set a magic or trap card on the field.
                    if set_or_activate == "s":
                        set_magic_or_trap(card_to_play)
                    # Activate a magic or trap card from the hand.
                    elif set_or_activate == "a":
                        activate_magic_or_trap_from_hand(card_to_play)
                    else:
                        print(colored("Invalid input...please try again!", "red"))

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
            # Display the board, players' life points, and the current player's hand after each action.
            # Determine action to take depending on user input
            user_input = main_phase_user_input()
            if user_input == "x":
                return
            # Change card on the field
            elif user_input == "f":
                change_card_on_field()
            # Play card from hand/catch invalid input
            else:
                check_valid_hand_and_play(user_input)

    def battle_phase(self):
        """Players are able to use monsters they control to declare attacks on their opponents monsters, or in the case
        that the opponent has no monsters, they are able to attack their opponent's life points directly.
        """

        def monsters_able_to_attack(all_current_monsters):
            """Determines what monsters are able to attack this turn, by checking if they are in attack position.
            Returns a list of monster objects that are able to attack this turn.
            """

            return [x for x in all_current_monsters if x.position == "ATK" and x.attacked_this_turn is False]

        def player_not_able_to_attack(all_current_monsters):
            """Checks if player has no monsters able to attack. (All monsters are in defense position.) Returns True if
            all monsters are in defense position, returns False otherwise.
            """
            for monster in all_current_monsters:
                if monster.position == "ATK":
                    return False
            return True

        def select_monster_declaring_attack(able_to_attack):
            """Current player selects monster they'd like to initiate an attack from the list of valid monsters.
            Returns the monster declaring the attack.
            """
            print("These are your monsters that are able to attack:", able_to_attack)
            user_input = input(colored(f"Please choose a monster [1 - {len(able_to_attack)}] to initiate attack.",
                                       "green"))
            if int(user_input) in range(1, len(able_to_attack) + 1):
                return able_to_attack[int(user_input) - 1]
            else:
                print(colored("Invalid index, please try again!", "red"))

        def select_monster_to_attack(potential_targets):
            """Current player selects opponents' monster they'd like to attack. Receives a list of opponents monsters
            on the field. Returns that monster being attacked.
            """
            potential_targets = [x for x in potential_targets if x.sent_to_grave_this_turn is False]
            if not potential_targets:
                return False
            else:
                print("These are the monsters you can attack:", potential_targets)
                user_input = input(colored(f"Please choose a monster [1 - {len(potential_targets)}] to attack.",
                                           "green"))
                if int(user_input) in range(1, len(potential_targets) + 1):
                    return potential_targets[int(user_input) - 1]
                else:
                    print(colored("Invalid index, please try again!", "red"))

        def opposing_monsters(potential_targets):
            """Checks if the opponent has monsters on the field. Returns True if they do, False if they have none."""
            potential_targets = [x for x in potential_targets if x.sent_to_grave_this_turn is False]
            if not potential_targets:
                return False
            else:
                return True

        def direct_attack(direct_attacking_monster):
            """Monster attacks opponent directly subtracting their attack from the opponent's life points. Sets the
            attacking monster's attacked_this_turn attribute to True. Receives the attacking monster object, returns
            nothing.
            """
            damage = direct_attacking_monster.attack
            self.opposing_player.life_points -= damage
            direct_attacking_monster.attacked_this_turn = True
            print(colored(f"{direct_attacking_monster} attacked {self.opposing_player} directly, inflicting {damage} "
                          f"damage!", "red"))

        def damage_calc_update_life_points(atk_monster, tgt_monster):
            """Damage is calculated, life points are updated, and destroyed monsters are removed from the board and
            added to the graveyard.
            """
            damage_to_current_player = 0
            damage_to_opponent = 0

            def remove_monster_from_field(monster, player_indicator_num):
                """Removes the inputted monster from the board. Adds it to the graveyard of the correct player
                according to the player_indicator num.
                """
                for i in vars(self.board):
                    # Find monster to be removed
                    if vars(self.board)[i] == monster:
                        # Set that board's spot to the empty placeholder, removing monster from the board
                        vars(self.board)[i] = self.board.empty_placeholder
                        # Set monster as sent to graveyard this turn
                        monster.sent_to_grave_this_turn = True
                        # Send monster to the correct graveyard
                        if player_indicator_num == 0:
                            self.current_player.graveyard.append(monster)
                            print(colored(f"{monster} sent to {self.current_player}'s graveyard.\n", "red"))
                        else:
                            self.opposing_player.graveyard.append(monster)
                            print(colored(f"{monster} sent to {self.opposing_player}'s graveyard.\n", "red"))

            # Attacking defense position monster
            if tgt_monster.position == "DEF" or tgt_monster.position == "FD":
                # Attack > defense -- remove the defense monster from the field
                if atk_monster.attack - tgt_monster.defense > 0:
                    # Remove the defense position monster from the field
                    remove_monster_from_field(tgt_monster, 1)
                # Attack <= defense -- attacking player takes damage equal to difference, both monsters remain on field
                else:
                    damage_to_current_player += (tgt_monster.defense - atk_monster.attack)
            # Attacking attack position monster
            elif tgt_monster.position == "ATK":
                # Attack > attack of target monster, calculate damage and remove target monster from field
                if atk_monster.attack > tgt_monster.attack:
                    damage_to_opponent += (atk_monster.attack - tgt_monster.attack)
                    remove_monster_from_field(tgt_monster, 1)
                # Attack of both monsters is equal, both monsters are removed from the field, no life point damage
                elif atk_monster.attack == tgt_monster.attack:
                    remove_monster_from_field(tgt_monster, 1)
                    remove_monster_from_field(atk_monster, 0)
                # Attack < attack of target monster, calculate damage and remove attacking monster from field
                else:
                    damage_to_current_player += (tgt_monster.attack - atk_monster.attack)
                    remove_monster_from_field(atk_monster, 0)
            # Set the attacking monster's attribute of "attacked this turn" to True
            atk_monster.attacked_this_turn = True

            # Assign to player attribute for use with effect in card Waboku
            self.current_player.damage_taken_this_turn = damage_to_current_player
            self.opposing_player.damage_taken_this_turn = damage_to_opponent

            # Update life points for each player after damage calculation, inform users of damage done
            self.current_player.life_points = (self.current_player.life_points - damage_to_current_player)
            self.opposing_player.life_points = (self.opposing_player.life_points - damage_to_opponent)
            print(colored(f"Battle resulted in {damage_to_current_player} damage to {self.current_player} and"
                  f" {damage_to_opponent} damage to {self.opposing_player}!", "red"))

        # -- Battle Phase -- Main Logic Loop --
        while True:
            # No battle phase on the first player's turn
            if self.turn_count == 0:
                break
            elif player_not_able_to_attack(self.get_current_players_monsters()):
                print(colored("You have no monsters able to attack this turn. Battle phase ended.", "red"))
                break
            print(colored("BATTLE PHASE -- Possible actions to take...", "magenta"))
            print(colored("Type 'f': to declare at attack.", "green"))
            print(colored("Type 'x': to end the battle phase.", "red"))
            user_decision = input()
            if user_decision == 'x':
                break
            elif user_decision == 'f':
                # Determine set of possible monsters to attack
                attack_pos_monsters = monsters_able_to_attack(self.get_current_players_monsters())
                # Determine the attacking monster
                monster_attacking = select_monster_declaring_attack(attack_pos_monsters)
                # Determine the monster being attacked
                if opposing_monsters(self.get_opposing_players_monsters()) is False:
                    # If opponent has no monsters left, direct attack on opponent is initiated
                    direct_attack(monster_attacking)
                else:
                    target_monster = select_monster_to_attack(self.get_opposing_players_monsters())
                    # Damage calculation and update board
                    damage_calc_update_life_points(monster_attacking, target_monster)
                # Check if user has no more monsters able to attack
                if len(monsters_able_to_attack(self.get_current_players_monsters())) < 1:
                    print(colored("Battle phase over. You have no more monsters able to attack.", "red"))
                    break
            else:
                print(colored("Invalid input! Please try again!", "red"))

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

    def choose_current_monster(self):
        """Allows user to select one of their monsters from those on the field. Returns that monster."""
        currents_monsters = self.get_current_players_monsters()
        print("These are your monsters you can choose from:", currents_monsters)
        user_input = input(colored(f"Please choose a monster [1 - {len(currents_monsters)}].",
                                   "green"))
        if int(user_input) in range(1, len(currents_monsters) + 1):
            return currents_monsters[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def choose_monster_from_both_graveyards(self):
        both_graveyards = self.get_current_player_graveyard() + self.get_opposing_player_graveyard()
        both_graveyards = [x for x in both_graveyards if isinstance(x, Monster)]
        print("These are the monsters you can choose from either graveyard:", both_graveyards)
        user_input = input(colored(f"Please choose a monster [1 - {len(both_graveyards)}] to revive.",
                                   "green"))
        if int(user_input) in range(1, len(both_graveyards) + 1):
            return both_graveyards[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def choose_opponent_monster(self):
        """Allows user to select an opponent's monster from those on the field. Returns that monster."""
        opponents_monsters = self.get_opposing_players_monsters()
        print("These are your opponents monsters you can choose from:", opponents_monsters)
        user_input = input(colored(f"Please choose a monster [1 - {len(opponents_monsters)}].",
                                   "green"))
        if int(user_input) in range(1, len(opponents_monsters) + 1):
            return opponents_monsters[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def place_in_open_monster_spot(self, monster_to_place):
        """Finds an open monster spot on the current players side of the field. Places monster_to_place in that spot
        on the board.
        """
        if self.current_player == self.p1:
            open_spots = ["p1_monster_1", "p1_monster_2", "p1_monster_3", "p1_monster_4", "p1_monster_5"]
        else:
            open_spots = ["p2_monster_1", "p2_monster_2", "p2_monster_3", "p2_monster_4", "p2_monster_5"]

        for item in open_spots:
            if not isinstance(item, Monster):
                setattr(self.board, item, monster_to_place)
                break
        print(colored("You have no open spots to place a monster!", "red"))

    def all_monsters_attacked_to_false(self):
        """Sets all monsters on the field (attacked_this_turn) attribute to False, to allow for next turn."""
        for i in vars(self.board):
            # Find monster to be removed
            if isinstance(vars(self.board)[i], Monster):
                vars(self.board)[i].attacked_this_turn = False

    def all_monster_sent_grave_to_false(self):
        """Sets all monsters in the graveyards attribute (sent_to_grave_this_turn) to false, to allow for correct
        gameplay moving forward.
        """
        for card in [self.p1.graveyard, self.p2.graveyard]:
            if isinstance(card, Monster):
                card.sent_to_grave_this_turn = False

    def send_card_hand_to_graveyard(self, card_to_send):
        """Sends a card from a player's hand to their graveyard. Receives a card object and returns nothing."""
        if card_to_send in self.current_player.hand:
            self.current_player.hand.remove(card_to_send)
            self.current_player.graveyard.append(card_to_send)
        elif card_to_send in self.opposing_player.hand:
            self.opposing_player.hand.remove(card_to_send)
            self.opposing_player.graveyard.append(card_to_send)
        else:
            print(colored("Card is not in either player's hand!", "red"))

    def send_card_field_to_graveyard(self, card_to_send):
        """Sends a card from the field to the owner's graveyard. Receives a card object and returns nothing."""
        pass

    def summon_monster_from_graveyard(self, monster_to_summon):
        """Summons a monster from the graveyard to the field."""
        pass

    def get_current_player_graveyard(self):
        """Returns the current player's graveyard as a list of Card objects."""
        return self.current_player.graveyard

    def get_opposing_player_graveyard(self):
        """Returns the current player's graveyard as a list of Card objects."""
        return self.opposing_player.graveyard

    def get_current_players_monsters(self):
        """Returns a list of the current players monsters on the field."""
        if self.current_player == self.p1:
            currents_monsters = [x for x in [self.board.p1_monster_1, self.board.p1_monster_2, self.board.p1_monster_3,
                                 self.board.p1_monster_4, self.board.p1_monster_5] if isinstance(x, Monster)]
        else:
            currents_monsters = [x for x in [self.board.p2_monster_1, self.board.p2_monster_2, self.board.p2_monster_3,
                                 self.board.p2_monster_4, self.board.p2_monster_5] if isinstance(x, Monster)]
        return currents_monsters

    def get_opposing_players_monsters(self):
        """Returns a list of the opposing player's monsters on the field."""
        if self.current_player == self.p1:
            opponents_monsters = [x for x in [self.board.p2_monster_1, self.board.p2_monster_2, self.board.p2_monster_3,
                                  self.board.p2_monster_4, self.board.p2_monster_5] if isinstance(x, Monster)]
        else:
            opponents_monsters = [x for x in [self.board.p1_monster_1, self.board.p1_monster_2, self.board.p1_monster_3,
                                  self.board.p1_monster_4, self.board.p1_monster_5] if isinstance(x, Monster)]
        return opponents_monsters

    def next_turn(self):
        """Prepare for next player's turn, changing current player, opposing player, incrementing turn count, resetting
        player's ability to summon a monster for their next turn, setting all monsters attacked_this_turn and
        sent_to_grave_this_turn attributes to False.
        """
        self.turn_count += 1
        self.current_player.summoned_monster_this_turn = False
        self.all_monsters_attacked_to_false()
        self.all_monster_sent_grave_to_false()
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

        print(colored(f"{self.current_player.name}: {self.current_player.life_points} life points", "magenta"))
        print(colored(f"{self.opposing_player.name}: {self.opposing_player.life_points} life points", "magenta"))

    def play_game(self):
        """Handles playing the game. Provides instructions turn by turn, accepting player input from terminal via
        keystrokes.
        """
        self.start_game()

        # Main loop to run game.
        while True:
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
            print(colored("Your turn is over...", "blue"))
            self.next_turn()


if __name__ == "__main__":
    game = Game()
    game.play_game()
