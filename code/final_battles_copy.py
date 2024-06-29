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

def round_simulation (team1: 'Team', team2: 'Team', effectiveness: Dict[Tuple[str, str], float]) -> None:
    """
    Simula una ronda de batalla entre dos equipos de Pokémon.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        effectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.
    """
    #Conseguir al starter/pokemon actual de ambos equipos
    pokemon1 = team1.pokemons[0]
    pokemon2 = team2.pokemons[0]
    
    #Conseguir el mejor movimiento a la hora de atacar
    movement1 = pokemon.get_best_attack(pokemon2, effectiveness)
    movement2 = pokemon.get_best_attack(pokemon1, effectiveness)

    damage1 = movement1.get_damage(pokemon1, pokemon2, effectiveness)
    damage2 = movement2.get_damage(pokemon2, pokemon1, effectiveness)

    #Datos y visualización
    pokemon2.current_hp -= damage1
    print(f'{pokemon1.name} usó {movement1.name}!')
    events_visualization(f'{team1.name}: {pokemon1.name} usó {movement1.name}')
    
    #Vida
    hp1 = team1.get_current_pokemon().current_hp

    #Checkeo de vida
    if hp1 > 0:
        special_events_visualization(f'{int(hp1)}/{int(team1.get_current_pokemon().max_hp)}', width - 130, 495, 20, 1)
    elif hp1 <= 0:
        special_events_visualization(f'0/{int(team1.get_current_pokemon().max_hp)}', width - 130, 495, 20, 1)

    
    if pokemon2.current_hp <= 0:
        print(f'{pokemon2.name} se debilitó...')
        team2.pokemons.pop(0)
        if len(team2.pokemons) == 0:
            print(f'¡Has derrotado a {team2.name}!')

    if team2.pokemons:
        pokemon1.current_hp -= damage2
        print(f'{pokemon2.name} usó {movement2.name}!')
        events_visualization(f'{team2.name}: {pokemon2.name} usó {movement2.name}')
        if pokemon1.current_hp <= 0:
            print(f'{pokemon1.name} se debilitó...')
            team1.pokemons.pop(0)
            if len(team1.pokemons) == 0:
                print(f'[Nombre del Jugador] se quedó sin Pokémon utilizables.')
    
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

def battle_turn (team1: 'Team', team2: 'Team', effectiveness: Dict[Tuple[str, str], float]) -> None:
    """
    Ejecuta un turno de batalla entre dos equipos de Pokémon.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        effectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.
    """
    current_pokemon1 = team1.get_current_pokemon()
    current_pokemon2 = team2.get_current_pokemon()
    
    pygame.time.delay(2000)
    action1, objetive1 = team1.get_next_action(team2, effectiveness)
    action2, objetive2 = team2.get_next_action(team1, effectiveness)
    pygame.time.delay(2000)
    
    events_visualization(f'{team1.name}: {current_pokemon1.name} usó {action1}')
    pygame.time.delay(2000)
    events_visualization(f'{team2.name}: {current_pokemon2.name} usó {action2}')

    if action1 == 'switch' and objetive1 is not None:
        team1.do_action(action1, objetive1, team2, effectiveness)
        print(f'{team1.name} cambió a {current_pokemon1.name} por {objetive1.name}')
        events_visualization(f'{team1.name} cambió a {current_pokemon1.name} por {objetive1.name}')
        pygame.time.delay(2000)

    elif action2 == 'switch' and objetive2 is not None:
        team2.do_action(action2, objetive2, team1, effectiveness)
        print(f'{team2.name} cambió a {current_pokemon2.name} por {objetive2.name}')
        events_visualization(f'{team2.name} cambió a {current_pokemon2.name} por {objetive2.name}')
        pygame.time.delay(2000)


