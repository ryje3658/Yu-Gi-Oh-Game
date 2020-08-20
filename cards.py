from game_objects import *


# Card effects for individual cards- each effect is unique and manipulates the game/board/cards in different ways.
# Functions return True when they successfully resolve, or False when they fail to resolve. Unique error messages
# accompany each function to give player specific feedback of the conditions they failed to meet.
def monster_reborn_eff(game):
    """Choose a monster from either player's graveyard and special summon it to the field."""
    # Check that there is at least one monster in either graveyard
    both_graveyards = game.get_current_player_graveyard() + game.get_opposing_player_graveyard()
    both_graveyards = [x for x in both_graveyards if isinstance(x, Monster)]
    if len(both_graveyards) > 0:
        monster_to_revive = game.choose_monster_from_both_graveyards()
        game.change_position(monster_to_revive)
        game.place_in_open_monster_spot(monster_to_revive)
        return True
    else:
        print(colored("There are no monsters in either player's graveyard!", "red"))
        return False


def dark_energy_eff(game):
    """Target one face up fiend monster on the field. It gains 300 attack and 300 defense."""
    # Checks that there is at least one fiend monster.
    for monster in game.get_current_players_monsters():
        if monster.monster_type == "Fiend":
            # Loops asking for input, until user chooses a Fiend monster to increase attack/defense of
            while True:
                print(colored("Choose a Fiend monster to gain 300 attack and 300 defense.", "green"))
                monster = game.choose_current_monster()
                if monster.monster_type == "Fiend":
                    monster.attack += 300
                    monster.defense += 300
                    print(f"{monster}'s attack increased from {monster.attack-300} to {monster.attack}!\n"
                          f"{monster}'s defense increased from {monster.defense-300} to {monster.defense}!")
                    return True
                else:
                    print(colored("Must choose a Fiend type monster!", "red"))
    else:
        print(colored("Card effect could not be activated! You have no fiend monsters on the field!", "red"))
        return False


def invigoration_eff(game):
    """Target one face up earth monster on the field. It gains 400 attack and loses 200 defense."""
    # Checks that there is at least one earth monster.
    for monster in game.get_current_players_monsters():
        if monster.attribute == "Earth":
            # Loops asking for input, until user chooses a Earth monster to increase attack/defense of
            while True:
                print(colored("Choose an Earth monster to gain 400 attack and lose 200 defense.", "green"))
                monster = game.choose_current_monster()
                if monster.attribute == "Earth":
                    monster.attack += 400
                    monster.defense -= 200
                    print(f"{monster}'s attack increased from {monster.attack - 400} to {monster.attack}!\n"
                          f"{monster}'s defense decreased from {monster.defense} to {monster.defense - 200}!")
                    return True
                else:
                    print(colored("Must choose an Earth type monster!", "red"))
    else:
        print(colored("Card effect could not be activated! You have no Earth monsters on the field!", "red"))
        return False


def dark_hole_eff(game):
    """Sends all monster on the field to their respective graveyards."""
    for monster in game.get_all_monsters_on_field():
        game.send_monster_field_to_graveyard(monster)
    return True


def oozaki_eff(game):
    """Inflicts 800 points of direct damage to opponent's life points."""
    game.opposing_player.life_points -= 800
    print(f"{game.opposing_player} lost 800 life points!")
    return True


def fissure_eff(game):
    """Destroys opponent's monster with the lowest attack power."""
    opponents_face_up_monsters = [x for x in game.get_opposing_players_monsters() if x.position != "FD"]
    if len(opponents_face_up_monsters) > 0:
        weakest_monster = min(opponents_face_up_monsters, key=lambda x: x.attack)
        game.send_monster_field_to_graveyard(weakest_monster)
        return True
    else:
        print(colored("Can't activate card effect! Opponent has no monsters on the field!", "red"))
        return False


def trap_hole_eff(game):
    """Target one opponent your monster controls with >= 1000 attack and destroy that monster."""
    for monster in game.get_opposing_players_monsters():
        if monster.attack >= 1000:
            # Loops asking for input, until user chooses a monster with >= 1000 attack to destroy
            while True:
                print(colored("Choose a monster with 1000 attack or more to destroy.", "green"))
                monster = game.choose_opponent_monster()
                if monster.attack >= 1000:
                    game.send_monster_field_to_graveyard(monster)
                    print(f"{monster} sent to graveyard!")
                    return True
                else:
                    print(colored("Must choose a monster with 1000 attack or more to destroy!", "red"))
    else:
        print(colored("Card effect could not be activated! Opponent has no monsters with at least 1000 attack!", "red"))
        return False


