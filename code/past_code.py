import csv
import pygame
import random
from utils.team import Team
import utils.pokemon as pokemon
from utils.combat import get_winner
from utils.move import Move
from typing import Dict, List, Tuple

# ------------------ Carga de datos ------------------
def define_pokemons_objects():
    pokemon_objects = []
    moves_data = {}
    # Abre los archivos csv de pokemones y movimientos
    with open('pokemons.csv', newline='') as pokemonfile:
        with open('moves.csv', newline='') as movesfile:
            # Crea un diccionario con los movimientos
            moves_reader = csv.DictReader(movesfile)
            for row in moves_reader: #Lectura del archivo csv de movimientos
                # Crea un diccionario con los datos (de cada columna) de movimientos
                moves_data[row['name']] = {'type' : row['type'], 'category' : row['category'],
                    'pp' : int(row['pp']), 'power' : int(row['power']), 'accuracy' : int(row['accuracy'])}
        # Crea un diccionario con los pokemones
        pokemon_reader = csv.DictReader(pokemonfile)
        for row in pokemon_reader:
            pokemon_moves = {}
            pokemon_info = { #Lectura del archivo csv de pokemones, evitando legendarios
                    'pokedex_number': row['pokedex_number'], 'type1': row['type1'], 'type2': row['type2'],
                    'hp': int(row['hp']), 'attack': int(row['attack']), 'defense': int(row['defense']),
                    'sp_attack': int(row['sp_attack']), 'sp_defense': int(row['sp_defense']), 'speed': int(row['speed']),
                    'generation': int(row['generation']), 'height_m': row['height_m'], 'weight_kg': row['weight_kg'],
                    'is_legendary': row['is_legendary'], 'moves' : row['moves'].split(';')}
            
            for move in pokemon_info['moves']:
                if move != '': #Evito que de error si no tiene movimientos (como es el caso de algunos pokemon). Ver nota despues de la funcion
                    pokemon_moves[move] = moves_data[move]

            pokemon_objects.append(pokemon.Pokemon.from_dict(row['name'], pokemon_info, pokemon_moves))
    return pokemon_objects

def load_moves(moves_file: str) -> dict[str, dict[str, str|int]]:
    moves = {}
    moves_file = 'moves.csv'
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
    effectiveness_file = 'effectiveness_chart.csv'
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

# ------------------ Simulación de combate ------------------

# Inicialización de pygame y del mezclador de música
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Música de Pokemon Red & Blue - Batalla (VS. Entrenador).mp3')
pygame.mixer.music.play(-1)


# Configuración de la ventana
width, height = 1024, 768
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('PELEA POKEMON')


# Definición de colores
white = (255, 255, 255)
grey = (72, 72, 72)
black = (0, 0, 0)
red = (236, 59, 25)
green = (24, 192, 32)
blue = (0, 0, 255)
white_text = white
grey_text = grey