def battle_sim(team1, team2, effectiveness):
    turn = 0
    while any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):  
                  
        action_1, target_1 = team1.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(team1, effectiveness)

        current_pokemon1 = team1.get_current_pokemon()
        current_pokemon2 = team2.get_current_pokemon()
        
        pygame.time.delay(2000)
        
        # El cambio (switch) siempre ocurre primero
        if action_1 == 'switch':
            first = team1
            second = team2

            print(f'{team1.name} cambió a {current_pokemon1.name} por {team1.get_current_pokemon().name}')
            events_visualization(f'{team1.name} cambió a {current_pokemon1.name} por {team1.get_current_pokemon().name}')
            pygame.time.delay(2000)

        elif action_2 == 'switch':
            first = team2
            second = team1

            print(f'{team2.name} cambió a {current_pokemon2.name} por {team2.get_current_pokemon().name}')
            events_visualization(f'{team2.name} cambió a {current_pokemon2.name} por {team2.get_current_pokemon().name}')
            pygame.time.delay(2000)

            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1

        elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:            
            first = team1
            second = team2
        
        else:
            
            first = team2
            second = team1
            
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
    
        first.do_action(action_1, target_1, second, effectiveness)
        
        events_visualization(f'{team1.name}: {current_pokemon1.name} usó {action_1}')
        
        pygame.time.delay(2000)

        events_visualization(f'{team2.name}: {current_pokemon2.name} usó {action_2}')

        # Si alguno de los pokemons se debilita, el turno termina, y ambos tienen la oportunida de cambiar de pokemon (switch)
        if team1.get_current_pokemon().current_hp == 0:
            print(f'{team1.get_current_pokemon().name} se debilitó...')
            events_visualization(f'{team1.get_current_pokemon().name} se debilitó...')
            pygame.time.delay(2000)

            possibility_of_change(team1, team2, effectiveness)

        elif team2.get_current_pokemon().current_hp == 0:
            print(f'{team2.get_current_pokemon().name} se debilitó...')
            events_visualization(f'{team2.get_current_pokemon().name} se debilitó...')
            pygame.time.delay(2000)

            possibility_of_change(team2, team1, effectiveness)

        else:
            if action_2 == 'attack' and target_2 is None:
                print('No había nadie!')
                events_visualization('No había nadie')
                pygame.time.delay(2000)
                action_2, target_2 = second.get_next_action(first, effectiveness)
            second.do_action(action_2, target_2, first, effectiveness)
            
            if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:

                print(f'{team1.get_current_pokemon().name} se debilitó...')
                events_visualization(f'{team1.get_current_pokemon().name} se debilitó...')

                possibility_of_change(team1, team2, effectiveness)

        turn += 1
    
    return team1 if any(pokemon.current_hp > 0 for pokemon in team1.pokemons) else team2


def get_damage(self, attacker_pokemon: 'pokemon', defending_pokemon: 'pokemon', effectiveness: dict[str, dict[str, float]]) -> float:
    """
    Calcula el daño que el movimiento haría al Pokémon defensor.

    Parámetros:
    attacker_pokemon (Pokemon): El Pokémon que usa el movimiento.
    defending_pokemon (Pokemon): El Pokémon que recibe el movimiento.
    effectiveness (dict[str, dict[str, float]]): Un diccionario que contiene la efectividad de cada tipo contra otro.

    Devuelve:
    float: El daño que el movimiento haría al Pokémon defensor.
    """

    if self.accuracy < random.random()*100:
        print(f'¡ {attacker_pokemon.name} falló!')
        events_visualization(f'¡ {attacker_pokemon.name} falló!')
        return 0
    if self.category == 'physical':
        a = attacker_pokemon.attack
        d = defending_pokemon.defense
    else:
        a = attacker_pokemon.sp_attack
        d = defending_pokemon.sp_defense
    
    stab = 1.5 if self.type == attacker_pokemon.type1 or self.type == attacker_pokemon.type2 else 1
    effectiveness_bonus = effectiveness[defending_pokemon.type1][self.type]
    if defending_pokemon.type2 is not None:
        effectiveness_bonus *= effectiveness[defending_pokemon.type2][self.type]

    if random.random() <= 0.04:    
        if effectiveness > 1:
            print('¡Es súper eficaz!')
            events_visualization('¡Es súper eficaz!')
            
            print('¡Es un golpe crítico!')
            events_visualization('¡Es un golpe crítico!')
            
        elif effectiveness == 1:
            print('Es efectivo.')
            events_visualization('Es efectivo.')
            
            print('¡Es un golpe crítico!')
            events_visualization('¡Es un golpe crítico!')

        elif effectiveness == 0:
            print(f'No afecta a {defending_pokemon.name}...')
            events_visualization(f'No afecta a {defending_pokemon.name}...')
            
        else:
            print('No es muy eficaz...')
            events_visualization('No es muy eficaz...')
            
            print('¡Es un golpe crítico!')
            events_visualization('¡Es un golpe crítico!')
            
        return (((2*attacker_pokemon.level/5) * self.power * a/d)/50 + 2) * stab *  effectiveness_bonus * 1.5

        