def two_pronged_attack_eff(game):
    """Select and destroy 2 of your monsters and 1 of your opponent's monsters."""
    # Check for current player having 2+ monsters and opponent having 1+ monster(s)
    if len(game.get_current_players_monsters()) > 1 and len(game.get_opposing_players_monsters()) > 0:
        # Choose monsters to sacrifice and send to graveyard
        print(colored("Choose two of your own monsters to sacrifice...", "green"))
        game.send_monster_field_to_graveyard(game.choose_current_monster())
        game.send_monster_field_to_graveyard(game.choose_current_monster())

        # Choose opponent's monster to destroy and send to graveyard
        print(colored("Choose one of your opponents monsters to destroy...", "green"))
        game.send_monster_field_to_graveyard(game.choose_opponent_monster())
        return True
    else:
        print(colored("Can't activate card effect at this time. Not enough monsters on the field.", "red"))
        return False


def de_spell_eff(game):
    """Target one magic card on the field. Destroy it."""
    opponents_spells = game.get_opponents_magic_trap()
    for magic_or_trap in opponents_spells:
        if isinstance(magic_or_trap, Magic):
            while True:
                print(colored("Choose a magic card to destroy.", "green"))
                card = game.choose_opponent_magic_or_trap()
                if isinstance(card, Magic):
                    game.send_magic_field_to_graveyard(card)
                    print(f"{card} sent to graveyard!")
                    return True
                else:
                    print(colored("Must choose a magic card to destroy!", "red"))
        else:
            print(colored("Card effect could not be activated! Opponent has no magic cards.", "red"))
            return False


def inexperienced_spy_eff(game):
    """Select and see 1 card in your opponent's hand."""
    hand_len = len(game.opposing_player.hand)
    if hand_len > 0:
        card_num = input(colored(f"Please choose a number in range [1-{hand_len}].", "green"))
        print(f"The card you chose to see is: {game.opposing_player.hand[int(card_num)-1]}")
        return True
    else:
        print(colored("Your opponent has no cards in their hand!", "red"))
        return False


def reinforcements_eff(game):
    """Target one face up monster on the field. It gains 500 attack."""
    if len(game.get_current_players_monsters()) > 0:
        print(colored("Choose a monster to gain 500 attack.", "green"))
        monster = game.choose_current_monster()
        monster.attack += 500
        print(f"{monster}'s attack increased from {monster.attack-500} to {monster.attack}!")
        return True
    else:
        print(colored("Card effect could not be activated! You have no monsters on the field!", "red"))
        return False


def ancient_telescope_eff(game):
    """Allows you to see the top 5 cards or your opponent's deck."""
    top_5_cards = game.opposing_player.player_deck.card_list[-5:]
    top_5_correct_order = top_5_cards[::-1]
    print(f"{game.opposing_player}'s top 5 cards: {top_5_correct_order}")
    return True


def just_desserts_eff(game):
    """Inflicts 500 points of direct damage for each monster your opponent controls."""

    # Generate list of opponents monster
    opponents_monsters = game.get_opposing_players_monsters()

    # Take length of list, multiple by 500, inflict damage to opponent equal to the product
    opponents_monster_count = len(opponents_monsters)
    damage_to_life_points = 500 * opponents_monster_count
    game.opposing_player.life_points -= damage_to_life_points
    print(f"{game.opposing_player} lost {damage_to_life_points} life points!")
    return True


def remove_trap_eff(game):
    """Target one trap card on the field. Destroy it."""
    opponents_spells = game.get_opponents_magic_trap()
    for magic_or_trap in opponents_spells:
        if isinstance(magic_or_trap, Trap):
            while True:
                print(colored("Choose a trap card to destroy.", "green"))
                card = game.choose_opponent_magic_or_trap()
                if isinstance(card, Trap):
                    game.send_magic_field_to_graveyard(card)
                    print(f"{card} sent to graveyard!")
                    return True
                else:
                    print(colored("Must choose a trap card to destroy!", "red"))
        else:
            print(colored("Card effect could not be activated! Opponent has no trap cards.", "red"))
            return False


def sogen_eff(game):
    """All warrior and beast-warrior monsters on the field gain 200 attack and 200 defense."""
    monsters = game.get_all_monsters_on_field()
    for monster in monsters:
        if monster.monster_type == "Warrior" or monster.monster_type == "Beast-Warrior":
            monster.attack += 200
            monster.defense += 200
            print(f"{monster}'s attack and defense increased by 200!")
    return True


