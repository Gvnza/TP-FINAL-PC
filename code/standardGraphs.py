import matplotlib.pyplot as plt
import numpy as np

# Diversidad de Pokémon en los Equipos por Época: Un gráfico que muestre la cantidad de Pokémon distintos que aparecen en los equipos de cada época. Esto podría proporcionar información sobre la diversidad de Pokémon en los equipos a lo largo del tiempo.
def pokemon_diversity(teams):
    diversity = []
    for epoch in range(len(teams)):
        unique_pokemon = []
        for team in teams[epoch]:
            for pokemon in team.pokemons:
                if pokemon in unique_pokemon:
                    continue
                else:
                    unique_pokemon.append(pokemon)
        diversity.append(len(unique_pokemon))
    
    plt.plot(diversity, 'k')
    plt.xlabel('Época')
    plt.ylabel('Número de Pokémons únicos')
    plt.title('Diversidad Pokémon En los equipos por épocas')
    plt.show()

# Evolución de la Aptitud a lo largo de las Épocas: Un gráfico que muestre cómo cambia la aptitud del mejor equipo encontrado en cada época. Esto puede ayudar a visualizar cómo el algoritmo genético mejora la calidad de los equipos con el tiempo.
def fitness_evolution(fitness_list):
    plt.plot(fitness_list, 'royalblue')
    plt.xlabel('Época')
    plt.ylabel('Aptitud')
    plt.title('Evolución de aptitud por época')
    plt.show()

# Distribución de Pokémon en los Equipos en la última Época: Un gráfico de barras o un “pie chart” que muestre la distribución de los Pokémon en los equipos de la última época. Esto podría proporcionar información sobre la diversidad de Pokémon en los equipos finales.
def pokemon_distribution(last_epoch_teams):
    # Cuenta el número de veces que aparece cada Pokémon in los equipos
    pokemon_counts = {}
    for team in last_epoch_teams:
        for pokemon in team.pokemons:
            if pokemon not in pokemon_counts:
                pokemon_counts[pokemon] = 1
            else:
                pokemon_counts[pokemon] += 1
        
    # Crea un grafico de barras o un "pie chart" para mostrar la distribución
    pokemon_names = list(pokemon_counts.keys())
    pokemon_occurrences = list(pokemon_counts.values())
        
    # Gráfico de barras
    plt.bar(pokemon_names, pokemon_occurrences)
    plt.xlabel('Pokémon')
    plt.ylabel('Apariciones')
    plt.title('Distribución de Pokémons en los equipos (última época)')
    plt.show()
        
    # Pie chart
    plt.pie(pokemon_occurrences, labels=pokemon_names, autopct='%1.1f%%')
    plt.title('Distribución de Pokémons en los equipos (última época)')
    plt.show()

# Distribución de Tipos de Pokémon en los Equipos en la última Época: Un gráfico de barras o un “pie chart” que muestre la distribución de los tipos de Pokémon en los equipos de la última época. Esto podría proporcionar información sobre la diversidad de tipos de Pokémon en los equipos finales.
def pokemon_type_distribution1(last_epoch_teams):
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    type_counts = [0] * len(types)

    for team in last_epoch_teams:
        for pokemon in team.pokemons:
            pokemon_type = pokemon['type']
            type_index = types.index(pokemon_type)
            type_counts[type_index] += 1

    plt.bar(types, type_counts, color=['red', 'blue', 'green', 'yellow', 'gray', 'brown', 'purple', 'pink', 'lightblue', 'orange', 'lime', 'black', 'maroon', 'darkviolet', 'indigo', 'lightpink', 'silver'])
    plt.xlabel('Tipo de Pokémon')
    plt.ylabel('Cantidad')
    plt.title('Distribución de tipos de Pokémons en los equipos (última época)')
    plt.xticks(rotation=45)
    plt.show()

# Distribución de Tipos de Pokémon en los Equipos por Época: Un gráfico de lineas o un “stacked area plot” que muestre la distribución de los tipos de Pokémon en los equipos de cada época. Esto podría proporcionar información sobre la diversidad de tipos de Pokémon en los equipos a lo largo del tiempo.

