import random


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
    def __init__(self, name, hp, mp, atk, deff, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.deff = deff
        self.magic = magic                 # argument je niz objekata tipa Spell
        self.items = items                 # arg.je niz riječnika koji sadrže "item" -> objekt i "quantity" -> integer
        self.actions = ["Attack", "Magic", "Items"]

    def generate_dmg(self):
        return random.randrange(self.atkl, self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

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

    """
    Kada prosljeđujemo magic argument, prosljeđujemo niz objekata. U slučaju ove for petlje, svaki objekt zove se spell.
    To znači da se za svaki objekt spell pozovu argumenti type, name, dmg i cost iz klase magic. Klasa magic se ne 
    treba importati u game.py jer se argument poziva u main.py. Self.magic znači da se gleda niz objekata magic 
    koji je proslijeđen kao argument pri inicijalizaciji objekta. Program zna da se funkcija odnosi na taj objekt
    jer se poziva preko njega (player.choose_magic())
    """
    def choose_magic(self):
        print("MAGIC")
        i = 0
        for spell in self.magic:
            if spell.type == "black":
                print("    ", str(i+1) + ":", spell.name, "(damage:", str(spell.dmg) + ", cost:", str(spell.cost) + ")")
            elif spell.type == "white":
                print("    ", str(i + 1) + ":", spell.name, "(heal:", str(spell.dmg) + ", cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        print("ITEMS")
        i = 0
        for item in self.items:
            print("    ", str(i+1) + ":", item["item"].name, "-", item["item"].description +
                  ", (x" + str(item["quantity"]) + ")")
            i += 1

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
        return choice