def do_action(self, action: str, target: Move|int|None, defender: 'Team', effectiveness: dict[str, dict[str, float]]) -> None:
    """
    Ejecuta una acción.

    Parámetros:
    action (str): La acción que realizará el equipo. Puede ser 'attack' o 'switch'.
    target (Move|int|None): El movimiento que usará el equipo si la acción es 'attack', el índice del Pokémon al que el equipo cambiará si la acción es 'switch' o None si la acción es 'skip'.
    defender (Team): El equipo que recibirá la acción.
    effectiveness (dict[str, dict[str, float]]): Un diccionario que contiene la efectividad de cada tipo contra otro.
    """
    if action == 'attack':
        damage = target.get_damage(self.get_current_pokemon(), defender.get_current_pokemon(), effectiveness)
        
        defender.recieve_damage(damage)
        self.consecutive_switches = 0
    # Daño
    
    elif action == 'switch':
        if target is not None:
            self.change_pokemon(target)
            self.consecutive_switches += 1
    else:
        self.get_current_pokemon().current_hp = 0
  
def possibility_of_change(team1: Team, team2: Team, effectiveness: dict[str, dict[str, float]]) -> None:
    """
    Cambia el Pokémon actual del equipo que tiene un Pokémon debilitado. El otro equipo también puede cambiar su Pokémon después del equipo con el Pokémon debilitado.

    Parámetros:
    team1 (Team): Uno de los equipos.
    team2 (Team): El otro equipo.
    effectiveness (dict[str, dict[str, float]]): Un diccionario que contiene la efectividad de cada tipo contra otro.
    """
    if team1.get_current_pokemon().current_hp == 0:
        fainted_team = team1
        other_team = team2
    else:
        fainted_team = team2
        other_team = team1
    action_1, target_1 = fainted_team.get_next_action(other_team, effectiveness)
    fainted_team.do_action(action_1, target_1, other_team, effectiveness)
    action_2, target_2 = other_team.get_next_action(fainted_team, effectiveness)
    if action_2 == 'switch':
        other_team.do_action(action_2, target_2, fainted_team, effectiveness)


def fight_simulation_visualization(team1: 'Team', team2: 'Team', effectiveness: Dict[Tuple[str, str], float]) -> 'Team':
    """
    Simula y visualiza una batalla entre dos equipos de Pokémon.

    Args:
        team1 (Team): El primer equipo de Pokémon.
        team2 (Team): El segundo equipo de Pokémon.
        effectiveness (Dict[Tuple[str, str], float]): Un diccionario con la efectividad de los movimientos.

    Returns:
        Team: El equipo ganador.
    """
    print(f'¡{team2.name} quiere luchar!')
    events_visualization(f'¡{team2.name} quiere luchar!')
    pygame.time.wait(2000)
    running = True
    clock = pygame.time.Clock()
    
    while running:
        #Condicion de corte
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        #Fondo
        window.blit(background, (0, 0))
        
        # Análisis de la vida
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
    
    # Visualización de imágenes de pokemons
    if team1.pokemons:
        current_pokemon1 = team1.get_current_pokemon()
        show_pokemon(team1, team2, current_pokemon1, 120, 310, (250, 250))
    
    if team2.pokemons:
        current_pokemon2 = team2.get_current_pokemon()
        show_pokemon(team1, team2, current_pokemon2, 670, 120, (250, 250))
    
    sample_of_defeated_pokemons(team1, team2)
    
    pygame.display.flip()
    clock.tick(60)

    battle_sim(team1, team2, effectiveness)

    pygame.time.wait(2000)
pygame.time.delay(5000)


def main() -> None:
    """
    Función principal que carga los datos y ejecuta la simulación de batalla.
    """
    pokemons_data = define_pokemons_objects()
    effectiveness = load_effectiveness('effectiveness_chart.csv')

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

    winner = fight_simulation_visualization(best_team, elite_four_will, effectiveness)
    print(winner)
    show_winner(winner)

if __name__ == '__main__':
    main()