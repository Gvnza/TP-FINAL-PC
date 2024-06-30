import csv
import pygame
import random
from utils.team import Team
import utils.pokemon as pokemon
from utils.move import Move
from typing import Dict, List, Tuple

# ------------------ Carga de datos ------------------
def define_pokemons_objects():
    pokemon_objects = []
    moves_data = {}
    with open('pokemons.csv', newline='') as pokemonfile, open('moves.csv', newline='') as movesfile:
        moves_reader = csv.DictReader(movesfile)
        for row in moves_reader:
            moves_data[row['name']] = {
                'type': row['type'],
                'category': row['category'],
                'pp': int(row['pp']),
                'power': int(row['power']),
                'accuracy': int(row['accuracy'])
            }
        pokemon_reader = csv.DictReader(pokemonfile)
        for row in pokemon_reader:
            pokemon_moves = {}
            pokemon_info = {
                'pokedex_number': row['pokedex_number'], 'type1': row['type1'], 'type2': row['type2'],
                'hp': int(row['hp']), 'attack': int(row['attack']), 'defense': int(row['defense']),
                'sp_attack': int(row['sp_attack']), 'sp_defense': int(row['sp_defense']), 'speed': int(row['speed']),
                'generation': int(row['generation']), 'height_m': row['height_m'], 'weight_kg': row['weight_kg'],
                'is_legendary': row['is_legendary'], 'moves': row['moves'].split(';')
            }
            for move in pokemon_info['moves']:
                if move:
                    pokemon_moves[move] = moves_data[move]
            pokemon_objects.append(pokemon.Pokemon.from_dict(row['name'], pokemon_info, pokemon_moves))
    return pokemon_objects

