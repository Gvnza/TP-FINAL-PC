import csv
import pygame
import random
from utils.team import Team
import utils.pokemon as pokemon
from utils.combat import get_winner
from utils.move import Move

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
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Música de Pokemon Red & Blue - Batalla (VS. Entrenador).mp3')
pygame.mixer.music.play(-1)

width, height = 750, 450
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('PELEA POKEMON')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white_text = white

def load_pokedex():
    pokedex = {}
    with open('pokemons.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pokedex[row['name']] = int(row['pokedex_number'])
    return pokedex

def load_img(pokedex):
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

pokemon_numbers = load_pokedex()
pokemon_images = load_img(pokemon_numbers)

background = pygame.image.load('Campo_de_batalla_DPPt_2.png')
background = pygame.transform.scale(background, (width, height))

def random_movements(Pokemon):
    return random.choice(Pokemon.moves)

def round_simulation (team1, team2, efectiveness):
    pokemon1 = team1.pokemons[0]
    pokemon2 = team2.pokemons[0]

    movement1 = random_movements(pokemon1)
    movement2 = random_movements(pokemon2)

    damage1 = movement1.get_damage(pokemon1, pokemon2, efectiveness)
    damage2 = movement2.get_damage(pokemon2, pokemon1, efectiveness)

    pokemon2.hp -= damage1
    print(f'{pokemon1.name} usó {movement1.name}!')
    if pokemon2.hp <= 0:
        print(f'{pokemon2.name} se debilitó...')
        team2.pokemons.pop(0)
        if len(team2.pokemons) == 0:
            print(f'¡Has derrotado a {team2.name}!')

    if team2.pokemons:
        pokemon1.hp -= damage2
        print(f'{pokemon2.name} usó {movement2.name}!')
        if pokemon1.hp <= 0:
            print(f'{pokemon1.name} se debilitó...')
            team1.pokemons.pop(0)
            if len(team1.pokemons) == 0:
                print(f'[Nombre del Jugador] se quedó sin Pokémon utilizables.')
    
def health_bar(pokemon, x, y):
    width = 100
    height = 10
    health = pokemon.current_hp / pokemon.max_hp
    pygame.draw.rect(window, red, (x, y, width, height))
    pygame.draw.rect(window, green, (x, y, width * health, height))
    
def show_pokemon(team1, team2, pokemon, x, y, scale):
    image = pokemon_images[pokemon.name]
    image = pygame.transform.scale(image, scale)
    window.blit(image, (x, y))
    if pokemon in team1.pokemons:
        health_bar(pokemon, x, y - 50)
    else:
        health_bar(pokemon, x, y + 50)

def events_visualization(text):
    font = pygame.font.Font('PressStart2P.ttf', 36)
    text_rendered = font.render(text, 1, white_text)
    # Obtiene el rectángulo del texto y ajusta su posición
    text_rect = text_rendered.get_rect()
    text_rect.centerx = width // 2  # Centrado horizontalmente
    text_rect.bottom = height - 20   # Ajuste para que aparezca en la parte inferior
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def defeated_pokemon_counter(team):
    counter = 0
    for pokemon in team.pokemons:
        if pokemon.current_hp <= 0:
            counter += 1
    return counter

def sample_of_defeated_pokemons(team1, team2):
    defeated_team1 = defeated_pokemon_counter(team1)
    defeated_team2 = defeated_pokemon_counter(team2)

    font = pygame.font.Font('PressStart2P.ttf', 36)

    text_team1 = font.render(f'Jugador: {defeated_team1} pokemones derrotados', 1, white_text)
    text_team2 = font.render(f'{team2.name}: {defeated_team2} pokemones derrotados', 1, white_text)

    text_rect = text_team1.get_rect()
    text_rect.centerx = width // 2  # Centrado horizontalmente
    text_rect.bottom = height - 20

    window.blit(text_team1, text_rect)
    pygame.display.flip()

    text_rect = text_team2.get_rect()
    text_rect.centerx = width // 2  # Centrado horizontalmente
    text_rect.bottom = height - 20

    window.blit(text_team2, text_rect)
    pygame.display.flip()

def fight_simulation_visualization(team1, team2, efectiveness):
    print(f'¡{team2.name} quiere luchar!')
    events_visualization(f'¡{team2.name} quiere luchar!')
    pygame.time.wait(2000)
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.Font('PressStart2P.ttf', 36)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
            events_visualization(f'¡{team2.name} ha ganado!')
            break
        elif not any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
            events_visualization(f'¡{team1.name} ha ganado!')
            break
        
        window.blit(background, (0, 0))

        if team1.pokemons:
            current_pokemon1 = team1.get_current_pokemon()
            show_pokemon(team1, team2, current_pokemon1, 50, 350, (350, 350))
            health_bar(current_pokemon1, 50, 350)
        
        if team2.pokemons:
            current_pokemon2 = team2.get_current_pokemon()
            show_pokemon(team1, team2, current_pokemon2, 400, 50, (350, 350))
            health_bar(current_pokemon2, 400, 50)
        
        #if team1.pokemons:
        #    text = font.render(f'{current_pokemon1.name} HP: {current_pokemon1.current_hp}', 1, white_text)
        
        #if team2.pokemons:
        #    text = font.render(f'{current_pokemon2.name} HP: {current_pokemon2.current_hp}', 1, white_text)
        
        sample_of_defeated_pokemons(team1, team2)

        pygame.display.flip()
        clock.tick(60)

        round_simulation(team1, team2, efectiveness)

        pygame.time.wait(2000)
    pygame.time.delay(5000)

def show_winner(team):
    window.fill(black)
    winner_screen_font = pygame.font.Font('PressStart2P.ttf', 36)
    winner_screen_text = winner_screen_font.render(f'¡{team.name} ha sido el vencedor!', 1, white_text)
    winner_screen_text_rect = winner_screen_text.get_rect(center = (width // 2, height // 2))
    window.blit(winner_screen_text, winner_screen_text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def do_action(attacker, defender, action, objetive, efectiveness):
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

def battle_turn (team1, team2, efectiveness):
    current_pokemon1 = team1.get_current_pokemon()
    current_pokemon2 = team2.get_current_pokemon()

    action1, objetive1 = team1.get_next_action(team2, efectiveness)
    action2, objetive2 = team2.get_next_action(team1, efectiveness)

    events_visualization(f'{team1.name}: {current_pokemon1.name} ha usado {action1} en {objetive1.name}')
    events_visualization(f'{team2.name}: {current_pokemon2.name} ha usado {action2} en {objetive2.name}')

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
        
        do_action(first, second, first_action, first_objetive, efectiveness)
        if second.get_current_pokemon().current_hp > 0:
            do_action(second, first, second_action, second_objetive, efectiveness)
    
    pygame.time.wait(2000)


def main():
    movements = load_moves('moves.csv')
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

    show_winner(winner)

if __name__ == '__main__':
    main()