def flute_of_summoning_dragon_eff(game):
    """If Lord. of D. is on the field, you can summon up to two dragon monsters from your hand."""
    for monster in game.get_all_monsters_on_field():
        if monster.name == "Lord of D.":
            for card in game.current_player.hand:
                if isinstance(card, Monster) and card.monster_type == "Dragon":
                    while True:
                        print(colored("Choose a dragon to summon.", "green"))
                        card = game.choose_monster_from_hand()
                        if isinstance(card, Monster) and card.monster_type == "Dragon":
                            game.place_in_open_monster_spot(card)
                            print(f"{card} special summoned to the field!")
                            for next_card in game.current_player.hand:
                                if isinstance(next_card, Monster) and next_card.monster_type == "Dragon":
                                    user_input = input(colored("Press 'a' to summon a second dragon or 'x' to finish "
                                                               "using Flute of Summoning Dragon's effect.", "green"))
                                    if user_input == 'a':
                                        while True:
                                            print(colored("Choose a dragon to summon.", "green"))
                                            next_card = game.choose_monster_from_hand()
                                            if isinstance(next_card, Monster) and next_card.monster_type == "Dragon":
                                                game.place_in_open_monster_spot(next_card)
                                                print(f"{next_card} special summoned to the field!")
                                                break
                                            else:
                                                print(colored("Please choose a dragon to summon!", "red"))
                                    elif user_input == 'x':
                                        return True
                                    else:
                                        print(colored("Invalid input! Please try again!", "red"))
                        else:
                            print(colored("Must choose a dragon card to summon!", "red"))
            else:
                print(colored("Effect not activated! You have no dragon cards in your hand!", "red"))
                return False
        else:
            print(colored("Card effect could not be activated! Lord of D. not on field.", "red"))
            return False


def ultimate_offering_eff(game):
    """Pay 500 life points to normal summon a monster. (Does not count as your turn's normal summon.)"""
    for card in game.current_player.hand:
        if isinstance(card, Monster):
            game.current_player.life_points -= 500
            print("You've paid 500 life points. You are allowed to summon a monster.")
            monster = game.choose_monster_from_hand()
            game.change_position(monster)
            game.place_in_open_monster_spot(monster)
            return True
    print(colored("You have no monsters in your hand!", "red"))
    return False


def castle_walls_eff(game):
    """Target one face up monster on the field. It gains 500 defense."""
    if len(game.get_current_players_monsters()) > 0:
        print(colored("Choose a monster to gain 500 defense.", "green"))
        monster = game.choose_current_monster()
        monster.defense += 500
        print(f"{monster}'s defense increased from {monster.defense - 500} to {monster.defense}!")
        return True
    else:
        print(colored("Card effect could not be activated! You have no monsters on the field!", "red"))
        return False


def sword_of_dark_destruction_eff(game):
    """Target one face up Dark monster on the field. It gains 400 attack and loses 200 defense."""
    # Checks that there is at least one Dark monster.
    for monster in game.get_current_players_monsters():
        if monster.attribute == "Dark":
            # Loops asking for input, until user chooses a Dark monster to increase attack/defense of
            while True:
                print(colored("Choose an Dark monster to gain 400 attack and loses 200 defense.", "green"))
                monster = game.choose_current_monster()
                if monster.attribute == "Dark":
                    monster.attack += 400
                    monster.defense -= 200
                    print(f"{monster}'s attack increased from {monster.attack - 400} to {monster.attack}!\n"
                          f"{monster}'s defense decreased from {monster.defense} to {monster.defense - 200}!")
                    return True
                else:
                    print(colored("Must choose an Dark type monster!", "red"))
    else:
        print(colored("Card effect could not be activated! You have no Dark monsters on the field!", "red"))
        return False


def book_of_secret_arts_eff(game):
    """Target one face up Spellcaster monster on the field. It gains 300 attack and 300 defense."""
    # Checks that there is at least one Spellcaster monster.
    for monster in game.get_current_players_monsters():
        if monster.monster_type == "Spellcaster":
            # Loops asking for input, until user chooses a Spellcaster monster to increase attack/defense of
            while True:
                print(colored("Choose a Spellcaster monster to gain 300 attack and 300 defense.", "green"))
                monster = game.choose_current_monster()
                if monster.monster_type == "Spellcaster":
                    monster.attack += 300
                    monster.defense += 300
                    print(f"{monster}'s attack increased from {monster.attack - 300} to {monster.attack}!\n"
                          f"{monster}'s defense increased from {monster.defense - 300} to {monster.defense}!")
                    return True
                else:
                    print(colored("Must choose a Spellcaster type monster!", "red"))
    else:
        print(colored("Card effect could not be activated! You have no Spellcaster monsters on the field!", "red"))
        return False


