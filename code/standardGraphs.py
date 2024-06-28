import matplotlib.pyplot as plt
import numpy as np

# Diversidad de Pokémon en los Equipos por Época: Un gráfico que muestre la cantidad de Pokémon distintos que aparecen en los equipos de cada época. Esto podría proporcionar información sobre la diversidad de Pokémon en los equipos a lo largo del tiempo.
def pokemon_diversity(teams):
    diversity = []
    for epoch in teams:
        unique_pokemon = set()
        for team in epoch:
            for pokemon in team.pokemons:
                unique_pokemon.add(pokemon.name)
        diversity.append(len(unique_pokemon))
    
    plt.plot(diversity)
    plt.xlabel('Época')
    plt.ylabel('Número de Pokémons únicos')
    plt.title('Diversidad Pokémon En los equipos por épocas')
    plt.savefig('pokemon_diversity.png')
    plt.close()
        

# Evolución de la Aptitud a lo largo de las Épocas: Un gráfico que muestre cómo cambia la aptitud del mejor equipo encontrado en cada época. Esto puede ayudar a visualizar cómo el algoritmo genético mejora la calidad de los equipos con el tiempo.
def fitness_evolution(fitness_list):
    plt.plot(fitness_list, 'royalblue')
    plt.xlabel('Época')
    plt.ylabel('Aptitud')
    plt.title('Evolución de aptitud por época')
    plt.savefig('fitness_evolution.png')
    plt.close()
        

# Distribución de Pokémon en los Equipos en la última Época: Un gráfico de barras o un “pie chart” que muestre la distribución de los Pokémon en los equipos de la última época. Esto podría proporcionar información sobre la diversidad de Pokémon en los equipos finales.
def pokemon_distribution(last_epoch_teams):
    # Cuenta el número de veces que aparece cada Pokémon en los equipos
    pokemon_counts = {}
    for team in last_epoch_teams:
        for pokemon in team.pokemons:
            if pokemon.name not in pokemon_counts:
                pokemon_counts[pokemon.name] = 1
            else:
                pokemon_counts[pokemon.name] += 1

    # Ordenar los Pokémon por el número de apariciones de manera descendente
    sorted_pokemon_counts = sorted(pokemon_counts.items(), key=lambda item: item[1], reverse=True)
    pokemon_names = [item[0] for item in sorted_pokemon_counts]
    pokemon_counts = [item[1] for item in sorted_pokemon_counts]

    # Gráfico de barras horizontal
    plt.figure(figsize=(12, 10))  # Ajuste del tamaño de la figura
    plt.yticks(fontsize=5)
    plt.barh(pokemon_names, pokemon_counts, color='darkblue')
    plt.xlabel('Apariciones')
    plt.ylabel('Pokémon')
    plt.title('Distribución de Pokémon en los equipos (última época)')
    plt.gca().invert_yaxis()
    plt.savefig('pokemon_distribution_I.png')
    plt.close()

# Distribución de Tipos de Pokémon en los Equipos en la última Época: Un gráfico de barras o un “pie chart” que muestre la distribución de los tipos de Pokémon en los equipos de la última época. Esto podría proporcionar información sobre la diversidad de tipos de Pokémon en los equipos finales.
def second_pokemon_type_distribution(last_epoch_teams):
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    type_counts = [0] * len(types)

    for team in last_epoch_teams:
        for pokemon in team.pokemons:
            type_index = types.index(pokemon.type1)
            type_counts[type_index] += 1
            if pokemon.type2 is not None:
                type_index = types.index(pokemon.type2)
                type_counts[type_index] += 1
            else:
                type_counts[type_index] += 1

    plt.bar(types, type_counts, color=['grey', 'red', 'blue', 'yellow', 'green', 'lightblue', 'firebrick', 'purple', 'sandybrown', 'skyblue', 'deeppink', 'olivedrab', 'peru', 'indigo', 'midnightblue', 'black', 'slategrey', 'magenta'])
    plt.xlabel('Tipo de Pokémon')
    plt.ylabel('Cantidad')
    plt.title('Distribución de tipos de Pokémons en los equipos (última época)')
    plt.xticks(rotation=45)
    plt.savefig('second_pokemon_type_distribution.png')
    plt.close()

# Distribución de Tipos de Pokémon en los Equipos por Época: Un gráfico de lineas o un “stacked area plot” que muestre la distribución de los tipos de Pokémon en los equipos de cada época. Esto podría proporcionar información sobre la diversidad de tipos de Pokémon en los equipos a lo largo del tiempo.


