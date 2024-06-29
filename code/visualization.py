import csv
import pygame
from utils.team import Team
import utils.pokemon as pokemon
from typing import Dict, List, Tuple

# Inicialización de pygame y del mezclador de música
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('Música de Pokemon Red & Blue - Batalla (VS. Entrenador).mp3')
pygame.mixer.music.play(-1)


# Configuración de la ventana
width, height = 1024, 768
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('PELEA POKEMON')

# Pq no la haces mas corta y pones todo en donde estaba???
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