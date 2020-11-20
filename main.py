from Classes.game import bcolors
from Functions.init_and_equip_players import init_characters
from Functions.battle import action_choice_recursive, enemy_phase, print_header

players, enemies = init_characters()
running = True
print(bcolors.FAIL + bcolors.BOLD + "\nAn enemy attacks!" + bcolors.ENDC)
defeated_enemies = 0
defeated_players = 0

while running:
    print_header()
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()
    for player in players:
        if not running:
            continue
# PLAYER PHASE
        enemy, chosen_spell, chosen_item, index = action_choice_recursive(player, players, enemies)
        if index == 0 or index == 1 and chosen_spell.type == "dark" or index == 2 and chosen_item.type == "attack":
            if enemies[enemy].get_hp() == 0:
                del enemies[enemy]
                defeated_enemies += 1
                print("Defeated enemies:", defeated_enemies)
        if defeated_enemies == 3:
            print(bcolors.OKGREEN + "You defeated the enemies!" + bcolors.ENDC)
            running = False
# ENEMY PHASE
    print("\n")
    for enemy in enemies:
        if not running:
            continue
        target = enemy_phase(enemy, players)
        if players[target].get_hp() == 0:
            print(players[target].name.replace(" ", "") + " has died.")
        if players[target].get_hp() == 0:
            del players[target]
            defeated_players += 1
        if defeated_players == 3:
            print(bcolors.FAIL + "You have been defeated!" + bcolors.ENDC)
            running = False