def load_pokedex() -> Dict[str, int]:
    """
    Carga los datos de la Pokédex desde un archivo CSV.

    Returns:
        Dict[str, int]: Un diccionario con los nombres de los Pokémon como claves y sus números de Pokédex como valores.
    """
    pokedex = {}
    with open('pokemons.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokedex[row['name']] = int(row['pokedex_number'])
    return pokedex

def load_img(pokedex: Dict[str, int]) -> Dict[str, pygame.Surface]:
    """
    Carga las imágenes de los Pokémon desde el directorio 'imgs'.

    Args:
        pokedex (Dict[str, int]): Un diccionario con los nombres de los Pokémon como claves y sus números de Pokédex como valores.

    Returns:
        Dict[str, pygame.Surface]: Un diccionario con los nombres de los Pokémon como claves y sus imágenes como valores.
    """
    img = {}
    for name, pokedex_number in pokedex.items():
        number = f'{pokedex_number:03}'
        img_path = f'imgs/{number}.png'
        try:
            image = pygame.image.load(img_path)
            img[name] = image
        except pygame.error:
            print(f'No se pudo cargar la imagen {img_path}')
    return img

# Cargar los datos de la Pokédex y las imágenes de los Pokémon
pokemon_numbers = load_pokedex()
pokemon_images = load_img(pokemon_numbers)

# Cargar y escalar la imagen de fondo
background = pygame.image.load('Fondo.jpg')
background = pygame.transform.scale(background, (width, height))

def random_movements(poke: 'pokemon') -> 'Move':
    """
    Selecciona un movimiento aleatorio de un Pokémon.

    Args:
        poke (Pokemon): Un objeto de la clase Pokémon.

    Returns:
        Move: Un objeto de la clase Movimiento seleccionado aleatoriamente.
    """
    pokemon_moves = []
    for dicc in list(poke.moves.values()):
        for move in list(dicc.values()):
            if move is not None:
                pokemon_moves.append(move)
    return random.choice(pokemon_moves)

def round_simulation (team1, team2, efectiveness):
    pokemon1 = team1.pokemons[0]
    pokemon2 = team2.pokemons[0]

    movement1 = random_movements(pokemon1)
    movement2 = random_movements(pokemon2)

    damage1 = movement1.get_damage(pokemon1, pokemon2, efectiveness)
    damage2 = movement2.get_damage(pokemon2, pokemon1, efectiveness)

    pokemon2.current_hp -= damage1
    print(f'{pokemon1.name} usó {movement1.name}!')

    if pokemon2.current_hp <= 0:
        print(f'{pokemon2.name} se debilitó...')
        team2.pokemons.pop(0)
        if len(team2.pokemons) == 0:
            print(f'¡Has derrotado a {team2.name}!')

    if team2.pokemons:
        pokemon1.current_hp -= damage2
        print(f'{pokemon2.name} usó {movement2.name}!')
        if pokemon1.current_hp <= 0:
            print(f'{pokemon1.name} se debilitó...')
            team1.pokemons.pop(0)
            if len(team1.pokemons) == 0:
                print(f'{team1.name} se quedó sin Pokémon utilizables.')
    

def health_bar(pokemon: 'pokemon', x: int, y: int) -> None:
    """
    Dibuja una barra de salud para un Pokémon.

    Args:
        pokemon (Pokemon): El Pokémon para el cual se dibuja la barra de salud.
        x (int): La coordenada x de la barra de salud.
        y (int): La coordenada y de la barra de salud.
    """
    width = 220
    height = 23
    health = pokemon.current_hp / pokemon.max_hp
    pygame.draw.rect(window, white, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(window, white, (x - 4, y, width + 8, height))
    pygame.draw.rect(window, white, (x, y - 4, width, height + 8))
    pygame.draw.rect(window, red, (x, y, width, height))
    pygame.draw.rect(window, green, (x, y, width * health, height))
    
def show_pokemon(team1: 'Team', team2: 'Team', pokemon: 'pokemon', x: int, y: int, scale: Tuple[int, int]) -> None:
    """
    Muestra la imagen de un Pokémon en la pantalla.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        pokemon (Pokemon): El Pokémon cuya imagen se muestra.
        x (int): La coordenada x donde se muestra la imagen.
        y (int): La coordenada y donde se muestra la imagen.
        scale (Tuple[int, int]): La escala de la imagen.
    """
    image = pokemon_images[pokemon.name]
    image = pygame.transform.scale(image, scale)
    window.blit(image, (x, y))
    if pokemon in team1.pokemons:
        health_bar(pokemon, 770, 460)
    else:
        health_bar(pokemon, 190, 145)

def events_visualization(text: str) -> None:
    """
    Muestra un texto de evento en la pantalla.

    Args:
        text (str): El texto del evento que se mostrará.
    """
    font = pygame.font.Font('Windows Regular.ttf', 20)
    text_rendered = font.render(text, 1, grey_text)
    # Obtiene el rectángulo del texto y ajusta su posición
    text_rect = text_rendered.get_rect()
    text_rect.topleft = (25, height - 100)
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def line1_right_events_visualization(text: str) -> None:
    """
    Muestra un texto de evento en la pantalla.

    Args:
        text (str): El texto del evento que se mostrará.
    """
    font = pygame.font.Font('PressStart2P.ttf', 10)
    text_rendered = font.render(text, 1, grey_text)
    # Obtiene el rectángulo del texto y ajusta su posición
    text_rect = text_rendered.get_rect()
    text_rect.right = width - 55
    text_rect.bottom = height - 130
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def line2_right_events_visualization(text: str) -> None:
    """
    Muestra un texto de evento en la pantalla.

    Args:
        text (str): El texto del evento que se mostrará.
    """
    font = pygame.font.Font('PressStart2P.ttf', 10)
    text_rendered = font.render(text, 1, grey_text)
    # Obtiene el rectángulo del texto y ajusta su posición
    text_rect = text_rendered.get_rect()
    text_rect.right = width - 55
    text_rect.bottom = height - 100
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def special_events_visualization(text: str, x: int, y: int, scale: int, selected_font: int) -> None:
    """
    Muestra un texto en la pantalla en las coordenadas (x, y) especificadas.

    Args:
        text (str): El texto a mostrar.
        x (int): La coordenada x donde se mostrará el texto.
        y (int): La coordenada y donde se mostrará el texto.
        scale (int): El tamaño de la fuente del texto.
    """
    if selected_font == 1:
        font = pygame.font.Font('PressStart2P.ttf', scale)
    elif selected_font == 2:
        font = pygame.font.Font('Windows Regular.ttf', scale)

    text_rendered = font.render(text, True, grey_text)
    text_rect = text_rendered.get_rect()
    text_rect.topleft = (x, y)  # Alinea la esquina superior izquierda del texto con (x, y)
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def defeated_pokemon_counter(team: 'Team') -> int:
    """
    Cuenta el número de Pokémon derrotados en un equipo.

    Args:
        team (Team): El equipo de Pokémon.

    Returns:
        int: El número de Pokémon derrotados.
    """
    counter = 0
    for pokemon in team.pokemons:
        if pokemon.current_hp <= 0:
            counter += 1
    return counter

def sample_of_defeated_pokemons(team1: 'Team', team2: 'Team') -> None:
    """
    Muestra el número de Pokémon derrotados de cada equipo en la pantalla.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
    """
    defeated_team1 = defeated_pokemon_counter(team1)
    defeated_team2 = defeated_pokemon_counter(team2)

    line1_right_events_visualization(f'Jugador: {defeated_team1} pokemones derrotados')
    line2_right_events_visualization(f'{team2.name}: {defeated_team2} pokemones derrotados')

    pygame.display.flip()




# ------------------ Simulación de batalla ------------------

def fight_simulation_visualization(team1: 'Team', team2: 'Team', efectiveness: Dict[Tuple[str, str], float]) -> 'Team':
    """
    Simula y visualiza una batalla entre dos equipos de Pokémon.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        efectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.

    Returns:
        Team: El equipo ganador.
    """
    print(f'¡{team2.name} quiere luchar!')
    events_visualization(f'¡{team2.name} quiere luchar!')

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window.blit(background, (0, 0))

        if not any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
            events_visualization(f'¡{team2.name} ha ganado!')
            break
        elif not any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
            events_visualization(f'¡{team1.name} ha ganado!')
            break
        else:
            if team1.pokemons:
                current_pokemon1_name = team1.get_current_pokemon().name
                special_events_visualization(f'{current_pokemon1_name}', 613, 408, 45, 2)
                pygame.display.flip()

            if team2.pokemons:
                current_pokemon2_name = team2.get_current_pokemon().name
                special_events_visualization(f'{current_pokemon2_name}', 18, 92, 45, 2)
                pygame.display.flip()

        
        sample_of_defeated_pokemons(team1, team2)

        if team1.pokemons:
            current_pokemon1 = team1.get_current_pokemon()
            show_pokemon(team1, team2, current_pokemon1, 120, 310, (250, 250))
            pygame.display.flip()
        
        if team2.pokemons:
            current_pokemon2 = team2.get_current_pokemon()
            show_pokemon(team1, team2, current_pokemon2, 670, 120, (250, 250))
            pygame.display.flip()
        
        round_simulation(team1, team2, efectiveness)
        pygame.display.flip()

        
        pygame.display.flip()
        clock.tick(60)
        pygame.time.delay(2000)
    

        

def show_winner(team: 'Team') -> None:
    """
    Muestra la pantalla de ganador con el nombre del equipo vencedor.

    Args:
        team (Team): El equipo ganador.
    """
    window.fill(black)
    winner_screen_font = pygame.font.Font('PressStart2P.ttf', 36)
    winner_screen_text = winner_screen_font.render(f'¡{team.name} ha sido el vencedor!', 1, white_text)
    winner_screen_text_rect = winner_screen_text.get_rect(center = (width // 2, height // 2))
    window.blit(winner_screen_text, winner_screen_text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def our_do_action(attacker: 'Team', defender: 'Team', action: str, objetive: 'Move', efectiveness: Dict[Tuple[str, str], float]) -> None:
    """
    Realiza una acción en la batalla, ya sea un ataque o un cambio de Pokémon.

    Args:
        attacker (Team): El equipo que realiza la acción.
        defender (Team): El equipo que recibe la acción.
        action (str): La acción a realizar ('attack' o 'switch').
        objetive (Move): El movimiento a usar o el Pokémon al que cambiar.
        efectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.
    """

    if action == 'attack':
        damage = round(objetive.get_damage(attacker.get_current_pokemon(), defender.get_current_pokemon(), efectiveness))
        print(f'{attacker.get_current_pokemon().name} ha usado {objetive.name} en {defender.get_current_pokemon().name} y ha hecho {damage} de daño')
        events_visualization(f'{attacker.get_current_pokemon().name} usó {action}!')

        if efectiveness > 1:
            print('¡Es súper eficaz!')
            events_visualization('¡Es súper eficaz!')
        elif efectiveness == 1:
            print('Es efectivo.')
            events_visualization('Es efectivo.')
        elif efectiveness == 0:
            print(f'No afecta a {defender.name}...')
            events_visualization(f'No afecta a {defender.name}...')
        else:
            print('No es muy eficaz...')
            events_visualization('No es muy eficaz...')

        if defender.get_current_pokemon().current_hp == 0:
            print(f'{defender.get_current_pokemon().name} se debilitó...')
            events_visualization(f'{defender.get_current_pokemon().name} se debilitó...')

    elif action == 'switch':
        attacker.do_action(action, objetive, defender, efectiveness)
        print(f'{attacker.name} cambió a {attacker.get_current_pokemon().name} por {objetive.name}')
        events_visualization(f'{attacker.name} cambió a {attacker.get_current_pokemon().name} por {objetive.name}')

    pygame.time.wait(2000)

def battle_turn (team1: 'Team', team2: 'Team', efectiveness: Dict[Tuple[str, str], float]) -> None:
    """
    Ejecuta un turno de batalla entre dos equipos de Pokémon.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        efectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.
    """
    current_pokemon1 = team1.get_current_pokemon()
    current_pokemon2 = team2.get_current_pokemon()

    action1, objetive1 = team1.get_next_action(team2, efectiveness)
    action2, objetive2 = team2.get_next_action(team1, efectiveness)

    events_visualization(f'{team1.name}: {current_pokemon1.name} usó {action1}')
    events_visualization(f'{team2.name}: {current_pokemon2.name} usó {action2}')

    if action1 == 'switch' and objetive1 is not None:
        team1.do_action(action1, objetive1, team2, efectiveness)
        print(f'{team1.name} cambió a {current_pokemon1.name} por {objetive1.name}')
        events_visualization(f'{team1.name} cambió a {current_pokemon1.name} por {objetive1.name}')

    elif action2 == 'switch' and objetive2 is not None:
        team2.do_action(action2, objetive2, team1, efectiveness)
        print(f'{team2.name} cambió a {current_pokemon2.name} por {objetive2.name}')
        events_visualization(f'{team2.name} cambió a {current_pokemon2.name} por {objetive2.name}')

    else:
        if current_pokemon1.speed > current_pokemon2.speed:
            first, second = team1, team2
            first_action, first_objetive, second_action, second_objetive = action1, objetive1, action2, objetive2
        else:
            first, second = team2, team1
            first_action, first_objetive, second_action, second_objetive = action2, objetive2, action1, objetive1

        our_do_action(first, second, first_action, first_objetive, efectiveness)
        if second.get_current_pokemon().current_hp > 0:
            our_do_action(second, first, second_action, second_objetive, efectiveness)

    pygame.time.wait(2000)


def main() -> None:
    """
    Función principal que carga los datos y ejecuta la simulación de batalla.
    """
    pokemons_data = define_pokemons_objects()
    efectiveness = load_effectiveness('effectiveness_chart.csv')

    best_team = Team('Epic Team', pokemons = [
        pokemons_data[94],
        pokemons_data[150],
        pokemons_data[149],
        pokemons_data[6],
        pokemons_data[130],
        pokemons_data[68]
    ])

    # Definición de los equipos basados en los datos cargados
    elite_four_will = Team('Will', [
        pokemons_data[437],
        pokemons_data[124],
        pokemons_data[326],
        pokemons_data[80],
        pokemons_data[282],
        pokemons_data[178]
    ])

    elite_four_koga = Team('Koga', [
        pokemons_data[435],
        pokemons_data[454],
        pokemons_data[317],
        pokemons_data[49],
        pokemons_data[89],
        pokemons_data[169]
    ])

    elite_four_bruno = Team('Bruno', [
        pokemons_data[237],
        pokemons_data[106],
        pokemons_data[297],
        pokemons_data[68],
        pokemons_data[448],
        pokemons_data[107]
    ])

    elite_four_karen = Team('Karen', [
        pokemons_data[461],
        pokemons_data[442],
        pokemons_data[430],
        pokemons_data[197],
        pokemons_data[229],
        pokemons_data[359]
    ])

    champion_lance = Team('Lance', [
        pokemons_data[373],
        pokemons_data[445],
        pokemons_data[149],
        pokemons_data[6],
        pokemons_data[334],
        pokemons_data[130]
    ])

    winner = fight_simulation_visualization(best_team, elite_four_will, efectiveness)
    print(winner)
    show_winner(winner)

if __name__ == '__main__':
    main()