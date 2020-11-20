from Classes.game import Person
from Functions.create_spells_and_items import create_items, create_magic

spells, enemy_spells = create_magic()
items = create_items()


# INSTANTIATE PLAYERS AND ENEMIES
def init_characters():
    player1 = Person("Valos", 20, 40, 250, spells, items)
    player2 = Person("Nick ", 20, 145, 200, spells, items)
    player3 = Person("Robot", 20, 150, 160, spells, items)
    enemy1 = Person("Imp  ", 20, 50, 200, enemy_spells, [])
    enemy2 = Person("Grogr", 20, 60, 500, enemy_spells, [])
    enemy3 = Person("Imp  ", 20, 30, 200, enemy_spells, [])

    player1.items = [{"item": items[0], "quantity": 5}, {"item": items[1], "quantity": 5},
                     {"item": items[2], "quantity": 5}, {"item": items[3], "quantity": 5},
                     {"item": items[4], "quantity": 2}, {"item": items[5], "quantity": 5}]
    player2.items = [{"item": items[0], "quantity": 5}, {"item": items[1], "quantity": 5},
                     {"item": items[2], "quantity": 5}, {"item": items[3], "quantity": 5},
                     {"item": items[4], "quantity": 2}, {"item": items[5], "quantity": 5}]
    player3.items = [{"item": items[0], "quantity": 5}, {"item": items[1], "quantity": 5},
                     {"item": items[2], "quantity": 5}, {"item": items[3], "quantity": 5},
                     {"item": items[4], "quantity": 2}, {"item": items[5], "quantity": 5}]

    players = [player1, player2, player3]
    enemies = [enemy1, enemy2, enemy3]
    return players, enemies