def dian_keto_the_cure_master_eff(game):
    """Dian Keto card increases player's life points by 1000."""
    game.current_player.life_points += 1000
    print(f"{game.current_player} gained 1000 life points!")
    return True


def change_of_heart_eff(game):
    """Choose an opponent's monster to take control of."""
    # Check that opponent has at least 1 monster
    if len(game.get_opposing_players_monsters()) > 0:
        # Get target Monster
        target_monster = game.choose_opponent_monster()
        # Remove monster from opponents side of the field
        game.monster_to_blank_space(target_monster)
        # Place monster on current players side of the field
        game.place_in_open_monster_spot(target_monster)
        return True
    else:
        print(colored("Opponent has no monsters!", "red"))
        return False


def last_will_eff(game):
    """If a monster on your side of the field was sent to the graveyard this turn, you can special summon 1 monster
    with 1500 ATK points or less from your deck. Shuffle deck afterwards."""
    if game.current_player.monster_sent_to_gy_this_turn:
        monster_options = [x for x in game.current_player.player_deck if isinstance(x, Monster) and x.attack <= 1500]
        monster_index = input(colored(f"Please enter a number from [1-{len(monster_options)}] "
                                      f"to summon to the field.", "green"))
        monster = monster_options[int(monster_index)-1]
        game.place_in_open_monster_spot(monster)
        print(f"You chose to revive {monster}!")
        return True
    else:
        print(colored("Invalid! A monster was not sent from your side of the field to the graveyard this turn!", "red"))
        return False


def card_destruction_eff(game):
    """Sends all cards from both players' hands to their graveyards. They draw the same number they discarded."""

    # Save lengths of hands before card destruction activated
    current_player_hand_length = len(game.current_player.hand) - 1
    opposing_player_hand_length = len(game.opposing_player.hand)

    # Save card objects
    cards_in_current_hand = [card for card in game.current_player.hand]
    cards_in_opp_hand = [card for card in game.opposing_player.hand]

    # Iterate over both players cards in hand, sending each card to the graveyard
    for card in cards_in_current_hand:
        game.send_card_hand_to_graveyard(card)
    for card in cards_in_opp_hand:
        game.send_card_hand_to_graveyard(card)

    # Add cards to players' hands equivalent to the number of cards they discarded
    for i in range(current_player_hand_length):
        game.current_player.hand.append(game.current_player.player_deck.pop())
    for i in range(opposing_player_hand_length):
        game.opposing_player.hand.append(game.opposing_player.player_deck.pop())

    return True


def yami_eff(game):
    """All fiend/spellcaster monsters on the field gain 200 attack/defense. Fairy monsters lose 200 attack/defense."""
    monsters = game.get_all_monsters_on_field()
    for monster in monsters:
        if monster.monster_type == "Warrior" or monster.monster_type == "Beast-Warrior":
            monster.attack += 200
            monster.defense += 200
            print(f"{monster}'s attack and defense increased by 200!")
        elif monster.monster_type == "Fairy":
            monster.attack -= 200
            monster.defense -= 200
            print(f"{monster}'s attack and defense decreased by 200!")
    return True


def dragon_capture_jar_eff(game):
    """All face up Dragon-type monsters on the field are changed to defense position."""
    for monster in game.get_all_monsters_on_field:
        if monster.monster_type == "Dragon":
            monster.position = "DEF"
    return True


def waboku_eff(game):
    """You take no battle damage and any monsters destroyed in battle are revived after battle phase."""
    # Negate any damage taken this turn in battle
    game.current_player.damage_taken_this_turn += game.current_player.life_points
    for card in game.get_current_player_graveyard():
        if isinstance(card, Monster):
            if card.sent_to_grave_this_turn:
                # Special summon monsters
                return True


def reverse_trap_eff(game):
    pass


def soul_exchange_eff(game):
    pass


def the_wicked_worm_beast_eff(game):
    pass


def lord_of_d_eff(game):
    pass


def mysterious_puppeteer_eff(game):
    pass


