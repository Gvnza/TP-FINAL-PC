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
            # Agrega el nombre y el tipo del pokemon a la lista según la columna 'name' y 'type1' y 'is_legendary'
            pokemon_info = {
                'name': row['name'],
                'type': row['type1'],
                'legendary': row['is_legendary']
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

def generate_non_legendary():
    while True:
        pokemon = random.choice(save_names_types(csv_file))
        if pokemon['legendary'] != '1':
            return pokemon['name']

def team_generator(epoch):
    teams = []
    for _ in range(epoch):
        team = []
        for i in range(6):
            team.append(generate_non_legendary())
        teams.append(list(team))
    return teams

# Generar 50 equipos
generated_teams = team_generator(50)

# Imprimir los equipos
# for i, team in enumerate(generated_teams, start=1):
#     print(f"Equipo {i}: {', '.join(team)}")

def generate_encounters():
    teams = []
    for _ in range(400):
        team = []
        for i in range(6):
            pokemon = random.choice(save_names_types(csv_file))
            team.append(pokemon['name'])
        teams.append(list(team))
    return teams

# for i, team in enumerate(generated_teams, start=1):
#     print(f"Equipo {i}: {', '.join(team)}")

generated_encounters = generate_encounters()
for i, encounter in enumerate(generated_encounters, start=1):
    print(f"Encuentro {i}: {', '.join(encounter)}")