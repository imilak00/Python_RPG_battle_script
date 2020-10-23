class Item:
    def __init__(self, name, type, description, dmg):
        self.name = name
        self.type = type
        self.description = description
        self.dmg = dmg

    def generate_damage(self):

        return self.dmg
