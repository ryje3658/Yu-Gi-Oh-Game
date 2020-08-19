from game_objects import *


# Card effects for individual cards- each effect is unique and manipulates the game/board/cards in different ways.
def monster_reborn_eff(game):
    """Choose a monster from either player's graveyard and special summon it to the field."""
    monster_to_revive = game.choose_monster_from_both_graveyards()
    monster_position = input("Please type 'a' to revive the monster in attack position or 'd' for defense position.")
    if monster_position == 'a':
        monster_to_revive.position = "ATK"
    elif monster_position == 'd':
        monster_to_revive.position = "DEF"
    else:
        print(colored("Incorrect input, reviving monster in the position it was destroyed in.", "red"))
        pass
    game.place_in_open_monster_spot(monster_to_revive)


def the_wicked_worm_beast_eff(game):
    pass


def lord_of_d_eff(game):
    pass


def mysterious_puppeteer_eff(game):
    pass


def trap_master_eff(game):
    pass


def hane_hane_eff(game):
    pass


def dark_energy_eff(game):
    pass


def invigoration_eff(game):
    pass


def dark_hole_eff(game):
    """Dark hole card destroys all monster on the field."""
    monsters_to_destroy = [x for x in [game.board.p1_monster_1, game.board.p1_monster_2, game.board.p1_monster_3,
                           game.board.p1_monster_4, game.board.p1_monster_5, game.board.p2_monster_1,
                           game.board.p2_monster_2, game.board.p2_monster_3, game.board.p2_monster_4,
                           game.board.p2_monster_5] if isinstance(x, Monster)]
    # for i in vars(game.board):
    #     # Find monster to be removed
    #     if vars(game.board)[i] == monster:
    #         # Set that board's spot to the empty placeholder, removing monster from the board
    #         vars(game.board)[i] = game.board.empty_placeholder
    #         # Set monster as sent to graveyard this turn
    #         monster.sent_to_grave_this_turn = True
    #         # Send monster to the correct graveyard
    #         if player_indicator_num == 0:
    #             game.current_player.graveyard.append(monster)
    #             print(colored(f"{monster} sent to {game.current_player}'s graveyard.\n", "red"))
    #         else:
    #             game.opposing_player.graveyard.append(monster)
    #             print(colored(f"{monster} sent to {game.opposing_player}'s graveyard.\n", "red"))


def oozaki_eff(game):
    """Oozaki card inflicts 800 points of direct damage to opponent's life points."""
    game.opposing_player.life_points -= 800


def fissure_eff(game):
    pass


def trap_hole_eff(game):
    pass


def two_pronged_attack_eff(game):
    pass


def de_spell_eff(game):
    pass


def inexperienced_spy_eff(game):
    pass


def reinforcements_eff(game):
    pass


def ancient_telescope_eff(game):
    """Ancient telescope card allows you to see the top 5 cards or your opponent's deck."""
    top_5_cards = game.opposing_player.player_deck.card_list[-5:]
    top_5_correct_order = top_5_cards[::-1]
    print(f"{game.opposing_player}'s top 5 cards: {top_5_correct_order}")


def just_desserts_eff(game):
    """Inflicts 500 points of direct damage for each monster your opponent controls."""

    # Generate list of opponents monster
    opponents_monsters = game.get_opposing_players_monsters()

    # Take length of list, multiple by 500, inflict damage to opponent equal to the product
    opponents_monster_count = len(opponents_monsters)
    damage_to_life_points = 500 * opponents_monster_count
    game.opposing_player.life_points -= damage_to_life_points


def remove_trap_eff(game):
    pass


def sogen_eff(game):
    pass


def flute_of_summoning_dragon_eff(game):
    pass


def ultimate_offering_eff(game):
    pass


def castle_walls_eff(game):
    """Increases a monster's defense by 500 points for one turn."""

    pass


def reverse_trap_eff(game):
    pass


def man_eater_bug_eff(game):
    pass


def the_stern_mystic_eff(game):
    pass


def wall_of_illusion_eff(game):
    pass


def sword_of_dark_destruction_eff(game):
    pass


def book_of_secret_arts_eff(game):
    pass


def dian_keto_the_cure_master_eff(game):
    """Dian Keto card increases player's life points by 1000."""
    game.current_player.life_points += 1000


def change_of_heart_eff(game):
    """Choose an opponent's monster to take control of."""
    # Get target Monster
    target_monster = game.choose_opponent_monster()

    # Remove monster from opponents side of the field

    # Place monster on current players side of the field
    game.place_in_open_monster_spot(target_monster)


def soul_exchange_eff(game):
    pass


def last_will_eff(game):
    pass


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


def yami_eff(game):
    pass


def dragon_capture_jar_eff(game):
    pass


def waboku_eff(game):
    """You take no battle damage and any monsters destroyed in battle are revived after battle phase."""
    # Negate any damage taken this turn in battle
    game.current_player.damage_taken_this_turn += game.current_player.life_points
    for card in game.get_current_player_graveyard():
        if isinstance(card, Monster):
            if card.sent_to_grave_this_turn:
                # Special summon monsters
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
trap_master = Monster("Trap Master", "TrapMaster", True, 500, 1100, 3, "Warrior", "Earth")
hane_hane = Monster("Hane-Hane", "Hane-Hane ", True, 450, 500, 2, "Beast", "Earth")

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
stern_mystic = Monster("The Stern Mystic", "St. Mystic", True, 1500, 1200, 4, "Spellcaster", "Light")
wall_of_illusion = Monster("Wall of Illusion", "W. Illusion", True, 1000, 1850, 4, "Fiend", "Dark")
neo = Monster("Neo the Magic Swordsman", "Neo Sword ", None, 1700, 1000, 4, "Spellcaster", "Light")
baron = Monster("Baron of the Fiend Sword", "BaronFiend", None, 1550, 800, 4, "Fiend", "Dark")
man_eating = Monster("Man-Eating Treasure Chest", "Man-Eating", None, 1600, 1000, 4, "Fiend", "Dark")
sorcerer = Monster("Sorcerer of the Doomed", " Sorcerer ", None, 1450, 1200, 4, "Spellcaster", "Dark")
trap_master2 = Monster("Trap Master", "TrapMaster", True, 500, 1100, 3, "Warrior", "Earth")
man_eater = Monster("Man-Eater Bug", "Man-Eater B", True, 450, 600, 2, "Insect", "Earth")

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