def pokemon_type_distribution(teams):
    types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']
    entire_distribution_list = []

    for epoch in teams:
        type_counts = [0] * len(types)
        for team in epoch:
            for pokemon in team.pokemons:
                type_index = types.index(pokemon.type1)
                type_counts[type_index] += 1
                if pokemon.type2 is not None:
                    type_index = types.index(pokemon.type2)
                    type_counts[type_index] += 1
        entire_distribution_list.append(type_counts)


    transposed_distribution = list(map(list, zip(*entire_distribution_list)))

    # Colores para los tipos
    colors = ['grey', 'red', 'blue', 'yellow', 'green', 'lightblue', 'firebrick', 'purple', 'sandybrown', 'skyblue', 'deeppink', 'olivedrab', 'peru', 'indigo', 'midnightblue', 'black', 'slategrey', 'magenta']
    plt.figure(figsize=(12, 8))
    # Traza el gráfico de áreas apiladas
    plt.stackplot(range(len(teams)), transposed_distribution, colors=colors)
    plt.xlabel('Época')
    plt.ylabel('Cantidad de Pokemones')
    plt.title('Distribución de los tipos en los Equipos según la época')
    plt.legend(types, loc='upper right')
    plt.savefig('pokemon_type_distribution.png')
    plt.close()


# Estadísticas del mejor equipo encontrado: Un gráfico que muestre las estadísticas de los Pokémon en el mejor equipo encontrado por el algoritmo genético. Esto podría ayudar a visualizar las fortalezas y debilidades del equipo final. Se podría usar un gráfico de barras o un “radar chart” para este propósito.

def radar_chart(best_team):
    labels = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    for pokemon in best_team.pokemons:
        values = [pokemon.max_hp, pokemon.attack, pokemon.defense, pokemon.sp_attack, pokemon.sp_defense, pokemon.speed]
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
    plt.savefig('radar_chart.png')
    plt.close()

# Mejor equipo encontrado: Puede mostrar las imágenes de los Pokémon que componen el mejor equipo encontrado. Mostrando sus nombres y tipos.
def show_best_team(best_team):
    # Carga la información de los Pokémon desde el archivo pokemons.csv
    pokedex_number_list = []
    for pokemon in best_team.pokemons: 
        pokedex_number_list.append(pokemon.pokedex_number.zfill(3))

    # Prepara un subplot para mostrar las imágenes
    fig, axes = plt.subplots(2, 3)
    fig.suptitle('Mejor Equipo Encontrado\n')

    i = 0
    # Muestra las imágenes e información de cada Pokémon en el mejor equipo
    for number in pokedex_number_list:
        # Carga y muestra la imagen del Pokémon
        img_path = f'imgs/{number}.png'
        img = plt.imread(img_path)
        axes[i // 3, i % 3].imshow(img)
        axes[i // 3, i % 3].axis('off')

        name = best_team.pokemons[i].name
        type_1 = best_team.pokemons[i].type1
        if best_team.pokemons[i].type2 is not None:
            type_2 = best_team.pokemons[i].type2
        # Establece el título del subplot con el nombre y tipo
        axes[i // 3, i % 3].set_title(f'{name}\n{type_1}') if best_team.pokemons[i].type2 is None else axes[i // 3, i % 3].set_title(f'{name}\n{type_1} {type_2}')
        i += 1
    plt.savefig('show_best_team.png')
    plt.close()

def average_wins(average_list):
    plt.plot(average_list, 'forestgreen', label='Equipos')
    
    plt.xlabel('Época')
    plt.ylabel('Promedio de Victorias')
    plt.title('Promedio de Victorias por Epoca')
    plt.legend()
    plt.savefig('average_wins.png')
    plt.close()

def time_per_epoch(time_per_epoch):
    plt.plot(time_per_epoch, 'indigo')
    plt.xlabel('Época')
    plt.ylabel('Tiempo (s)')
    plt.title('Tiempo por época')
    plt.savefig('time_per_epoch.png')
    plt.close()

def best_teams_wins(best_teams, best_rivals):
    plt.plot(best_teams, 'gold')
    plt.plot(best_rivals, 'firebrick', label='Rivales')
    plt.xlabel('Época')
    plt.ylabel('Batallas ganadas')
    plt.title('Mejor equipo por época')
    plt.savefig('best_teams_wins.png')
    plt.close()