def trap_master_eff(game):
    """Select one spell or trap card on the field and destroy it."""
    if len(game.get_all_magic_trap()) > 0:
        print("The owner of Trap Master can choose one magic or trap card on the field and destroy it!")
        while True:
            print(colored("Type 'f': if there is magic or trap you'd like to destroy.", "green"))
            print(colored("Type 'x': if there is no magic or trap you'd like to destroy.", "red"))
            user_input = input()
            if user_input == 'f':
                card_to_send = game.choose_from_all_magic_trap_on_field()
                game.send_magic_field_to_graveyard(card_to_send)
                return
            elif user_input == 'x':
                return
            else:
                print(colored("Invalid input, please choose a valid option!", "red"))
    else:
        print(colored("No spell or trap cards on the field to destroy. Effect not resolved!", "red"))


def hane_hane_eff(game):
    """Select one monster on the field, and return it to the owner's hand."""
    # Hane-Hane still on the field/not destroyed by battle
    if len([x for x in game.get_all_monsters_on_field() if x.name == "Hane-Hane"]) == 1:
        if len(game.get_all_monsters_on_field()) > 1:
            print("The owner of Hane-Hane can choose one monster on the field to send to the owner's hand!")
            while True:
                print(colored("Type 'f': if there is monster you'd like to send to the owner's hand.", "green"))
                print(colored("Type 'x': if there is no monster you'd like send to the owner's hand.", "red"))
                user_input = input()
                if user_input == 'f':
                    game.send_monster_field_to_hand()
                    return
                elif user_input == 'x':
                    return
                else:
                    print(colored("Invalid input, please choose a valid option!", "red"))
        # No other monsters on the field besides Hane-Hane, no targets
        else:
            print(colored("There are no possible targets. Effect could not be resolved.", "red"))
            return
    # Hane-Hane no longer on the field
    else:
        if len(game.get_all_monsters_on_field()) > 0:
            print(colored("The owner of Hane-Hane can choose one monster on the field to send to the owner's hand!"
                          , "green"))
            while True:
                print(colored("Type 'f': if there is monster you'd like to send to the owner's hand.", "green"))
                print(colored("Type 'x': if there is no monster you'd like to send to the owner's hand.", "red"))
                user_input = input()
                if user_input == 'f':
                    game.send_monster_field_to_hand()
                    return
                elif user_input == 'x':
                    return
                else:
                    print(colored("Invalid input, please choose a valid option!", "red"))
        # No other monsters on the field besides Hane-Hane, no targets
        else:
            print(colored("There are no possible targets. Effect could not be resolved.", "red"))
            return


def man_eater_bug_eff(game):
    """Destroy one monster on the field, regardless of position."""
    # Man-Eater bug still on the field/not destroyed by battle
    if len([x for x in game.get_all_monsters_on_field() if x.name == "Man-Eater Bug"]) == 1:
        if len(game.get_all_monsters_on_field()) > 1:
            print("The owner of Man-Eater Bug can choose one monster on the field to destroy!")
            while True:
                print(colored("Type 'f': if there is monster you'd like to destroy.", "green"))
                print(colored("Type 'x': if there is no monster you'd like to destroy.", "red"))
                user_input = input()
                if user_input == 'f':
                    monster_to_destroy = game.choose_from_all_monsters_on_field()
                    game.send_monster_field_to_graveyard(monster_to_destroy)
                    return
                elif user_input == 'x':
                    return
                else:
                    print(colored("Invalid input, please choose a valid option!", "red"))
        # No other monsters on the field besides Man-eater bug, no targets
        else:
            print(colored("There are no possible targets. Effect could not be resolved.", "red"))
            return
    # Man-Eater bug no longer on the field
    else:
        if len(game.get_all_monsters_on_field()) > 0:
            print(colored("The owner of Man-Eater Bug can choose one monster on the field to destroy!", "green"))
            while True:
                print(colored("Type 'f': if there is monster you'd like to destroy.", "green"))
                print(colored("Type 'x': if there is no monster you'd like to destroy.", "red"))
                user_input = input()
                if user_input == 'f':
                    monster_to_destroy = game.choose_from_all_monsters_on_field()
                    game.send_monster_field_to_graveyard(monster_to_destroy)
                    return
                elif user_input == 'x':
                    return
                else:
                    print(colored("Invalid input, please choose a valid option!", "red"))
        # No other monsters on the field besides Man-eater bug, no targets
        else:
            print(colored("There are no possible targets. Effect could not be resolved.", "red"))
            return


def the_stern_mystic_eff(game):
    """Reveal all face-down cards on the field, then return them to their original positions."""
    set_magic_trap = [x for x in game.get_all_magic_trap() if x.position == "SET"]
    face_down_monsters = [x for x in game.get_all_monsters_on_field() if x.position == "FD"]
    all_face_downs = set_magic_trap + face_down_monsters
    print("These are all of the face down cards on the field:", all_face_downs)


