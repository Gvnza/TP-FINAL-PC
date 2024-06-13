import csv, random
from typing import List, Dict
import utils.pokemon as pokemon
import utils.move as move
import utils.team


def define_pokemons_objects():
    '''
    Crea todos los pokemones en forma de objetos

    Returns:
    Todos los pokemones (a excepcion de legendarios) en forma de diccionario. Ej; {... , "Charmander" : [objeto]}
    '''
    pokemon_objects = {}
    moves_data = {}
    with open('pokemons.csv', newline='') as pokemonfile:
        with open('moves.csv', newline='') as movesfile:
            moves_reader = csv.DictReader(movesfile)
            for row in moves_reader: #Lectura del archivo csv de movimientos
                moves_data[row['name']] = {'type' : row['type'], 'category' : row['category'],
                    'pp' : int(row['pp']), 'power' : int(row['power']), 'accuracy' : int(row['accuracy'])}
        pokemon_reader = csv.DictReader(pokemonfile)
        for row in pokemon_reader:
            pokemon_moves = {}
            if row['is_legendary'] != 1:
                pokemon_info = { #Lectura del archivo csv de pokemones, evito legendarios
                    'pokedex_number': row['pokedex_number'], 'type1': row['type1'], 'type2': row['type2'],
                    'hp': int(row['hp']), 'attack': int(row['attack']), 'defense': int(row['defense']),
                    'sp_attack': int(row['sp_attack']), 'sp_defense': int(row['sp_defense']), 'speed': int(row['speed']),
                    'generation': int(row['generation']), 'height_m': row['height_m'], 'weight_kg': row['weight_kg'],
                    'is_legendary': bool(row['is_legendary']), 'moves' : row['moves'].split(';') }
                for move in pokemon_info['moves']:
                    if move != '': #Evito que de error si no tiene movimientos (como es el caso de algunos pokemon). Ver nota despues de la funcion
                        pokemon_moves[move] = moves_data[move]
                pokemon_objects[row['name']] = pokemon.Pokemon.from_dict(row['name'], pokemon_info, pokemon_moves) #Creo los objetos
    return pokemon_objects

#Nota: Se podria evitar el if move != '': si se evita que se procesen pokemones del archivo csv que no tengan movimientos, posible cambio a tener en cuenta. -Gonza

def create_teams(cuantity):
    '''
    Crea todos los equipos.

    Args:
    cuantity: La cantidad de equipos totales que queres.

    Returns: 
    teams: Los equipos procesados con las funciones dadas.
    '''
    all_pokemon_objects = define_pokemons_objects()
    teams = []
    for i in range(cuantity):
        team = []
        team_pokemon_names = [] #Este codigo no cambio
        while len(team) < 6:
            pokemon_name = random.choice(list(all_pokemon_objects.keys()))
            pokemon = all_pokemon_objects[pokemon_name]
            if pokemon_name not in team_pokemon_names:
                team.append(pokemon)
                team_pokemon_names.append(pokemon_name)
        teams.append(utils.team.Team(str(f'Equipo {i}'), team, 0))
    return teams

#NOTA: Si bien el codigo se redujo bastante en cantidad de lineas, la complejidad no deberia haberse visto tan afectada, deberia haber mejorado, pero tampoco es demasiado.
#      Un problema recurrente de los TPs por lo que estuve viendo de los demas, es que tarda mucho en correr. Intentemos hacer el codigo lo mas optimizado posible. -Gonza