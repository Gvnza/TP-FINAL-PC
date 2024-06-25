import csv
from utils.team import Team
from utils.pokemon import Pokemon

# Carga de datos
def load_pokemons(pokemons_file: str, moves_file: str) -> dict[str, Pokemon]:
    pokemons = {}
    moves_data = load_moves(moves_file)
    
    with open(pokemons_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokedex_number = int(row['pokedex_number'])
            name = row['name']
            type1 = row['type1']
            type2 = row['type2'] if row['type2'] != '' else None
            hp = int(row['hp'])
            attack = int(row['attack'])
            defense = int(row['defense'])
            sp_attack = int(row['sp_attack'])
            sp_defense = int(row['sp_defense'])
            speed = int(row['speed'])
            generation = int(row['generation'])
            height_m = float(row['height_m'])
            weight_kg = float(row['weight_kg'])
            is_legendary = bool(int(row['is_legendary']))
            moves = row['moves'].split(';')
            pokemon = Pokemon.from_dict(name, {
                'pokedex_number': pokedex_number,
                'type1': type1,
                'type2': type2,
                'hp': hp,
                'attack': attack,
                'defense': defense,
                'sp_attack': sp_attack,
                'sp_defense': sp_defense,
                'speed': speed,
                'generation': generation,
                'height_m': height_m,
                'weight_kg': weight_kg,
                'is_legendary': is_legendary,
                'moves': moves
            }, moves_data)
            pokemons[name] = pokemon
    return pokemons

def load_moves(moves_file: str) -> dict[str, dict[str, str|int]]:
    moves = {}
    with open(moves_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            type = row['type']
            category = row['category']
            pp = int(row['pp'])
            power = int(row['power'])
            accuracy = int(row['accuracy'])
            moves[name] = {
                'type': type,
                'category': category,
                'pp': pp,
                'power': power,
                'accuracy': accuracy
            }
    return moves

def load_effectiveness(effectiveness_file: str) -> dict[str, dict[str, float]]:
    effectiveness = {}
    with open(effectiveness_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            attack_type = row['attacking']
            effectiveness[attack_type] = {}
            for defense_type in row.keys():
                if defense_type != 'attacking':
                    effectiveness[attack_type][defense_type] = float(row[defense_type])
    return effectiveness

# Definición de los equipos basados en los datos cargados
pokemons_data = load_pokemons('pokemons.csv', 'moves.csv')
effectiveness = load_effectiveness('effectiveness_chart.csv')
elite_four_will = Team('Will', [
    pokemons_data['Bronzong'],
    pokemons_data['Jynx'],
    pokemons_data['Grumpig'],
    pokemons_data['Slowbro'],
    pokemons_data['Gardevoir'],
    pokemons_data['Xatu']
])

elite_four_koga = Team('Koga', [
    pokemons_data['Skuntank'],
    pokemons_data['Toxicroak'],
    pokemons_data['Swalot'],
    pokemons_data['Venomoth'],
    pokemons_data['Muk'],
    pokemons_data['Crobat']
])

elite_four_bruno = Team('Bruno', [
    pokemons_data['Hitmontop'],
    pokemons_data['Hitmonlee'],
    pokemons_data['Hariyama'],
    pokemons_data['Machamp'],
    pokemons_data['Lucario'],
    pokemons_data['Hitmonchan']
])

elite_four_karen = Team('Karen', [
    pokemons_data['Weavile'],
    pokemons_data['Spiritomb'],
    pokemons_data['Honchkrow'],
    pokemons_data['Umbreon'],
    pokemons_data['Houndoom'],
    pokemons_data['Absol']
])

champion_lance = Team('Lance', [
    pokemons_data['Salamence'],
    pokemons_data['Garchomp'],
    pokemons_data['Dragonite'],
    pokemons_data['Charizard'],
    pokemons_data['Altaria'],
    pokemons_data['Gyarados']
])

def generate_fight(team: Team):
    rival_teams = [elite_four_will, elite_four_koga, elite_four_bruno, elite_four_karen, champion_lance]
    
    for rival_team in rival_teams: