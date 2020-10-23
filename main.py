from Classes.game import Person, bcolors
from Classes.magic import Spell
from Classes.inventory import Item
import random

# create black magic (objects from class Spell
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# create white magic (objects from class Spell)
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# create items
potion = Item("Potion", "potion", "heals 50 HP", 50)
hi_potion = Item("Hi-Potion", "potion", "heals 100 HP", 100)
super_potion = Item("Super-Potion", "potion", "heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP and MP of one party member", 9999)
mega_elixir = Item("Mega-Elixir", "elixir", "Fully restores party's HP and MP", 9999)
grenade = Item("Grenade", "attack", "Deals 200 damage", 200)

items = {}

# characters instantiation
player1 = Person("Valos", 3200, 160, 1500, 34, [fire, thunder, blizzard, meteor, quake, cure, cura], items)
player2 = Person("Nick ", 4100, 145, 1330, 34, [fire, thunder, blizzard, meteor, quake, cure, cura], items)
player3 = Person("Robot", 3000, 150, 1460, 34, [fire, thunder, blizzard, meteor, quake, cure, cura], items)
enemy1 = Person("Imp  ", 1250, 130, 300, 25, [], [])
enemy2 = Person("Grogr", 10000, 700, 500, 25, [], [])
enemy3 = Person("Imp  ", 1250, 130, 300, 25, [], [])

player1.items = [{"item": potion, "quantity": 5}, {"item": hi_potion, "quantity": 5},
                 {"item": super_potion, "quantity": 5}, {"item": elixir, "quantity": 5},
                 {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]
player2.items = [{"item": potion, "quantity": 5}, {"item": hi_potion, "quantity": 5},
                 {"item": super_potion, "quantity": 5}, {"item": elixir, "quantity": 5},
                 {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]
player3.items = [{"item": potion, "quantity": 5}, {"item": hi_potion, "quantity": 5},
                 {"item": super_potion, "quantity": 5}, {"item": elixir, "quantity": 5},
                 {"item": mega_elixir, "quantity": 2}, {"item": grenade, "quantity": 5}]

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
print(bcolors.FAIL + bcolors.BOLD + "An enemy attacks!" + bcolors.ENDC)

# battle
while running:
    print("\n")
    print("=======================================================================")
    print(bcolors.BOLD + "NAME                HP                                      MP" + bcolors.ENDC)

    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose the action: ")
        index = int(choice) - 1

# player attacks
        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print(player.name.replace(" ", "") + " attacked "
                  + enemies[enemy].name.replace(" ", "") + " for", dmg, "damage.")
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]                                      # OBAVEZNO PROUČI !!!!!!!

# player chooses a spell
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose your spell: ")) - 1
            if magic_choice == -1:
                continue
            chosen_spell = player.magic[magic_choice]                          # magic je niz objekata
            magic_dmg = chosen_spell.generate_damage()
            current_mp = player.get_mp()
            if chosen_spell.cost > current_mp:
                print(bcolors.FAIL + "Not enough MP" + bcolors.ENDC)
                continue
            player.reduce_mp(chosen_spell.cost)
            if chosen_spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + player.name, " healed for " + str(magic_dmg) + " points.", bcolors.ENDC)

            elif chosen_spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + player.name, "cast a spell on " + enemies[enemy].name.replace(" ", "")
                      + "for", magic_dmg, "damage.", bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace + " has died.")
                    del enemies[enemy]

# player chooses an item
        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose your item: ")) - 1
            if item_choice == -1:
                continue
            chosen_item = player.items[item_choice]["item"]                     # ################
            item_quantity = player.items[item_choice]["quantity"]               # ###############
            item_dmg = chosen_item.generate_damage()
            if item_quantity == 0:
                print(player.name, "doesn't have anymore of that item left.")
                continue
            if chosen_item.type == "potion":
                player.heal(item_dmg)
                print(bcolors.WARNING + player.name, "used a", chosen_item.name,
                      "and healed for", item_dmg, "points.", bcolors.ENDC)
            elif chosen_item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(item_dmg)
                print(bcolors.WARNING + player.name, "used a", chosen_item.name,
                      "and dealt", item_dmg, "damage to" + enemies[enemy].name + ".", bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
            elif chosen_item.type == "elixir":
                if chosen_item.name == "Elixir":
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.WARNING + player.name, "used a", chosen_item.name,
                          "and fully restored his HP and MP", bcolors.ENDC)
                elif chosen_item.name == "Mega-Elixir":
                    for guy in players:
                        guy.hp = guy.maxhp
                        guy.mp = guy.maxmp
                    print(bcolors.WARNING + player.name, "used a", chosen_item.name,
                          "and fully restored party's HP and MP", bcolors.ENDC)

            player.items[item_choice]["quantity"] -= 1

        defeated_enemies = 0
        for enemy in enemies:
            if enemy.get_hp() == 0:
                defeated_enemies += 1

        if defeated_enemies == 3:
            print(bcolors.OKGREEN + "You defeated the enemies!" + bcolors.ENDC)
            running = False
            continue

    if not running:
        continue

# enemy attacks
    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemies[0].generate_dmg()
    players[target].take_dmg(enemy_dmg)
    print("Enemy attacked " + players[target].name + " for", enemy_dmg, "damage.")

    defeated_players = 0
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_players == 3:
        print(bcolors.FAIL + "You have been defeated!" + bcolors.ENDC)
        running = False
        continue
