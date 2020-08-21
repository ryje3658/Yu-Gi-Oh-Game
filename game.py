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
        self.card_effects = {"Hane-Hane": hane_hane_eff, "Sogen": sogen_eff, "Flute of Summoning Dragon":
                             flute_of_summoning_dragon_eff, "Ancient Telescope": ancient_telescope_eff,
                             "Inexperienced Spy": inexperienced_spy_eff, "De-Spell": de_spell_eff, "Fissure":
                                 fissure_eff, "Oozaki": oozaki_eff, "Dark Hole": dark_hole_eff, "Invigoration":
                                 invigoration_eff, "Dark Energy": dark_energy_eff, "Ultimate Offering":
                                 ultimate_offering_eff, "Castle Walls": castle_walls_eff, "Pot of Greed":
                                 pot_of_greed_eff, "Just Desserts": just_desserts_eff, "The Stern Mystic":
                                 the_stern_mystic_eff, "Trap Master": trap_master_eff, "Waboku": waboku_eff,
                                 "Man-Eater Bug": man_eater_bug_eff, "Monster Reborn":
                                 monster_reborn_eff, "Remove Trap": remove_trap_eff, "Sword of Dark Destruction":
                                 sword_of_dark_destruction_eff, "Book of Secret Arts": book_of_secret_arts_eff,
                                 "Dian Keto the Cure Master": dian_keto_the_cure_master_eff, "Change of Heart":
                                 change_of_heart_eff, "Last Will": last_will_eff, "Tribute to the Doomed":
                                 tribute_to_the_doomed_eff, "Card Destruction": card_destruction_eff, "Yami": yami_eff,
                                 "Reinforcements": reinforcements_eff, "Two-Pronged Attack": two_pronged_attack_eff,
                                 "Trap Hole": trap_hole_eff, "Dragon Capture Jar": dragon_capture_jar_eff}

    def start_game(self):
        """Shuffles both player decks, deals hands, and provides a welcome message explaining the basic gameplay."""
        for player in [self.p1, self.p2]:
            player.shuffle_and_start_hand()
        print("\n")
        print(colored("_________________________________________________________________________________________",
                      "green"))
        print(colored("_________________________________________________________________________________________",
                      "green"))
        print(colored("_________________________________________________________________________________________",
                      "green"))
        print(colored(f"\nWelcome! Each player starts with {self.p1.life_points} life points. A coin has been flipped "
                      f"and it has\nbeen decided that {self.current_player.name} will go first! Each turn, players will"
                      f" have a drawing phase, main\nphase 1, battle phase, then main phase 2,"
                      " where they will provide input according to the\nactions they'd like to take. The player who "
                      "reduces their opponent's life points to 0 or\ncauses their opponent to no longer have any cards "
                      "to draw wins.\n", "green"))
        print(colored("_________________________________________________________________________________________",
                      "green"))
        print(colored("_________________________________________________________________________________________",
                      "green"))
        print(colored("_________________________________________________________________________________________",
                      "green"))

    def draw_phase(self):
        """Player draws one card from their deck and adds it to their hand. Displays new hand to player. First player '
        to move does not draw a card.
        """
        if self.turn_count != 0:
            print(colored(f"{self.phase} -- Drawing a card...", "magenta", attrs=['bold']))
            time.sleep(1)
            self.current_player.hand.append(self.current_player.player_deck.pop())

    def end_phase(self):
        """Player has finished actions for their turn. Message displayed."""
        print(colored(f"{self.phase} -- Your turn is over...", "magenta", attrs=['bold']))
        time.sleep(1)

    def update_game_state(self):
        """Checks if either player has ran out of life points or if either player is unable to draw a card. Updates the
        game state if either condition is met.
        """
        if self.p1.life_points <= 0 or self.p1.player_deck.is_empty():
            self.game_state = "Kaiba won!"
        elif self.p2.life_points <= 0 or self.p2.player_deck.is_empty():
            self.game_state = "Yugi won!"

    def main_phase(self):
        """Players are able to place cards onto the field according to the rules. Players are also able to manipulate
        their cards on the field by changing their positions or activating card effects.
        """

        def main_phase_user_input():
            """Prompts user to enter input based on potential actions they can take. Returns that input."""
            print("\n")
            self.display_life_points()
            self.board.display_board()
            print(f"{self.current_player}'s hand: {self.current_player.hand}\n")
            print(colored(f"{self.phase} -- Possible actions to take...", "magenta", attrs=['bold']))
            print(colored(f"Type [1-{len(self.current_player.hand)}]: to play a card your hand.\n"
                          f"Type 'f': to activate a magic or trap card on the field or change the position of "
                          f"a monster.", "green"))
            print(colored(f"Type 'x': to end the main phase.\n", "red"))
            action_input = input()
            return action_input

        def set_magic_or_trap(mag_trap):
            """Sets magic/trap card on the field and then removes the card from the player's hand."""
            # Place magic or trap card on board in an open slot
            self.place_in_open_magic_trap_spot(mag_trap)
            # Update position to SET
            mag_trap.position = "SET"
            # Remove card from hand after card is placed on field.
            self.current_player.hand.remove(mag_trap)

        def activate_magic_or_trap():
            """Activates the effect of a magic or trap card on the field."""
            # Player selects card to activate from their magic/trap cards on the field
            card_to_activate = self.choose_current_magic_or_trap()
            card_effect_function = self.card_effects[card_to_activate.name]
            print(card_to_activate, "effect initiated...", card_effect_function.__doc__)
            if card_effect_function(self):
                # Set card position to ACTIVATED
                card_to_activate.position = "ACTIVATED"
                # Send card from field to the graveyard
                self.send_magic_field_to_graveyard(card_to_activate)
                # Else...message displayed will come from effect function being called

        def activate_magic_or_trap_from_hand(card_to_activate):
            """Activates the effect of a magic or trap card directly from the hand."""
            if isinstance(card_to_activate, Magic) or isinstance(card_to_activate, Trap):
                # Activate card's specific effect by calling function
                card_effect_function = self.card_effects[card_to_activate.name]
                print(card_to_activate, "effect initiated...", card_effect_function.__doc__)
                if card_effect_function(self):
                    # Set card position to ACTIVATED
                    card_to_activate.position = "ACTIVATED"
                    # Move card to graveyard
                    self.get_current_player_graveyard().append(card_to_activate)
                    # Remove card from hand
                    self.current_player.hand.remove(card_to_activate)
                    print("Effect resolved successfully!")
            else:
                print(colored("Invalid card, try again!", "red"))

        def summon_monster(monster):
            """Summons a monster from player's hand to the field. Receives a monster object and returns nothing."""
            if self.current_player.summoned_monster_this_turn is False:
                self.place_in_open_monster_spot(monster)
                self.summon_position(monster)
                self.current_player.summoned_monster_this_turn = True
                monster.position_changed_this_turn = True
                self.current_player.hand.remove(monster)
            else:
                print(colored("You can't summon another monster this turn!", "red"))

        def change_monster_position():
            """Changes the position attribute of a Monster on the field. (To attack or defense.)"""
            monster_on_field = self.choose_current_monster()
            if monster_on_field is not False:
                if monster_on_field.position_changed_this_turn:
                    print(colored("This monster has already changed positions this turn!", "red"))
                    return
                else:
                    monster_on_field.position_changed_this_turn = True
                    # If monster is face down and has a flip effect, activate flip effect after changing position
                    if monster_on_field.position == "FD" and monster_on_field.effect == "Flip":
                        self.change_position(monster_on_field)
                        self.activate_flip_effect(monster_on_field)
                    # All other cases- just change the monster's position
                    else:
                        self.change_position(monster_on_field)

        def change_card_on_field():
            """Prompts user to specify what kind of action they want to take on a card on the field."""
            while True:
                print(colored("Type 'm': to select a monster card on the field.", "green"))
                print(colored("Type 's': to select a magic or trap card on the field.", "green"))
                print(colored("Type 'x': to go back and choose a different action.", "red"))
                magic_or_monster = input()
                # Change the position of a monster on the field.
                if magic_or_monster == 'm':
                    change_monster_position()
                    return
                # Activate a magic or trap card on the field.
                elif magic_or_monster == 's':
                    activate_magic_or_trap()
                    return
                # Cancel action
                elif magic_or_monster == 'x':
                    return
                else:
                    print(colored("Invalid input. Please try again!", "red"))

        def set_or_activate_from_hand(magic_or_trap):
            while True:
                print(colored("Type 's': to set the magic/trap card.", "green"))
                print(colored("Type 'a': to activate the card now.", "green"))
                print(colored("Type 'x': to go back and choose a different action.", "red"))
                set_or_activate = input()
                # Set a magic or trap card on the field.
                if set_or_activate == "s":
                    set_magic_or_trap(magic_or_trap)
                    return
                # Activate a magic or trap card from the hand.
                elif set_or_activate == "a":
                    activate_magic_or_trap_from_hand(magic_or_trap)
                    return
                # Cancel action
                elif set_or_activate == 'x':
                    return
                else:
                    print(colored("Invalid input...please try again!", "red"))

        def play_card_from_hand(hand_input):
            """Player chose to play a card from their hand. Prompts for input of which card and what they would like
            to play. Different from choose card from hand function as this function uses the display of hand already
            there versus printing out the hand again to the user and receives a hand_input already declaring the card
            they are interested in playing. Returns nothing.
            """
            currents_cards = self.current_player.hand
            try:
                while True:
                    if int(hand_input) in range(1, len(currents_cards) + 1):
                        card_to_play = currents_cards[int(hand_input) - 1]
                        break
                    else:
                        print(colored("Invalid index, please try again!", "red"))
                        return
                # Player chose to play a Monster card
                if isinstance(card_to_play, Monster):
                    summon_monster(card_to_play)
                # Player chose to play a Trap or Magic Card
                else:
                    set_or_activate_from_hand(card_to_play)
            except ValueError:
                print(colored("Invalid input! Please try again!", "red"))

        # -- Main Phase -- Main Loop Logic --
        while True:
            # Display the board, players' life points, and the current player's hand after each action.
            user_input = main_phase_user_input()
            if user_input == "x":
                return
            # Change card on the field
            elif user_input == "f":
                change_card_on_field()
            # Play card from hand/catch invalid input
            else:
                play_card_from_hand(user_input)

    def battle_phase(self):
        """Players are able to use monsters they control to declare attacks on their opponents monsters, or in the case
        that the opponent has no monsters, they are able to attack their opponent's life points directly.
        """

        def battle_phase_input():
            print(colored(f"{self.phase} -- Possible actions to take...", "magenta", attrs=['bold']))
            print(colored("Type 'f': to declare at attack.", "green"))
            print(colored("Type 'x': to end the battle phase.", "red"))
            return input()

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

        def update_life_points(current_player_damage_to_calc, opponent_damage_to_calc):
            """Updates life points according to damage inflicted during battle. Receives damage adjustments to apply
            to each player's life points.
            """
            # Assign damage adjustments to player attribute for use with effect in card Waboku
            self.current_player.damage_taken_this_turn = current_player_damage_to_calc
            self.opposing_player.damage_taken_this_turn = opponent_damage_to_calc

            # Update life points for each player after damage calculation, inform users of damage done
            self.current_player.life_points = (self.current_player.life_points - current_player_damage_to_calc)
            self.opposing_player.life_points = (self.opposing_player.life_points - opponent_damage_to_calc)
            print(colored(f"Battle resulted in {current_player_damage_to_calc} damage to {self.current_player} and"
                          f" {opponent_damage_to_calc} damage to {self.opposing_player}!", "red"))

        def damage_calculation(atk_monster, tgt_monster):
            """Damage is calculated and destroyed monsters are removed from the board and added to the graveyard.
            Receives an attacking monster and a target monster. Returns nothing.
            """
            damage_to_current_player = 0
            damage_to_opponent = 0

            # Attacking defense position monster
            if tgt_monster.position == "DEF" or tgt_monster.position == "FD":
                # Attack > defense -- remove the defense monster from the field
                if atk_monster.attack - tgt_monster.defense > 0:
                    # Remove the defense position monster from the field
                    self.send_monster_field_to_graveyard(tgt_monster)
                # Attack <= defense -- attacking player takes damage equal to difference, both monsters remain on field
                else:
                    damage_to_current_player += (tgt_monster.defense - atk_monster.attack)
                # Target monster is face down and has a flip effect
                if tgt_monster.position == "FD" and tgt_monster.effect == "Flip":
                    tgt_monster.position = "DEF"
                    self.activate_flip_effect(tgt_monster)
            # Attacking attack position monster
            elif tgt_monster.position == "ATK":
                # Attack > attack of target monster, calculate damage and remove target monster from field
                if atk_monster.attack > tgt_monster.attack:
                    damage_to_opponent += (atk_monster.attack - tgt_monster.attack)
                    self.send_monster_field_to_graveyard(tgt_monster)
                # Attack of both monsters is equal, both monsters are removed from the field, no life point damage
                elif atk_monster.attack == tgt_monster.attack:
                    self.send_monster_field_to_graveyard(tgt_monster)
                    self.send_monster_field_to_graveyard(atk_monster)
                # Attack < attack of target monster, calculate damage and remove attacking monster from field
                else:
                    damage_to_current_player += (tgt_monster.attack - atk_monster.attack)
                    self.send_monster_field_to_graveyard(atk_monster)
            # Set the attacking monster's attribute of "attacked this turn" to True
            atk_monster.attacked_this_turn = True
            update_life_points(damage_to_current_player, damage_to_opponent)

        def choose_monsters_to_battle():
            """User selects a monster to attack and a target monster for the attack."""
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
                damage_calculation(monster_attacking, target_monster)

        # -- Battle Phase -- Main Logic Loop --
        while True:
            # No battle phase on the first player's turn
            if self.turn_count == 0:
                break
            # Check if user has no monsters able to attack, end battle phase if so
            elif player_not_able_to_attack(self.get_current_players_monsters()):
                print(colored("You have no monsters able to attack this turn. Battle phase ended.", "red"))
                break
            # User has decided to initiate an attack
            user_decision = battle_phase_input()
            if user_decision == 'x':
                break
            elif user_decision == 'f':
                choose_monsters_to_battle()
                # Check if user has no more monsters able to attack
                if len(monsters_able_to_attack(self.get_current_players_monsters())) < 1:
                    print(colored("Battle phase over. You have no more monsters able to attack.", "red"))
                    break
            else:
                print(colored("Invalid input! Please try again!", "red"))

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
            return False

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

    def choose_from_all_monsters_on_field(self):
        """Allows user to select a monster from either side of the field. Returns that monster."""
        all_monsters_on_field = self.get_all_monsters_on_field()
        print("These are all of the monsters on the field:",  all_monsters_on_field)
        user_input = input(colored(f"Please choose a monster [1 - {len(all_monsters_on_field)}].",
                                   "green"))
        if int(user_input) in range(1, len(all_monsters_on_field) + 1):
            return all_monsters_on_field[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def choose_from_all_magic_trap_on_field(self):
        """Allows user to select a magic or trap card from either side of the field. Returns that magic or trap card."""
        all_magic_trap_on_field = self.get_all_magic_trap()
        print("These are all of the magic and trap cards on the field:", all_magic_trap_on_field)
        user_input = input(colored(f"Please choose a card [1 - {len(all_magic_trap_on_field)}].",
                                   "green"))
        if int(user_input) in range(1, len(all_magic_trap_on_field) + 1):
            return all_magic_trap_on_field[int(user_input) - 1]
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

    def choose_monster_from_hand(self):
        """Selects a monster to move from the hand to the field, in case of special summoning."""
        currents_monsters = [x for x in self.current_player.hand if isinstance(x, Monster)]
        print("These are the monsters in your hand you can choose from:", currents_monsters)
        user_input = input(colored(f"Please choose a monster [1 - {len(currents_monsters)}].",
                                   "green"))
        if int(user_input) in range(1, len(currents_monsters) + 1):
            return currents_monsters[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def choose_card_from_hand(self):
        """Selects a card from the current player's hand. Receives nothing. Returns a card object."""
        currents_cards = self.current_player.hand
        print("These are the cards in your hand you can choose from:", currents_cards)
        user_input = input(colored(f"Please choose a card [1 - {len(currents_cards)}].",
                                   "green"))
        if int(user_input) in range(1, len(currents_cards) + 1):
            return currents_cards[int(user_input) - 1]
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
            if getattr(self.board, item) == self.board.empty_placeholder:
                setattr(self.board, item, monster_to_place)
                print(f"{monster_to_place} ready to be summoned...")
                return
        print(colored("No spaces open to place a monster!", "red"))

    def place_in_open_magic_trap_spot(self, mag_trap_to_place):
        """Finds an open magic/trap spot on the current players side of the field. Places the received object in that
        spot on the board ore returns an error message if there are no open spots.
        """
        if self.current_player == self.p1:
            open_spots = ["p1_magic_1", "p1_magic_2", "p1_magic_3", "p1_magic_4", "p1_magic_5"]
        else:
            open_spots = ["p2_magic_1", "p2_magic_2", "p2_magic_3", "p2_magic_4", "p2_magic_5"]

        for item in open_spots:
            if getattr(self.board, item) == self.board.empty_placeholder:
                setattr(self.board, item, mag_trap_to_place)
                print(f"{mag_trap_to_place} placed on board.")
                return
        print(colored("No spaces open to place a magic or trap card!", "red"))

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

    def all_monsters_changed_pos_to_false(self):
        """Sets all monsters change_position_this_turn attribute to False, to allow for correct gameplay in the
        following turns.
        """
        for monster in self.get_all_monsters_on_field():
            monster.position_changed_this_turn = False

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

    def send_monster_field_to_hand(self):
        """Sends Monster from the field to the respective player's hand. Receives Monster object and returns nothing."""
        monster_to_send = self.choose_from_all_monsters_on_field()
        if monster_to_send in self.get_current_players_monsters():
            self.current_player.hand.append(monster_to_send)
        else:
            self.opposing_player.hand.append(monster_to_send)
        self.monster_to_blank_space(monster_to_send)
        print(f"{monster_to_send} send back to the owner's hand!")

    def send_monster_field_to_graveyard(self, monster):
        """Sends monster card from field to the owner's graveyard. Receives monster card object and returns nothing."""
        for i in vars(self.board):
            # Find monster to be removed
            if vars(self.board)[i] == monster:
                if monster in self.get_current_players_monsters():
                    to_graveyard = self.current_player
                elif monster in self.get_opposing_players_monsters():
                    to_graveyard = self.opposing_player
                else:
                    print(colored("Error!", "red"))
                    return
                vars(self.board)[i] = self.board.empty_placeholder
                # Set monster as sent to graveyard this turn and player attribute monster_sent_to_gy to True
                monster.sent_to_grave_this_turn = True
                self.current_player.monster_sent_to_gy_this_turn = True
                # Send monster to the correct graveyard
                if to_graveyard == self.current_player:
                    self.current_player.graveyard.append(monster)
                    print(colored(f"{monster} sent to {self.current_player}'s graveyard.\n", "red"))
                else:
                    self.opposing_player.graveyard.append(monster)
                    print(colored(f"{monster} sent to {self.opposing_player}'s graveyard.\n", "red"))

    def send_magic_field_to_graveyard(self, magic):
        """Sends magic card from the field to the owner's graveyard. Receives magic card object and returns nothing."""
        for i in vars(self.board):
            if vars(self.board)[i] == magic:
                if magic in self.get_current_players_magic_trap():
                    to_graveyard = self.current_player
                elif magic in self.get_opponents_magic_trap():
                    to_graveyard = self.opposing_player
                else:
                    print(colored("Error!", "red"))
                    return
                vars(self.board)[i] = self.board.empty_placeholder
                if to_graveyard == self.current_player:
                    self.current_player.graveyard.append(magic)
                else:
                    self.opposing_player.graveyard.append(magic)

    def monster_to_blank_space(self, card):
        """Removes Monster from the board without sending it anywhere. Replaces monster with empty placeholder. Receives
        monster object and returns nothing.
        """
        monster_spots = ["p1_monster_1", "p1_monster_2", "p1_monster_3", "p1_monster_4", "p1_monster_5",
                         "p2_monster_1", "p2_monster_2", "p2_monster_3", "p2_monster_4", "p2_monster_5"]

        for i in monster_spots:
            if getattr(self.board, i) == card:
                setattr(self.board, i, self.board.empty_placeholder)
                break

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

    def get_current_players_magic_trap(self):
        """Returns a list of the current player's magic and trap cards on the field."""
        if self.current_player == self.p1:
            currents_mag_trap = [x for x in [self.board.p1_magic_1, self.board.p1_magic_2, self.board.p1_magic_3,
                                 self.board.p1_magic_4, self.board.p1_magic_5] if isinstance(x, Magic) or
                                 isinstance(x, Trap)]
        else:
            currents_mag_trap = [x for x in [self.board.p2_magic_1, self.board.p2_magic_2, self.board.p2_magic_3,
                                 self.board.p2_magic_4, self.board.p2_magic_5] if isinstance(x, Magic) or
                                 isinstance(x, Trap)]
        return currents_mag_trap

    def get_opponents_magic_trap(self):
        """Returns a list of the current player's magic and trap cards on the field."""
        if self.current_player != self.p1:
            opponents_mag_trap = [x for x in [self.board.p1_magic_1, self.board.p1_magic_2, self.board.p1_magic_3,
                                  self.board.p1_magic_4, self.board.p1_magic_5] if isinstance(x, Magic) or
                                  isinstance(x, Trap)]
        else:
            opponents_mag_trap = [x for x in [self.board.p2_magic_1, self.board.p2_magic_2, self.board.p2_magic_3,
                                  self.board.p2_magic_4, self.board.p2_magic_5] if isinstance(x, Magic) or
                                  isinstance(x, Trap)]
        return opponents_mag_trap

    def get_all_magic_trap(self):
        """Returns a list of all the magic and trap cards on the field."""
        return self.get_opponents_magic_trap() + self.get_current_players_magic_trap()

    def choose_current_magic_or_trap(self):
        """Allows user to select a magic or trap from theirs on the field. Returns that magic or trap."""
        current_magic_or_trap = self.get_current_players_magic_trap()
        print("These are your magic/trap cards you can choose from:", current_magic_or_trap)
        user_input = input(colored(f"Please choose a magic/trap [1 - {len(current_magic_or_trap)}].",
                                   "green"))
        if int(user_input) in range(1, len(current_magic_or_trap) + 1):
            return current_magic_or_trap[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def choose_opponent_magic_or_trap(self):
        """Allows user to select an opponent's magic or trap from those on the field. Returns that magic or trap."""
        opponents_magic_or_trap = self.get_opponents_magic_trap()
        print("These are your opponents magic/trap cards you can choose from:", opponents_magic_or_trap)
        user_input = input(colored(f"Please choose a magic/trap [1 - {len(opponents_magic_or_trap)}].",
                                   "green"))
        if int(user_input) in range(1, len(opponents_magic_or_trap) + 1):
            return opponents_magic_or_trap[int(user_input) - 1]
        else:
            print(colored("Invalid index, please try again!", "red"))

    def get_all_monsters_on_field(self):
        """Returns a list of all the monsters on the field, of both players."""
        return self.get_current_players_monsters() + self.get_opposing_players_monsters()

    def change_position(self, monster):
        """Changes the position of a monster. (Not to be used when summoning monsters.) Receives a monster object and
        returns nothing.
        """
        desired_position = input(colored("What position would you like the monster in?\n"
                                         "'a' : attack\n"
                                         "'d' : defense\n", "green"))
        if desired_position == "a":
            monster.position = "ATK"
        elif desired_position == "d":
            monster.position = "DEF"
        else:
            print(colored("Invalid input. Please try again!", "red"))

    def summon_position(self, monster):
        """Sets the position of a monster being summoned according to user input, includes to option to set face down,
        which is not allowed in any other case. Receives monster object. Returns nothing.
        """
        desired_position = input(colored("What position would you like the monster in?\n"
                                         "'a' : attack\n"
                                         "'d' : defense\n"
                                         "'f' : face down defense\n", "green"))
        if desired_position == "a":
            monster.position = "ATK"
        elif desired_position == "d":
            monster.position = "DEF"
        elif desired_position == "f":
            monster.position = "FD"
        else:
            print(colored("Invalid input. Please try again!", "red"))

    def activate_flip_effect(self, flip_monster):
        """Activates the effect of a flip effect monster. Receives a flip effect monster and returns nothing."""
        card_effect_function = self.card_effects[flip_monster.name]
        # Display message to user that a flip effect has been activated, then call the corresponding flip effect
        print(f"{flip_monster} revealed as face down monster! Effect initiated! {card_effect_function.__doc__}")
        card_effect_function(self)

    def next_turn(self):
        """Prepare for next player's turn, changing current player, opposing player, incrementing turn count, resetting
        player's ability to summon a monster for their next turn, setting all monsters attacked_this_turn and
        sent_to_grave_this_turn attributes to False.
        """
        self.turn_count += 1
        self.current_player.summoned_monster_this_turn = False
        self.current_player.monster_sent_to_gy_this_turn = False
        self.all_monsters_attacked_to_false()
        self.all_monster_sent_grave_to_false()
        self.all_monsters_changed_pos_to_false()
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
        keystrokes, updating game phase as turns unfold.
        """
        self.start_game()

        # Main loop to run game.
        while True:
            # Draw phase
            self.phase = "DRAW PHASE"
            self.draw_phase()

            # Main Phase
            self.phase = "MAIN PHASE 1"
            self.main_phase()

            # Battle Phase
            self.phase = "BATTLE PHASE"
            self.battle_phase()

            # Main Phase 2
            self.phase = "MAIN PHASE 2"
            self.main_phase()

            # Update game state and then check for win, display and break main game loop if game over
            self.update_game_state()
            if self.game_state != "In Progress...":
                print(self.game_state)
                break

            # End Phase
            self.phase = "END PHASE"
            self.end_phase()

            # Get ready for the opposite player's turn
            self.next_turn()


if __name__ == "__main__":
    game = Game()
    game.play_game()