def pokemon_type_distribution(pokemon_types):
    epochs = len(pokemon_types)
    teams = len(pokemon_types[0])
    types = len(pokemon_types[0][0])

    # Crea un gráfico de áreas apiladas para cada época
    for epoch in range(epochs):
        # Initialize the data for the stacked area plot
        stacked_data = np.zeros((teams, types))

        # Calcula la distribución de tipos de Pokémon en cada equipo
        for team in range(teams):
            for poke_type in range(types):
                stacked_data[team, poke_type] = sum(pokemon_types[epoch][team][poke_type])

        # Traza el gráfico de áreas apiladas
        plt.stackplot(range(teams), stacked_data.T, labels=['Type 1', 'Type 2', 'Type 3', 'Type 4', 'Type 5'])
        plt.xlabel('Equipo')
        plt.ylabel('Cantidad de Pokemones')
        plt.title(f'Distribucion de los tipos en los Equipos según la época {epoch+1}')
        plt.legend()
        plt.show()

# Estadísticas del mejor equipo encontrado: Un gráfico que muestre las estadísticas de los Pokémon en el mejor equipo encontrado por el algoritmo genético. Esto podría ayudar a visualizar las fortalezas y debilidades del equipo final. Se podría usar un gráfico de barras o un “radar chart” para este propósito.

def radar_chart(stats):
    labels = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    values = [stats['hp'], stats['attack'], stats['defense'], stats['sp_atk'], stats['sp_def'], stats['speed']]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
    ax.fill(angles, values, color='skyblue', alpha=0.25)
    ax.plot(angles, values, color='skyblue', linewidth=2)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    
    ax.yaxis.grid(True)
    ax.set_title('Estadísticas del mejor equipo')
    
    plt.show()

# Mejor equipo encontrado: Puede mostrar las imágenes de los Pokémon que componen el mejor equipo encontrado. Mostrando sus nombres y tipos.
def show_best_team(best_teams):
    # Carga la información de los Pokémon desde el archivo pokemons.csv
    pokemon_info = {}
    with open('pokemons.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Divide la línea en tres partes: ID, nombre y tipo
            pokemon_id, name, type = line.strip().split(',')
            # Almacena la información en el diccionario pokemon_info
            pokemon_info[pokemon_id] = (name, type)

    # Prepara un subplot para mostrar las imágenes
    fig, axes = plt.subplots(2, 3)
    fig.suptitle('Mejor Equipo Encontrado')

    # Muestra las imágenes e información de cada Pokémon en el mejor equipo
    for i, pokemon_id in enumerate(best_teams):
        # Carga y muestra la imagen del Pokémon
        img_path = f'imgs/{pokemon_id}.png'
        img = plt.imread(img_path)
        axes[i // 3, i % 3].imshow(img)
        axes[i // 3, i % 3].axis('off')

        # Obtiene el nombre y tipo del Pokémon
        name, type = pokemon_info[pokemon_id]
        # Establece el título del subplot con el nombre y tipo
        axes[i // 3, i % 3].set_title(f'{name}\n{type}')

    # Muestra el gráfico completo
    plt.show()

def average_wins(average_list, result_list):
    plt.plot(average_list, 'forestgreen', label='Equipos')
    plt.plot(result_list, 'firebrick', label='Rivales')
    plt.xlabel('Época')
    plt.ylabel('Promedio de Victorias')
    plt.title('Promedio de Victorias por Epoca')
    plt.legend()
    plt.show()

def time_per_epoch(time_per_epoch):
    plt.plot(time_per_epoch, 'indigo')
    plt.xlabel('Época')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempo por época')
    plt.show()

def best_teams_wins(best_teams):
    plt.plot(best_teams, 'gold')
    plt.xlabel('Época')
    plt.ylabel('Batallas ganadas')
    plt.title('Mejor equipo por época')
    plt.show()