from game_objects import *


# Individual card effects stored in functions below in form: {card_name}_eff().
def monster_reborn_eff():
    pass


def wicked_worm_eff():
    pass


def lord_of_d_eff():
    pass


def mysterious_puppeteer_eff():
    pass


def trap_master_eff():
    pass


def hane_hane_eff():
    pass


def dark_energy_eff():
    pass


def invigoration_eff():
    pass


def dark_hole_eff():
    pass


def oozaki_eff():
    # """Opponent loses 800 life points."""
    # target_game.opposing_player.life_points -= 800
    pass

def fissure_eff():
    pass


def trap_hole_eff():
    pass


def two_pronged_attack_eff():
    pass


def despell_eff():
    pass


def inexperienced_spy_eff():
    pass


def reinforcements_eff():
    pass


def ancient_telescope_eff():
    pass


def just_desserts_eff():
    pass


def remove_trap_eff():
    pass


def sogen_eff():
    pass


def flute_eff():
    pass


def ultimate_offering_eff():
    pass


def castle_wall_eff():
    pass


def reverse_trap_eff():
    pass


def man_eater_bug_eff():
    pass


def stern_mystic_eff():
    pass


def wall_of_illusion_eff():
    pass


def sword_of_dark_destruction_eff():
    pass


def book_of_secret_arts_eff():
    pass


def dian_keto_eff():
    pass


def change_of_heart_eff():
    pass


def soul_exchange_eff():
    pass


def last_will_eff():
    pass


def card_destruction_eff():
    pass


def yami_eff():
    pass


def dragon_capture_jar_eff():
    pass


def waboku_eff():
    pass


# Kaiba Starter Deck Monster Cards
blue_eyes = Monster("Blue-Eyes White Dragon", "Blue-Eyes ", None, 3000, 2500, 8, "Dragon", "Light")
hitotsu = Monster("Hitotsu-Me Giant", "Hitotsu-Me", None, 1200, 1000, 4, "Beast-Warrior", "Earth")
ryu_kishin = Monster("Ryu-Kishin", "Ryu-Kishin", None, 1200, 1000, 4, "Beast-Warrior", "Earth")
wicked_worm = Monster("The Wicked Worm Beast", "WickedWorm", wicked_worm_eff, 1500, 700, 3, "Beast", "Earth")
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
lord_of_d = Monster("Lord of D.", "Lord of D.", lord_of_d_eff, 1200, 1100, 4, "Spellcaster", "Dark")
myst_pup = Monster("Mysterious Puppeteer", "mPuppeteer", mysterious_puppeteer_eff, 1000, 1500, 4, "Warrior", "Earth")
trap_master = Monster("Trap Master", "TrapMaster", trap_master_eff, 500, 1100, 3, "Warrior", "Earth")
hane_hane = Monster("Hane-Hane", "Hane-Hane ", hane_hane_eff, 450, 500, 2, "Beast", "Earth")

# Kaiba Starter Deck Magic Cards
monster_reborn = Magic("Monster Reborn", "M. Reborn ", monster_reborn_eff)
remove_trap = Magic("Remove Trap", "RemoveTrap", remove_trap_eff)
sogen = Field("Sogen", "   Sogen  ", sogen_eff)
flute_of_summoning_dragon = Magic("Flute of Summoning Dragon", "Flute - SD", flute_eff)
ancient_telescope = Magic("Ancient Telescope", " Telescope", ancient_telescope_eff)
inexperienced_spy = Magic("Inexperienced Spy", "Inexpd Spy", inexperienced_spy_eff)
de_spell = Magic("De-Spell", " De-Spell ", despell_eff)
fissure = Magic("Fissure", " Fissure  ", fissure_eff)
oozaki = Magic("Oozaki", " Oozaki  ", oozaki_eff)
dark_hole = Magic("Dark Hole", "Dark Hole ", dark_hole_eff)
invigoration = Equip("Invigoration", "Invigorate", invigoration_eff)
dark_energy = Equip("Dark Energy", "DarkEnergy", dark_energy_eff)

