import csv, random
from typing import List, Dict
import utils.pokemon
import utils.move
pokemons_csv = 'pokemons.csv'
moves_csv = 'moves.csv'

# Función que guardará los nombre de los pokemons en una lista
def create_teams_and_pokemons(pokemons_csv: str) -> List[Dict[str, str]]:
    """
    Lee un archivo CSV y guarda los nombres y tipos principales de los pokemons en una lista.

    Args:
        pokemons_csv (str): Ruta al archivo CSV que contiene los datos de los pokemons.

    Returns:
        List[Dict[str, str]]: Lista de diccionarios con los nombre y tipos de los pokemons.
            Cada diccionario tiene las claves 'name' y 'type1'.
    """
    pokemon_teams = []
    with open(pokemons_csv, newline='') as csvfile:
        # Crea un lector de diccionarios para procesar el archivo CSV
        pokemon_reader = csv.DictReader(csvfile)
        pokemon_data = []
        for row in pokemon_reader:
            # Agrega el nombre y el tipo del pokemon a la lista según la columna 'name' y 'type1' y 'is_legendary'
            pokemon_info = {
                'pokedex_number': row['pokedex_number'],
                'name': row['name'],
                'type1': row['type1'],
                'type2': row['type2'],
                'hp': row['hp'],
                'attack': row['attack'],
                'defense': row['defense'],
                'sp_attack': row['sp_attack'],
                'sp_defense': row['sp_defense'],
                'speed': row['speed'],
                'generation': row['generation'],
                'height_m': row['height_m'],
                'weight_kg': row['weight_kg'],
                'is_legendary': row['is_legendary'],
                'moves': row['moves']
            }
            pokemon_data.append(pokemon_info)
    print(pokemon_data)
    moves_reader = csv.DictReader('moves_csv')
    with open('moves.csv', newline='') as moves_csv_file:
        # Crea un lector de diccionarios para procesar el archivo CSV de movimientos
        moves_reader = csv.DictReader(moves_csv_file)
        move_data_list = []
        # Itera sobre cada fila en el archivo CSV de movimientos
        for move_row in moves_reader:
            # Crea un diccionario con la información de cada movimiento
            move_info = {
                'name': move_row['name'],
                'type': move_row['type'],
                'category': move_row['category'],
                'pp': move_row['pp'],
                'power': move_row['power'],
                'accuracy': move_row['accuracy']
            }
            move_data_list.append(move_info)
    
    for _ in range(50):
        team = []
        for _ in range(6):
            pokemon = random.choice(list(pokemon_data))
            print(pokemon)
            pokemon_name = pokemon_data[pokemon]['name']
            pokemon_data.pop([pokemon]['name'])
            moves_name = list(move_info['name'].split(';'))
            move_info.pop('name')
            moves_data = {}
            for move in moves_name:
                moves_data[move] = utils.move.Move.from_dict(move, move_info)
            pokemon.pop('moves')
            team.append(utils.pokemon.Pokemon.from_dict(pokemon_name, pokemon, moves_data))
        pokemon_teams.append(team)

    return pokemon_teams


create_teams_and_pokemons(pokemons_csv)