def wall_of_illusion_eff(game):
    pass


# Kaiba Starter Deck Monster Cards
blue_eyes = Monster("Blue-Eyes White Dragon", "Blue-Eyes ", None, 3000, 2500, 8, "Dragon", "Light")
hitotsu = Monster("Hitotsu-Me Giant", "Hitotsu-Me", None, 1200, 1000, 4, "Beast-Warrior", "Earth")
ryu_kishin = Monster("Ryu-Kishin", "Ryu-Kishin", None, 1200, 1000, 4, "Beast-Warrior", "Earth")
wicked_worm = Monster("The Wicked Worm Beast", "WickedWorm", True, 1500, 700, 3, "Beast", "Earth")
battle_ox = Monster("Battle Ox", "Battle Ox ", None, 1700, 1000, 4, "Beast-Warrior", "Earth")
koumori_dragon = Monster("Koumori Dragon", "Koumori D.", None, 1500, 1200, 4, "Dragon", "Normal")
judge_man = Monster("Judge Man", "Judge Man ", None, 2200, 1500, 6, "Warrior", "Earth")
rogue_doll = Monster("Rogue Doll", "Rogue Doll", None, 1600, 1000, 4, "Spellcaster", "Light")
kojikocy = Monster("Kojikocy", " Kojikocy ", None, 1500, 1200, 4, "Warrior", "Earth")
uraby = Monster("Uraby", "  Uraby   ", None, 1500, 800, 4, "Dinosaur", "Earth")
gyaku = Monster("Gyaukutenno Megami", "Gy. Megami", None, 1800, 2000, 6, "Fairy", "Light")
mystic_horseman = Monster("Mystic Horseman", "M. Horseman", None, 1300, 1550, 4, "Beast", "Earth")
terra = Monster("Terra the Terrible", "  Terra   ", None, 1200, 1300, 4, "Fiend", "Dark")
dark_titan = Monster("Dark Titan of Terror", "Dark Titan", None, 1300, 1100, 4, "Fiend", "Dark")
dark_assailant = Monster("Dark Assailant", "DAssailant", None, 1200, 1200, 4, "Zombie", "Dark")
master_expert = Monster("Master and Expert", "MastExpert", None, 1200, 1100, 4, "Beast", "Earth")
unknown_warrior = Monster("Unknown Warrior of Fiend", "U. Warrior", None, 1000, 500, 3, "Warrior", "Dark")
mystic_clown = Monster("Mystic Clown", "Myst Clown", None, 1500, 1000, 4, "Fiend", "Dark")
ogre_of_black = Monster("Ogre of the Black Shadow", "Ogre Black", None, 1200, 1400, 4, "Beast-Warrior", "Earth")
ryu_kishin_powered = Monster("Ryu-Kishin Powered", "RK Powered", None, 1600, 1200, 4, "Fiend", "Dark")
swordstalker = Monster("Swordstalker", "Swordstalk", None, 2000, 1600, 6, "Warrior", "Dark")
la_jinn = Monster("La Jinn the Mystical Genie of the Lamp", "  La Jinn ", None, 1800, 1000, 4, "Fiend", "Dark")
rude_kaiser = Monster("Rude Kaiser", "RudeKaiser", None, 1800, 1600, 5, "Beast-Warrior", "Earth")
destoyer_golem = Monster("Destroyer Golem", "Dest Golem", None, 1500, 1000, 4, "Rock", "Earth")
d_human = Monster("D. Human", " D. Human ", None, 1300, 1100, 4, "Warrior", "Earth")
pale_beast = Monster("Pale Beast", "Pale Beast", None, 1500, 1200, 4, "Beast", "Earth")
skull_red_bird = Monster("Skull Red Bird", "Skull Bird", None, 1550, 1200, 4, "Winged Beast", "Wind")
lord_of_d = Monster("Lord of D.", "Lord of D.", True, 1200, 1100, 4, "Spellcaster", "Dark")
myst_pup = Monster("Mysterious Puppeteer", "mPuppeteer", True, 1000, 1500, 4, "Warrior", "Earth")
trap_master = Monster("Trap Master", "TrapMaster", "Flip", 500, 1100, 3, "Warrior", "Earth")
hane_hane = Monster("Hane-Hane", "Hane-Hane ", "Flip", 450, 500, 2, "Beast", "Earth")

# Kaiba Starter Deck Magic Cards
monster_reborn = Magic("Monster Reborn", "M. Reborn ", True)
remove_trap = Magic("Remove Trap", "RemoveTrap", True)
sogen = Magic("Sogen", "   Sogen  ", True)
flute_of_summoning_dragon = Magic("Flute of Summoning Dragon", "Flute - SD", True)
ancient_telescope = Magic("Ancient Telescope", " Telescope", True)
inexperienced_spy = Magic("Inexperienced Spy", "Inexpd Spy", True)
de_spell = Magic("De-Spell", " De-Spell ", True)
fissure = Magic("Fissure", " Fissure  ", True)
oozaki = Magic("Oozaki", " Oozaki  ", True)
dark_hole = Magic("Dark Hole", "Dark Hole ", True)
invigoration = Magic("Invigoration", "Invigorate", True)
dark_energy = Magic("Dark Energy", "DarkEnergy", True)

# Kaiba Starter Deck Trap Cards
ultimate_offering = Trap("Ultimate Offering", "U.Offering", True, "Continuous")
castle_walls = Trap("Castle Walls", "CastleWall", True, "Normal")
reverse_trap = Trap("Reverse Trap", "Rev. Trap ", True, "Normal")
just_desserts = Trap("Just Desserts", "J.Desserts", True, "Normal")
reinforcements = Magic("Reinforcements", "Reinforce ", True)
two_pronged_attack = Trap("Two-Pronged Attack", "2P- Attack", True, "Normal")
trap_hole = Trap("Trap Hole", "Trap Hole ", True, "Quick")

####
####
####

# Yugi Starter Deck Monster Cards
mystical_elf = Monster("Mystical Elf", "Mystic Elf", None, 800, 2000, 4, "Spellcaster", "Light")
feral_imp = Monster("Feral Imp", "Feral Imp ", None, 1300, 1400, 4, "Fiend", "Dark")
winged_dragon = Monster("Winged Dragon", "WingDragon", None, 1400, 1200, 4, "Dragon", "Wind")
summoned_skull = Monster("Summoned Skull", "Summoned S", None, 2500, 1200, 6, "Fiend", "Dark")
beaver_warrior = Monster("Beaver Warrior", "B. Warrior", None, 1200, 1500, 4, "Beast-Warrior", "Earth")
dark_magician = Monster("Dark Magician", "D.Magician", None, 2500, 2000, 7, "Spellcaster", "Dark")
gaia = Monster("Gaia The Fierce Knight", "Gaia Knight", None, 2300, 2100, 7, "Warrior", "Earth")
curse_of_dragon = Monster("Curse of Dragon", "Curse of D", None, 2000, 1500, 5, "Dragon", "Dark")
celtic_guardian = Monster("Celtic Guardian", "C. Guardian", None, 1400, 1200, 4, "Warrior", "Earth")
mammoth_graveyard = Monster("Mammoth Graveryard", "Mammoth GY", None, 1200, 800, 4, "Dinosaur", "Earth")
great_white = Monster("Great White", "GreatWhite", None, 1600, 800, 4, "Fish", "Water")
silver_fang = Monster("Silver Fang", "Silver Fang", None, 1200, 800, 3, "Beast", "Earth")
giant_soldier = Monster("Giant Soldier of Stone", "GiantStone", None, 1300, 2000, 3, "Rock", "Earth")
dragon_zombie = Monster("Dragon Zombie", "DragZombie", None, 1600, 0, 3, "Zombie", "Dark")
doma = Monster("Doma the Angel of Silence", "Doma Angel", None, 1600, 1400, 5, "Fairy", "Dark")
ansatsu = Monster("Ansatsu", " Ansatsu  ", None, 1700, 1200, 5, "Warrior", "Earth")
witty_phantom = Monster("Witty Phantom", "W. Phantom", None, 1400, 1300, 4, "Fiend", "Dark")
claw_reacher = Monster("Claw Reacher", "Claw Reach", None, 1000, 800, 3, "Fiend", "Dark")
mystic_clown_2 = Monster("Mystic Clown", "Myst Clown", None, 1500, 1000, 4, "Fiend", "Dark")
ancient_elf = Monster("Ancient Elf", "AncientElf", None, 1450, 1200, 4, "Spellcaster", "Light")
magical_ghost = Monster("Magical Ghost", "MagicGhost", None, 1300, 1400, 4, "Zombie", "Dark")
stern_mystic = Monster("The Stern Mystic", "St. Mystic", "Flip", 1500, 1200, 4, "Spellcaster", "Light")
wall_of_illusion = Monster("Wall of Illusion", "W. Illusion", True, 1000, 1850, 4, "Fiend", "Dark")
neo = Monster("Neo the Magic Swordsman", "Neo Sword ", None, 1700, 1000, 4, "Spellcaster", "Light")
baron = Monster("Baron of the Fiend Sword", "BaronFiend", None, 1550, 800, 4, "Fiend", "Dark")
man_eating = Monster("Man-Eating Treasure Chest", "Man-Eating", None, 1600, 1000, 4, "Fiend", "Dark")
sorcerer = Monster("Sorcerer of the Doomed", " Sorcerer ", None, 1450, 1200, 4, "Spellcaster", "Dark")
trap_master2 = Monster("Trap Master", "TrapMaster", "Flip", 500, 1100, 3, "Warrior", "Earth")
man_eater = Monster("Man-Eater Bug", "Man-Eater B", "Flip", 450, 600, 2, "Insect", "Earth")

