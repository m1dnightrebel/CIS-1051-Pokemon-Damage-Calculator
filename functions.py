type_chart = {
        'Normal': {'Rock': 0.5, 'Ghost': 0.0, 'Steel': 0.5},
        'Fire': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ice': 2.0, 'Bug': 2.0, 'Rock': 0.5, 'Dragon': 0.5,
                 'Steel': 2.0, 'Ground': 0.5},
        'Water': {'Fire': 2.0, 'Water': 0.5, 'Grass': 0.5, 'Ground': 2.0, 'Rock': 2.0, 'Dragon': 0.5},
        'Electric': {'Water': 2.0, 'Electric': 0.5, 'Grass': 0.5, 'Ground': 0.0, 'Flying': 2.0, 'Dragon': 0.5},
        'Grass': {'Fire': 0.5, 'Water': 2.0, 'Grass': 0.5, 'Poison': 0.5, 'Ground': 2.0, 'Flying': 0.5, 'Bug': 0.5,
                  'Rock': 2.0, 'Dragon': 0.5, 'Steel': 0.5},
        'Ice': {'Fire': 0.5, 'Water': 0.5, 'Grass': 2.0, 'Ground': 2.0, 'Flying': 2.0, 'Dragon': 2.0, 'Steel': 0.5},
        'Fighting': {'Normal': 2.0, 'Ice': 2.0, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 2.0,
                     'Ghost': 0.0, 'Dark': 2.0, 'Steel': 2.0, 'Fairy': 0.5},
        'Poison': {'Grass': 2.0, 'Poison': 0.5, 'Ground': 0.5, 'Rock': 0.5, 'Ghost': 0.5, 'Steel': 0.0, 'Fairy': 2.0},
        'Ground': {'Fire': 2.0, 'Electric': 2.0, 'Grass': 0.5, 'Poison': 2.0, 'Flying': 0.0, 'Rock': 2.0, 'Steel': 2.0},
        'Flying': {'Electric': 0.5, 'Grass': 2.0, 'Fighting': 2.0, 'Bug': 2.0, 'Rock': 0.5, 'Steel': 0.5},
        'Psychic': {'Fighting': 2.0, 'Poison': 2.0, 'Psychic': 0.5, 'Dark': 0.0, 'Steel': 0.5},
        'Bug': {'Fire': 0.5, 'Grass': 2.0, 'Fighting': 0.5, 'Poison': 0.5, 'Flying': 0.5, 'Psychic': 2.0, 'Ghost': 0.5,
                'Dark': 2.0, 'Steel': 0.5, 'Fairy': 0.5},
        'Rock': {'Fire': 2.0, 'Ice': 2.0, 'Fighting': 0.5, 'Ground': 0.5, 'Flying': 2.0, 'Bug': 2.0, 'Steel': 0.5},
        'Ghost': {'Normal': 0.0, 'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5},
        'Dragon': {'Dragon': 2.0, 'Steel': 0.5, 'Fairy': 0.0},
        'Dark': {'Fighting': 0.5, 'Psychic': 2.0, 'Ghost': 2.0, 'Dark': 0.5, 'Fairy': 0.5},
        'Steel': {'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Ice': 2.0, 'Rock': 2.0, 'Steel': 0.5, 'Fairy': 2.0},
        'Fairy': {'Fire': 0.5, 'Fighting': 2.0, 'Poison': 0.5, 'Dragon': 2.0, 'Dark': 2.0, 'Steel': 0.5},
    }
def calculate_damage(level, attack, defense, base_power, effectiveness, move_type=None, defender_type1=None, defender_type2=None):


    def get_effectiveness(move_type, defender_type1, defender_type2):
        if not move_type:
            return 1.0
        eff1 = type_chart.get(move_type, {}).get(defender_type1, 1.0)
        eff2 = type_chart.get(move_type, {}).get(defender_type2, 1.0) if defender_type2 else 1.0
        return eff1 * eff2

    try:
        type_multiplier = get_effectiveness(move_type, defender_type1, defender_type2)
        total_effectiveness = effectiveness * type_multiplier
        damage = (((2 * level / 5 + 2) * attack * base_power / defense) / 50 + 2) * total_effectiveness
        return round(damage, 2)
    except Exception as e:
        return None

def get_type_multiplier(move_type, defender_type1, defender_type2):
        eff1 = type_chart.get(move_type, {}).get(defender_type1, 1.0)
        eff2 = type_chart.get(move_type, {}).get(defender_type2, 1.0) if defender_type2 else 1.0
        return eff1 * eff2