def load_effectiveness(effectiveness_file: str) -> Dict[str, Dict[str, float]]:
    effectiveness = {}
    with open(effectiveness_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            attack_type = row['attacking']
            effectiveness[attack_type] = {defense_type: float(value) for defense_type, value in row.items() if defense_type != 'attacking'}
    return effectiveness

# ------------------ Simulación de combate ------------------
def init_pygame():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Música de Pokemon Red & Blue - Batalla (VS. Entrenador).mp3')
    pygame.mixer.music.play(-1)
    window = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption('PELEA POKEMON')
    return window

def health_bar(window, pokemon, x, y):
    width = 220
    height = 23
    health = pokemon.current_hp / pokemon.max_hp
    pygame.draw.rect(window, (255, 255, 255), (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(window, (236, 59, 25), (x, y, width, height))
    pygame.draw.rect(window, (24, 192, 32), (x, y, width * health, height))

def show_pokemon(window, team1, team2, pokemon, x, y, scale):
    image = pygame.image.load(f'imgs/{pokemon.pokedex_number.zfill(3)}.png')
    image = pygame.transform.scale(image, scale)
    window.blit(image, (x, y))
    if pokemon in team1.pokemons:
        health_bar(window, pokemon, 770, 460)
    else:
        health_bar(window, pokemon, 190, 145)

def events_visualization(window, text):
    font = pygame.font.Font('Windows Regular.ttf', 40)
    text_rendered = font.render(text, 1, (72, 72, 72))
    text_rect = text_rendered.get_rect()
    text_rect.topleft = (50, 768 - 150)
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def line1_right_events_visualization(window, text):
    font = pygame.font.Font('PressStart2P.ttf', 10)
    text_rendered = font.render(text, 1, (72, 72, 72))
    text_rect = text_rendered.get_rect()
    text_rect.right = 1024 - 55
    text_rect.bottom = 768 - 130
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def line2_right_events_visualization(window, text):
    font = pygame.font.Font('PressStart2P.ttf', 10)
    text_rendered = font.render(text, 1, (72, 72, 72))
    text_rect = text_rendered.get_rect()
    text_rect.right = 1024 - 55
    text_rect.bottom = 768 - 100
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def special_events_visualization(window, text, x, y, scale, selected_font):
    if selected_font == 1:
        font = pygame.font.Font('PressStart2P.ttf', scale)
    elif selected_font == 2:
        font = pygame.font.Font('Windows Regular.ttf', scale)
    text_rendered = font.render(text, True, (72, 72, 72))
    text_rect = text_rendered.get_rect()
    text_rect.topleft = (x, y)
    window.blit(text_rendered, text_rect)
    pygame.display.flip()

def defeated_pokemon_counter(team):
    counter = 0
    for pokemon in team.pokemons:
        if pokemon.current_hp <= 0:
            counter += 1
    return counter

def sample_of_defeated_pokemons(window, team1, team2):
    defeated_team1 = defeated_pokemon_counter(team1)
    defeated_team2 = defeated_pokemon_counter(team2)
    line1_right_events_visualization(window, f'Jugador: {defeated_team1} pokemones derrotados')
    line2_right_events_visualization(window, f'{team2.name}: {defeated_team2} pokemones derrotados')
    pygame.display.flip()

def fight_simulation_visualization(window, team1, team2, effectiveness):
    events_visualization(window, f'¡{team2.name} quiere luchar!')
    pygame.time.wait(2000)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        sample_of_defeated_pokemons(window, team1, team2)
        pygame.display.flip()
        clock.tick(60)
        winner = get_winner(window, team1, team2, effectiveness)
        pygame.time.wait(2000)
        if not running:
            break
    return team1 if any(pokemon.current_hp > 0 for pokemon in team1.pokemons) else team2

def show_winner(window, team):
    window.fill((0, 0, 0))
    winner_screen_font = pygame.font.Font('PressStart2P.ttf', 36)
    winner_screen_text = winner_screen_font.render(f'¡{team.name} ha sido el vencedor!', 1, (255, 255, 255))
    winner_screen_text_rect = winner_screen_text.get_rect(center=(1024 // 2, 768 // 2))
    window.blit(winner_screen_text, winner_screen_text_rect)
    pygame.display.flip()
    pygame.time.delay(5000)

def battle(best_team, rival):
    window = init_pygame()
    pokemons_data = define_pokemons_objects()
    effectiveness = load_effectiveness('effectiveness_chart.csv')
    if rival == 1:
        Will = Team('Will', [
            pokemons_data[436], pokemons_data[123], pokemons_data[325], pokemons_data[79], pokemons_data[281], pokemons_data[177]
        ])
        winner = fight_simulation_visualization(window, best_team, Will, effectiveness)
        show_winner(window, winner)
    elif rival == 2:
        Koga = Team('Koga', [
            pokemons_data[435], pokemons_data[454], pokemons_data[317], pokemons_data[49], pokemons_data[89], pokemons_data[169]
        ])
        winner = fight_simulation_visualization(window, best_team, Koga, effectiveness)
        show_winner(window, winner)
    elif rival == 3:
        Bruno = Team('Bruno', [
            pokemons_data[237], pokemons_data[106], pokemons_data[297], pokemons_data[68], pokemons_data[448], pokemons_data[107]
        ])
        winner = fight_simulation_visualization(window, best_team, Bruno, effectiveness)
        show_winner(window, winner)
    elif rival == 4:
        Karen = Team('Karen', [
            pokemons_data[461], pokemons_data[442], pokemons_data[430], pokemons_data[197], pokemons_data[229], pokemons_data[359]
        ])
        winner = fight_simulation_visualization(window, best_team, Karen, effectiveness)
        show_winner(window, winner)
    else:
        Lance = Team('Lance', [
            pokemons_data[373], pokemons_data[445], pokemons_data[149], pokemons_data[6], pokemons_data[334], pokemons_data[130]
        ])
        winner = fight_simulation_visualization(window, best_team, Lance, effectiveness)
        show_winner(window, winner)
    pygame.quit()

def __faint_change__(window, team1, team2, effectiveness):
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

def __fight__(window, team1, team2, effectiveness):
    turn = 0
    running = True
    while running and any(pokemon.current_hp > 0 for pokemon in team1.pokemons) and any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        action_1, target_1 = team1.get_next_action(team2, effectiveness)
        action_2, target_2 = team2.get_next_action(team1, effectiveness)
        window.blit(pygame.transform.scale(pygame.image.load('Fondo.jpg'), (1024, 768)), (0, 0))
        if action_1 == 'switch':
            first = team1
            second = team2
        elif action_2 == 'switch':
            first = team2
            second = team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1
        elif team1.get_current_pokemon().speed > team2.get_current_pokemon().speed:
            first = team1
            second = team2
        else:
            first = team2
            second = team1
            action_1, target_1, action_2, target_2 = action_2, target_2, action_1, target_1

        first.do_action(action_1, target_1, second, effectiveness)
        if action_1 == 'attack':
            print(f'{first.get_current_pokemon().name} usó {target_1.name}!')
            events_visualization(window, f'{first.get_current_pokemon().name} usó {target_1.name}!')
        pokemon1 = team1.get_current_pokemon()
        health_bar(window, pokemon1, 770, 460)
        pygame.display.flip()

        if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
            __faint_change__(window, team1, team2, effectiveness)
        else:
            if action_2 == 'attack' and target_2 is None:
                action_2, target_2 = second.get_next_action(first, effectiveness)
            second.do_action(action_2, target_2, first, effectiveness)
            if action_2 == 'attack':
                print(f'{second.get_current_pokemon().name} usó {target_2.name}!')
                events_visualization(window, f'{second.get_current_pokemon().name} usó {target_2.name}!')
            pokemon2 = team2.get_current_pokemon()
            health_bar(window, pokemon2, 190, 145)
            pygame.display.flip()

            if team1.get_current_pokemon().current_hp == 0 or team2.get_current_pokemon().current_hp == 0:
                __faint_change__(window, team1, team2, effectiveness)

        pokemon2 = team2.get_current_pokemon()
        if pokemon2.current_hp <= 0:
            print(f'{pokemon2.name} se debilitó...')
            events_visualization(window, f'{pokemon2.name} se debilitó...')
            if len(team2.pokemons) == 0:
                pygame.time.delay(5000)

            elif pokemon1.current_hp <= 0:
                print(f'{pokemon1.name} se debilitó...')
                if len(team1.pokemons) == 0:
                    pygame.time.delay(5000)

        if not any(pokemon.current_hp > 0 for pokemon in team1.pokemons):
            print(f'¡{team2.name} ha ganado!')
            events_visualization(window, f'¡{team2.name} ha ganado!')
            break
        elif not any(pokemon.current_hp > 0 for pokemon in team2.pokemons):
            print(f'¡{team1.name} ha ganado!')
            events_visualization(window, f'¡{team1.name} ha ganado!')
            break
        else:
            if team1.pokemons:
                special_events_visualization(window, f'{team1.get_current_pokemon().name}', 613, 408, 45, 2)
            if team2.pokemons:
                special_events_visualization(window, f'{team2.get_current_pokemon().name}', 18, 92, 45, 2)

        if team1.pokemons:
            show_pokemon(window, team1, team2, team1.get_current_pokemon(), 120, 310, (250, 250))
        if team2.pokemons:
            show_pokemon(window, team1, team2, team2.get_current_pokemon(), 670, 120, (250, 250))

        pygame.display.flip()
        turn += 1
        pygame.time.wait(2000)
    
    return team1 if any(pokemon.current_hp > 0 for pokemon in team1.pokemons) else team2

def get_winner(window, team1, team2, effectiveness):
    team1_starter_pokemon = team1.current_pokemon_index
    team2_starter_pokemon = team2.current_pokemon_index
    winner = __fight__(window, team1, team2, effectiveness)
    for pokemon in team1.pokemons:
        pokemon.current_hp = pokemon.max_hp
    for pokemon in team2.pokemons:
        pokemon.current_hp = pokemon.max_hp
    team1.current_pokemon_index = team1_starter_pokemon
    team2.current_pokemon_index = team2_starter_pokemon
    return winner
