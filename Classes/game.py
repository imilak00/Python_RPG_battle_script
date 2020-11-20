import random
from Functions.create_spells_and_items import create_magic


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'            # završava formatiranje teksta
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.magic = magic                 # argument je niz objekata tipa Spell
        self.items = items                 # arg.je niz riječnika koji sadrže "item" -> objekt i "quantity" -> integer
        self.actions = ["Attack", "Magic", "Items", "Skip your turn"]

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def generate_dmg(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + self.name + bcolors.ENDC)
        print("ACTIONS")
        for action in self.actions:
            print(str(i) + ":", action)
            i += 1
        choice = int(input("Choose the action: ")) - 1
        if choice < 0 or choice > 3:
            print("Wrong input.")
            return self.choose_action()
        if choice == 1 and self.min_required_mana() > self.get_mp():
            print("Insufficient mana for any spell.")
            return self.choose_action()
        else:
            return choice

    def choose_magic(self):
        print("MAGIC")
        i = 0
        for spell in self.magic:
            if spell.type == "black":
                print("    ", str(i+1) + ":", spell.name, "(damage:", str(spell.dmg) + ", cost:", str(spell.cost) + ")")
            elif spell.type == "white":
                print("    ", str(i + 1) + ":", spell.name, "(heal:", str(spell.dmg) + ", cost:", str(spell.cost) + ")")
            i += 1
        print("     " + str(i+1) + ": Previous menu")
        magic_choice = int(input("Choose your spell: ")) - 1
        if magic_choice < 0 or magic_choice > i:
            print("Wrong input.")
            return self.choose_magic()
        else:
            return magic_choice, i

    def choose_item(self):
        print("ITEMS")
        i = 0
        for item in self.items:
            print("    ", str(i+1) + ":", item["item"].name, "-", item["item"].description +
                  ", (x" + str(item["quantity"]) + ")")
            i += 1
        print("     " + str(i+1) + ": Previous menu")
        item_choice = int(input("Choose your item: ")) - 1
        if item_choice < 0 or item_choice > i:
            print("Wrong input.")
            return self.choose_item()
        else:
            return item_choice, i

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.maxhp) * 100 / 2
        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1
        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)

        current_hp = ""
        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                    __________________________________________________")
        print(bcolors.BOLD + self.name + ": " + current_hp + "" + " |" + bcolors.FAIL +
              hp_bar + bcolors.ENDC + "|")

    def get_stats(self):        # POJASNI I SKRATI

        hp_bar = ""
        hp_bar_ticks = (self.hp / self.maxhp) * 100 / 4
        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1
        while len(hp_bar) < 25:
            hp_bar += " "

        mp_bar = ""
        mp_bar_ticks = (self.mp / self.maxmp) * 100 / 10
        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1
        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        mp_string = str(self.mp) + "/" + str(self.maxmp)

        current_hp = ""
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        current_mp = ""
        if len(mp_string) < 9:
            decreased = 9 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print("                    _________________________               __________ ")
        print(bcolors.BOLD + self.name + ":   " + current_hp + "" + " |" + bcolors.OKGREEN +
              hp_bar + bcolors.ENDC + "|" + bcolors.BOLD +
              "   " + current_mp + " |" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            print("        " + str(i) + ".", enemy.name)
            i += 1
        choice = int(input("    Choose target: ")) - 1

        if choice < 0 or choice > 2:
            print("Wrong input.")
            return self.choose_target(enemies)
        else:
            return choice

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))  # len je duljina liste, broj čarolija, len se odnosi i na broj elemenata, ne samo duljinu izraza
        chosen_spell = self.magic[magic_choice]
        if chosen_spell.cost > self.get_mp():
            return self.choose_enemy_spell()            # DRUGAČIJA SINTAKSA
        magic_dmg = chosen_spell.generate_damage()  # what -  atribut generate_damage se odnosi na Spell, vuče se iz magic.py
        health_percentage = self.hp / self.maxhp * 100
        chance = random.randrange(0, 9)

        if health_percentage > 35 and chosen_spell.type == "white" and chance > 1:
            return self.choose_enemy_spell()

        if health_percentage < 35 and chosen_spell.type == "black" and chance > 1:
            return self.choose_enemy_spell()
        return chosen_spell, magic_dmg

    def min_required_mana(self):
        spells, enemy_spells = create_magic()
        min_mana = spells[0].cost
        for spell in spells:
            if spell.cost < min_mana:
                min_mana = spell.cost

        return min_mana

