import csv, random
from typing import List, Dict
import utils.pokemon
import utils.move
import utils.team

def define_pokemons() -> List[Dict[str, str]]:
    """
    Lee un archivo CSV y guarda los datos en distintas listas.

    Returns:
        names_list: Los nombres de los pokemons, en fila
        .
    """
    with open('pokemons.csv', newline='') as csvfile:
        # Crea un lector de diccionarios para procesar el archivo CSV
        pokemon_reader = csv.DictReader(csvfile)
        pokemon_data = []
        names_list = []
        moves_list = []
        for row in pokemon_reader:
            pokemon_info = {
                'pokedex_number': row['pokedex_number'],
                'type1': row['type1'],
                'type2': row['type2'],
                'hp': int(row['hp']),
                'attack': int(row['attack']),
                'defense': int(row['defense']),
                'sp_attack': int(row['sp_attack']),
                'sp_defense': int(row['sp_defense']),
                'speed': int(row['speed']),
                'generation': int(row['generation']),
                'height_m': row['height_m'],
                'weight_kg': row['weight_kg'],
                'is_legendary': bool(row['is_legendary']),
            }
            pokemon_names = {
                'name': row['name']
            }
            pokemon_moves = {
                'moves' : row['moves']
            }
            # Hace listas con los diccionarios de los datos de nombres, movimientos y estadisticas.
            pokemon_data.append(pokemon_info), names_list.append(pokemon_names), moves_list.append(pokemon_moves)
    return names_list, pokemon_data, moves_list 

def define_moves():
    with open('moves.csv', newline='') as moves_file:
        moves_reader = csv.DictReader(moves_file)
        moves_data = []
        for row in moves_reader:
            move_info = {
                row['name']: {'type': row['type'],
                'category': row['category'],
                'pp': int(row['pp']),
                'power': int(row['power']),
                'accuracy': int(row['accuracy'])}
                }
            moves_data.append(move_info)
    return moves_data

def generate_pokemons(all_names, all_data, moves_names, moves_data):
    moves_data = define_moves()
    choice = random.choice(all_data) #Toma los datos de un pokemon de forma random (pokedex, tipos, stats, etc)
    pokemon_name = all_names[int(choice['pokedex_number']) -1] #Crea una variable que sea el nombre del pokemon. Se resta uno por el sistema basado en ceros.
    pokemon_name = pokemon_name['name'] #Pasa de {'name': Squirtle} a 'Squirtle'
    pokemon_moves = moves_names[int(choice['pokedex_number']) -1] #Toma los movimientos correspondientes del pokemon tomados en la func anterior (ex- pokemon_moves)
    # Es importante saber que se ve así: {'moves': ...Beam;Mud Shot;Aurora Beam;Facade;Hyper...}
    pokemon_moves = pokemon_moves['moves'].split(';') 
    choice['moves'] = pokemon_moves
    # Pasa a verse asi: [..., 'Strength', 'Dragon Rush', ...]
    moves_dicc = {}
    #Ya que la funcion Pokemon.from_dict necesita que los movimientos del pokemon tengan una forma de dics de dics (ver línea 101 de pokemon.py)
    for move in pokemon_moves:
        for dicc in moves_data:
            if list(dicc.keys())[0] == move:
                moves_dicc[move] = dicc[move]
    return pokemon_name, choice, moves_dicc

def create_teams(cuantity):
    all_names, all_data, moves_names = define_pokemons()
    moves = define_moves()
    teams = []
    for i in range(cuantity):
        team = []
        team_pokemon_names = set() #Toma los nombres de los pokemones asi no hay duplicados (despues hay que hacerlo)
        for _ in range(6):
            pokemon_name, choice, moves_dicc = generate_pokemons(all_names, all_data, moves_names, moves)
            pokemon = utils.pokemon.Pokemon.from_dict(pokemon_name, choice, moves_dicc)
            if pokemon_name not in team_pokemon_names:
                pokemon_name, choice, moves_dicc = generate_pokemons(all_names, all_data, moves_names, moves)
                pokemon = utils.pokemon.Pokemon.from_dict(pokemon_name, choice, moves_dicc)
                team.append(pokemon)
                team_pokemon_names.add(pokemon_name)
                break
            team.append(pokemon)
        teams.append(utils.team.Team(str(f'Equipo {i}'), team, 0))
    return teams