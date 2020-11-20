from Classes.magic import Spell
from Classes.inventory import Item


# CREATE MAGIC
def create_magic():
    fire = Spell("Fire", 10, 100, "black")
    thunder = Spell("Thunder", 10, 100, "black")
    blizzard = Spell("Blizzard", 10, 100, "black")
    meteor = Spell("Meteor", 20, 200, "black")
    quake = Spell("Quake", 14, 140, "black")
    cure = Spell("Cure", 12, 120, "white")
    cura = Spell("Cura", 18, 200, "white")

    spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
    enemy_spells = [fire, meteor, cura]
    return spells, enemy_spells


# CREATE ITEMS
def create_items():
    potion = Item("Potion", "potion", "heals 50 HP", 50)
    hi_potion = Item("Hi-Potion", "potion", "heals 100 HP", 100)
    super_potion = Item("Super-Potion", "potion", "heals 500 HP", 500)
    elixir = Item("Elixir", "elixir", "Fully restores HP and MP of one party member", 9999)
    mega_elixir = Item("Mega-Elixir", "elixir", "Fully restores party's HP and MP", 9999)
    grenade = Item("Grenade", "attack", "Deals 200 damage", 200)
    items = [potion, hi_potion, super_potion, elixir, mega_elixir, grenade]
    return items


