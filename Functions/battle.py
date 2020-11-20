from Classes.game import bcolors
import random


def print_header():
    print("\n")
    print("=======================================================================")
    print(bcolors.BOLD + "NAME                HP                                      MP" + bcolors.ENDC)
    return

# PLAYER PHASE #


# MAIN BATTLE LOOP
def action_choice_recursive(player, players, enemies):  # U OVO SE SVE EVENTUALNO VRAĆA, PRIMARNA TOČKA
    index = player.choose_action()

    # PLAYER ATTACKS
    if index == 0:
        enemy = attack(player, enemies)
        return enemy, None, None, index

    # PLAYER CASTS A SPELL
    elif index == 1:
        enemy, chosen_spell, spell_bool = spell_cast(player, enemies)
        if spell_bool:
            return action_choice_recursive(player, players, enemies)
        else:
            return enemy, chosen_spell, None, index

    # PLAYER USES AN ITEM
    elif index == 2:
        enemy, chosen_item, item_bool = use_item(player, players, enemies)
        if item_bool:
            return action_choice_recursive(player, players, enemies)
        else:
            return enemy, None, chosen_item, index
    elif index == 3:
        pass
        return None, None, None, index


# PLAYER ATTACKS
def attack(player, enemies):
    dmg = player.generate_dmg()
    enemy = player.choose_target(enemies)
    enemies[enemy].take_dmg(dmg)
    print(player.name.replace(" ", "") + " attacked "
          + enemies[enemy].name.replace(" ", "") + " for", dmg, "damage.")
    if enemies[enemy].get_hp() == 0:
        print(enemies[enemy].name.replace(" ", "") + " has died.")
    return enemy


# PLAYER CASTS A SPELL
def spell_cast(player, enemies):
    enemy = None
    magic_choice, index = player.choose_magic()
    if magic_choice == index:
        return enemy, magic_choice, True
    else:
        chosen_spell = player.magic[magic_choice]  # magic je niz objekata
        magic_dmg = chosen_spell.generate_damage()
        current_mp = player.get_mp()
        if chosen_spell.cost > current_mp:
            print(bcolors.FAIL + "Not enough MP" + bcolors.ENDC)
            return spell_cast(player, enemies)
        player.reduce_mp(chosen_spell.cost)
        if chosen_spell.type == "white":
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + player.name.replace(" ", ""),
                  "healed for " + str(magic_dmg) + " points.", bcolors.ENDC)
        elif chosen_spell.type == "black":
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(magic_dmg)
            print(bcolors.OKBLUE + player.name, "cast a spell on " + enemies[enemy].name.replace(" ", ""),
                  "for", magic_dmg, "damage.", bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]
        return enemy, chosen_spell, False


# PLAYER USES AN ITEM
def use_item(player, players, enemies):
    enemy = None
    item_choice, index = player.choose_item()
    if item_choice == index:
        return enemy, item_choice, True
    else:
        chosen_item = player.items[item_choice]["item"]
        item_quantity = player.items[item_choice]["quantity"]
        item_dmg = chosen_item.generate_damage()
        if item_quantity == 0:
            print(player.name, "doesn't have anymore of that item left.")
            return use_item(player, players, enemies)
        if chosen_item.type == "potion":
            player.heal(item_dmg)
            print(bcolors.WARNING + player.name.replace(" ", ""), "used a", chosen_item.name,
                  "and healed for", item_dmg, "points.", bcolors.ENDC)
        elif chosen_item.type == "attack":
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(item_dmg)
            print(bcolors.WARNING + player.name.replace(" ", ""), "used a", chosen_item.name,
                  "and dealt", item_dmg, "damage to", enemies[enemy].name.replace(" ", "") + ".", bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
        elif chosen_item.type == "elixir":
            if chosen_item.name == "Elixir":
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.WARNING + player.name.replace(" ", ""), "used a", chosen_item.name,
                      "and fully restored his HP and MP", bcolors.ENDC)
            elif chosen_item.name == "Mega-Elixir":
                for guy in players:
                    guy.hp = guy.maxhp
                    guy.mp = guy.maxmp
                print(bcolors.WARNING + player.name.replace(" ", ""), "used a", chosen_item.name,
                      "and fully restored party's HP and MP", bcolors.ENDC)

        player.items[item_choice]["quantity"] -= 1
        return enemy, chosen_item, False


# ENEMY PHASE #
def enemy_phase(enemy, players):
    if enemy.min_required_mana() > enemy.get_mp():
        enemy_choice = 0
    else:
        enemy_choice = random.randrange(0, 3)
# ENEMY ATTACKS
    target = random.randrange(0, len(players))
    if enemy_choice < 2:
        enemy_dmg = enemy.generate_dmg()
        players[target].take_dmg(enemy_dmg)
        print(enemy.name.replace(" ", "") + " attacked "
              + players[target].name.replace(" ", "") + " for", enemy_dmg, "damage.")
# ENEMY CASTS A SPELL
    elif enemy_choice == 2:
        chosen_spell, magic_dmg = enemy.choose_enemy_spell()
        enemy.reduce_mp(chosen_spell.cost)
        if chosen_spell.type == "white":
            enemy.heal(magic_dmg)
            print(bcolors.OKBLUE + enemy.name.replace(" ", ""),
                  "healed for " + str(magic_dmg) + " points.", bcolors.ENDC)
        elif chosen_spell.type == "black":
            players[target].take_dmg(magic_dmg)
            print(bcolors.OKBLUE + enemy.name.replace(" ", ""), "cast a spell on "
                  + players[target].name.replace(" ", "") + " for", magic_dmg, "damage.", bcolors.ENDC)
    return target
