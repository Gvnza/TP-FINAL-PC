import csv, random
from typing import List, Dict

csv_file = 'pokemons.csv'

# Función que guardará los nombre de los pokemons en una lista
def save_names_types(csv_file: str) -> List[Dict[str, str]]:
    """
    Lee un archivo CSV y guarda los nombres y tipos principales de los pokemons en una lista.

    Args:
        csv_file (str): Ruta al archivo CSV que contiene los datos de los pokemons.

    Returns:
        List[Dict[str, str]]: Lista de diccionarios con los nombre y tipos de los pokemons.
            Cada diccionario tiene las claves 'name' y 'type1'.
    """

    # Crea una lista vacía para almacenar la informacion
    pokemon_name_type = []

    # Abre el archivo CSV en modo lectura
    with open(csv_file, newline='') as csvfile:
        # Crea un lector de diccionarios para procesar el archivo CSV
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Agrega el nombre y el tipo del pokemon a la lista según la columna 'name' y 'type1'
            pokemon_info = {
                'name': row['name'],
                'type': row['type1']
            }

            # Agrega la información a la lista
            pokemon_name_type.append(pokemon_info)

    # Devuelve la lista de nombres y tipos
    return pokemon_name_type

# Lista de tipos de Pokémon
pokemons_type = [
                'normal', 'fire', 'water', 'grass', 'electric', 'ice',
                'fighting', 'poison', 'ground', 'flying', 'psychic',
                'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy'
                ]

def team_generator(num_teams):
    teams = []
    
    for _ in range(num_teams):
        team = set()  # Usamos un conjunto para evitar duplicados
        
        pokemon_I = random.choice(save_names_types(csv_file))
        team.add(pokemon_I['name'])
    
        pokemon_II = pokemon_I
        while pokemon_II['type'] == pokemon_I['type']:
            pokemon_II = random.choice(save_names_types(csv_file))
        team.add(pokemon_II['name'])

        pokemon_III = pokemon_II
        while (pokemon_III['type'] == pokemon_II['type']) or (pokemon_III['type'] == pokemon_I['type']):
            pokemon_III = random.choice(save_names_types(csv_file))
        team.add(pokemon_III['name'])

        pokemon_IV = pokemon_III
        while (pokemon_IV['type'] == pokemon_III['type']) or (pokemon_IV['type'] == pokemon_II['type']) or (pokemon_IV['type'] == pokemon_I['type']):
            pokemon_IV = random.choice(save_names_types(csv_file))
        team.add(pokemon_IV['name'])

        pokemon_V = pokemon_IV
        while (pokemon_V['type'] == pokemon_IV['type']) or (pokemon_V['type'] == pokemon_III['type']) or (pokemon_V['type'] == pokemon_II['type']) or (pokemon_V['type'] == pokemon_I['type']):
            pokemon_V = random.choice(save_names_types(csv_file))
        team.add(pokemon_V['name'])

        pokemon_VI = pokemon_V
        while (pokemon_VI['type'] == pokemon_V['type']) or (pokemon_VI['type'] == pokemon_IV['type']) or (pokemon_VI['type'] == pokemon_III['type']) or (pokemon_VI['type'] == pokemon_II['type']) or (pokemon_VI['type'] == pokemon_I['type']):
            pokemon_VI = random.choice(save_names_types(csv_file))
        team.add(pokemon_VI['name'])
        
        teams.append(list(team))  # Convertimos el conjunto en una lista
    
    return teams

# Generar 50 equipos
generated_teams = team_generator(50)

# Imprimir los equipos
for i, team in enumerate(generated_teams, start=1):
    print(f"Equipo {i}: {', '.join(team)}")