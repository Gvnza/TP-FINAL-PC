import csv, random
from typing import List, Dict
import utils.pokemon as pokemon
import utils.move as move
import utils.team

def define_pokemons_objects() -> Dict[str, pokemon.Pokemon]:
    '''
    Crea todos los pokemones en forma de objetos

    Returns:
    Todos los pokemones (a excepcion de legendarios) en forma de diccionario. Ej; {... , "Charmander" : [objeto]}
    '''
    pokemon_objects = {}
    moves_data = {}
    # Abre los archivos csv de pokemones y movimientos
    # Abre los archivos csv de pokemones y movimientos
    with open('pokemons.csv', newline='') as pokemonfile:
        with open('moves.csv', newline='') as movesfile:
            # Crea un diccionario con los movimientos
            # Crea un diccionario con los movimientos
            moves_reader = csv.DictReader(movesfile)
            for row in moves_reader: #Lectura del archivo csv de movimientos
                # Crea un diccionario con los datos (de cada columna) de movimientos
                # Crea un diccionario con los datos (de cada columna) de movimientos
                moves_data[row['name']] = {'type' : row['type'], 'category' : row['category'],
                    'pp' : int(row['pp']), 'power' : int(row['power']), 'accuracy' : int(row['accuracy'])}
        # Crea un diccionario con los pokemones
        # Crea un diccionario con los pokemones
        pokemon_reader = csv.DictReader(pokemonfile)
        for row in pokemon_reader:
            pokemon_moves = {}
            # Análisis de si el pokemon es legendario o no
            # Análisis de si el pokemon es legendario o no
            if row['is_legendary'] != 1:
                pokemon_info = { #Lectura del archivo csv de pokemones, evitando legendarios
                    'pokedex_number': row['pokedex_number'], 'type1': row['type1'], 'type2': row['type2'],
                    'hp': int(row['hp']), 'attack': int(row['attack']), 'defense': int(row['defense']),
                    'sp_attack': int(row['sp_attack']), 'sp_defense': int(row['sp_defense']), 'speed': int(row['speed']),
                    'generation': int(row['generation']), 'height_m': row['height_m'], 'weight_kg': row['weight_kg'],
                    'is_legendary': bool(row['is_legendary']), 'moves' : row['moves'].split(';') }
                
                # Por cada movimiento dentro de la categoría movimientos...
                
                # Por cada movimiento dentro de la categoría movimientos...
                for move in pokemon_info['moves']:
                    if move != '': #Evito que de error si no tiene movimientos (como es el caso de algunos pokemon). Ver nota despues de la funcion
                        pokemon_moves[move] = moves_data[move]
                
                # Creación de los objetos de los pokemones
                pokemon_objects[row['name']] = pokemon.Pokemon.from_dict(row['name'], pokemon_info, pokemon_moves)
    return pokemon_objects # Retorna los objetos

#Nota: Se podria evitar el if move != '': si se evita que se procesen pokemones del archivo csv que no tengan movimientos, posible cambio a tener en cuenta. -Gonza

def create_teams(cuantity: int) -> List[utils.team.Team]:
    '''
    Crea todos los equipos.

    Args:
    cuantity: La cantidad de equipos totales que queres.

    Returns: 
    teams: Los equipos procesados con las funciones dadas.
    '''
    all_pokemon_objects = define_pokemons_objects()
    all_pokemon_keys = list(all_pokemon_objects.keys())
    # Por cada vez dentro de la cantidad pedida...
    teams = []
    # Por cada vez dentro de la cantidad pedida...
    for i in range(cuantity):
        team = []
        team_pokemon_names = [] #Este codigo no cambio
        # Mientras la cantidad de pokemones en el equipo sea menor a 6...
        while len(team) < 6:
            pokemon_name = random.choice(all_pokemon_keys)
            # Guarda al pokemon en una variable
            pokemon = all_pokemon_objects[pokemon_name]
            # Si el nombre del pokemon no esta en la lista de nombres de pokemones del equipo...
            # Si el nombre del pokemon no esta en la lista de nombres de pokemones del equipo...
            if pokemon_name not in team_pokemon_names:
                # Se agrega el pokemon al equipo y el nombre del pokemon a la lista de nombres de pokemones del equipo
                team.append(pokemon)
                team_pokemon_names.append(pokemon_name)
        teams.append(utils.team.Team(str(f'Equipo {i}'), team, 0))
    return teams


#NOTA: Si bien el codigo se redujo bastante en cantidad de lineas, la complejidad no deberia haberse visto tan afectada, deberia haber mejorado, pero tampoco es demasiado.
#      Un problema recurrente de los TPs por lo que estuve viendo de los demas, es que tarda mucho en correr. Intentemos hacer el codigo lo mas optimizado posible. -Gonza