# Yugi Starter Deck Magic Cards
monster_reborn2 = Magic("Monster Reborn", "M. Reborn ", True)
remove_trap2 = Magic("Remove Trap", "RemoveTrap", True)
de_spell2 = Magic("De-Spell", " De-Spell ", True)
fissure2 = Magic("Fissure", " Fissure  ", True)
dark_hole2 = Magic("Dark Hole", "Dark Hole ", True)
sword_of_dark = Magic("Sword of Dark Destruction", "Dark Sword", True)
book_of_arts = Magic("Book of Secret Arts", "Secret Arts", True)
dian_keto = Magic("Dian Keto the Cure Master", "Dian Keto ", True)
change_of_heart = Magic("Change of Heart", "Chng Heart", True)
last_will = Magic("Last Will", "Last Will ", True)
soul_ex = Magic("Soul Exchange", "Soul Exchg", True)
card_destruction = Magic("Card Destruction", "Card Destr", True)
yami = Magic("Yami", "   Yami   ", True)

# Yugi Starter Deck Trap Cards
ultimate_offering2 = Trap("Ultimate Offering", "U.Offering", True, "Continuous")
castle_walls2 = Trap("Castle Walls", "CastleWall", True, "Normal")
reverse_trap2 = Trap("Reverse Trap", "Rev. Trap ", True, "Normal")
reinforcements2 = Magic("Reinforcements", "Reinforce ", True)
two_pronged_attack2 = Trap("Two-Pronged Attack", "2P- Attack", True, "Normal")
trap_hole2 = Trap("Trap Hole", "Trap Hole ", True, "Quick")
dragon_capture_jar = Trap("Dragon Capture Jar", "D Capt Jar", True, "Normal")
waboku = Trap("Waboku", "  Waboku  ", True, "Normal")

# Create deck with all of Kaiba's cards.
kaibas_deck = Deck([blue_eyes, hitotsu, ryu_kishin, wicked_worm, battle_ox, koumori_dragon, judge_man, rogue_doll,
                    kojikocy, uraby, gyaku, mystic_horseman, terra, dark_titan, dark_assailant, master_expert,
                    unknown_warrior, mystic_clown, ogre_of_black, dark_energy, invigoration, dark_hole, oozaki,
                    ryu_kishin_powered, swordstalker, la_jinn, rude_kaiser, destoyer_golem, skull_red_bird, d_human,
                    pale_beast, fissure, trap_hole, two_pronged_attack, de_spell, monster_reborn, inexperienced_spy,
                    reinforcements, ancient_telescope, just_desserts, lord_of_d, flute_of_summoning_dragon,
                    myst_pup, trap_master, sogen, hane_hane, reverse_trap, remove_trap, castle_walls,
                    ultimate_offering])

# Create deck with all of Yugi's cards.
yugis_deck = Deck([mystical_elf, feral_imp, winged_dragon, summoned_skull, beaver_warrior, dark_magician, gaia,
                   curse_of_dragon, celtic_guardian, mammoth_graveyard, great_white, silver_fang, giant_soldier,
                   dragon_zombie, doma, ansatsu, witty_phantom, claw_reacher, mystic_clown_2, sword_of_dark,
                   book_of_arts, dark_hole2, dian_keto, ancient_elf, magical_ghost, fissure2, trap_hole2,
                   two_pronged_attack2, de_spell2, monster_reborn2, reinforcements2, change_of_heart, stern_mystic,
                   wall_of_illusion, neo, baron, man_eating, sorcerer, last_will, waboku, soul_ex, card_destruction,
                   trap_master2, dragon_capture_jar, yami, man_eater, remove_trap2, castle_walls2,
                   ultimate_offering2])