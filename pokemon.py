import csv

class Pokemon:
    def __init__(self, pokedex, type, type1, name, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd):
        self.pokedex = pokedex
        self.type = type
        self.type1 = type1
        self.name = name
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_spatk = base_spatk
        self.base_spdef = base_spdef
        self.base_spd = base_spd

    def calculate_stat(self, base, level, iv=31, ev=0, is_hp=False):
        if is_hp:
            return int(((2 * base + iv + (ev // 4)) * level) / 100) + level + 10
        else:
            return int(((2 * base + iv + (ev // 4)) * level) / 100) + 5

    def get_stats(self, level):
        return {
            "HP": self.calculate_stat(self.base_hp, level, is_hp=True),
            "Attack": self.calculate_stat(self.base_atk, level),
            "Defense": self.calculate_stat(self.base_def, level),
            "Sp. Atk": self.calculate_stat(self.base_spatk, level),
            "Sp. Def": self.calculate_stat(self.base_spdef, level),
            "Speed": self.calculate_stat(self.base_spd, level),
        }

# --- Reading the CSV ---
pokemon_objects = {}

with open('pokemon.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pokemon = Pokemon(
            pokedex=row['Number'],
            type=row['Type 1'],
            type1=row['Type 2'],
            name=row['Name'],
            base_hp=int(row['HP']),
            base_atk=int(row['Attack']),
            base_def=int(row['Defense']),
            base_spatk=int(row['Sp.Attack']),
            base_spdef=int(row['Sp.Defense']),
            base_spd=int(row['Speed'])
        )
        pokemon_objects[pokemon.name] = pokemon