# Kaiba Starter Deck Trap Cards
ultimate_offering = Trap("Ultimate Offering", "U.Offering", ultimate_offering_eff, "Continuous")
castle_walls = Trap("Castle Walls", "CastleWall", castle_wall_eff, "Normal")
reverse_trap = Trap("Reverse Trap", "Rev. Trap ", reverse_trap_eff, "Normal")
just_desserts = Trap("Just Desserts", "J.Desserts", just_desserts_eff, "Normal")
reinforcements = Equip("Reinforcements", "Reinforce ", reinforcements_eff)
two_pronged_attack = Trap("Two-Pronged Attack", "2P- Attack", two_pronged_attack_eff, "Normal")
trap_hole = Trap("Trap Hole", "Trap Hole ", trap_hole_eff, "Quick")

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
stern_mystic = Monster("The Stern Mystic", "St. Mystic", stern_mystic_eff, 1500, 1200, 4, "Spellcaster", "Light")
wall_of_illusion = Monster("Wall of Illusion", "W. Illusion", wall_of_illusion_eff, 1000, 1850, 4, "Fiend", "Dark")
neo = Monster("Neo the Magic Swordsman", "Neo Sword ", None, 1700, 1000, 4, "Spellcaster", "Light")
baron = Monster("Baron of the Fiend Sword", "BaronFiend", None, 1550, 800, 4, "Fiend", "Dark")
man_eating = Monster("Man-Eating Treasure Chest", "Man-Eating", None, 1600, 1000, 4, "Fiend", "Dark")
sorcerer = Monster("Sorcerer of the Doomed", " Sorcerer ", None, 1450, 1200, 4, "Spellcaster", "Dark")
trap_master2 = Monster("Trap Master", "TrapMaster", trap_master_eff, 500, 1100, 3, "Warrior", "Earth")
man_eater = Monster("Man-Eater Bug", "Man-Eater B", man_eater_bug_eff, 450, 600, 2, "Insect", "Earth")

# Yugi Starter Deck Magic Cards
monster_reborn2 = Magic("Monster Reborn", "M. Reborn ", monster_reborn_eff)
remove_trap2 = Magic("Remove Trap", "RemoveTrap", remove_trap_eff)
de_spell2 = Magic("De-Spell", " De-Spell ", despell_eff)
fissure2 = Magic("Fissure", " Fissure  ", fissure_eff)
dark_hole2 = Magic("Dark Hole", "Dark Hole ", dark_hole_eff)
sword_of_dark = Equip("Sword of Dark Destruction", "Dark Sword", sword_of_dark_destruction_eff)
book_of_arts = Equip("Book of Secret Arts", "Secret Arts", book_of_secret_arts_eff)
dian_keto = Magic("Dian Keto the Cure Master", "Dian Keto ", dian_keto_eff)
change_of_heart = Magic("Change of Heart", "Chng Heart", change_of_heart_eff)
last_will = Magic("Last Will", "Last Will ", last_will_eff)
soul_ex = Magic("Soul Exchange", "Soul Exchg", soul_exchange_eff)
card_destruction = Magic("Card Destruction", "Card Destr", card_destruction_eff)
yami = Field("Yami", "   Yami   ", yami_eff)

# Yugi Starter Deck Trap Cards
ultimate_offering2 = Trap("Ultimate Offering", "U.Offering", ultimate_offering_eff, "Continuous")
castle_walls2 = Trap("Castle Walls", "CastleWall", castle_wall_eff, "Normal")
reverse_trap2 = Trap("Reverse Trap", "Rev. Trap ", reverse_trap_eff, "Normal")
reinforcements2 = Equip("Reinforcements", "Reinforce ", reinforcements_eff)
two_pronged_attack2 = Trap("Two-Pronged Attack", "2P- Attack", two_pronged_attack_eff, "Normal")
trap_hole2 = Trap("Trap Hole", "Trap Hole ", trap_hole_eff, "Quick")
dragon_capture_jar = Trap("Dragon Capture Jar", "D Capt Jar", dragon_capture_jar_eff, "Normal")
waboku = Trap("Waboku", "  Waboku  ", waboku_eff, "Normal")

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
                   trap_master2, dragon_capture_jar, yami, man_eater, remove_trap2, remove_trap2, castle_walls2,
                   ultimate_offering2])