import random
import team_battle
from utils.pokemon import Pokemon
from utils.team import Team
from utils.combat import get_winner
import team_gen as gen
from termcolor import cprint


def parents_selection(teams):
    total_wins = sum(list(teams.values()))
    
    probability = {}
    for key in teams.keys():
        probability[key] = int(teams[key])/total_wins
    keys = list(probability.keys())
    values = list(probability.values())
    #Tomo las victorias totales, y saco el % de wins que representa cada equipo (se podría implementar un incremento/decremento dependiendo la posicion)
    random_team_1 = random.choices(population = keys, weights = values)[0]
    random_team_2 = random.choices(population = keys, weights = values)[0]
    #Se eligen dos equipos segun las posibilidades
    while random_team_2 == random_team_1:
        random_team_2 = random.choices(population = keys, weights = values)[0]
        #Me aseguro que no sean dos equipos iguales
    return random_team_1, random_team_2


def crossing(teams, number, objects):
    mutation_counter = 0
    effectiveness_chart = team_battle.read_effectiveness_chart('effectiveness_chart.csv')
    mutated_teams = []
    #Preparación de variables
    for i in range(number):
        team_1, team_2 = parents_selection(teams)
        winner = get_winner(team_1, team_2, effectiveness_chart)
        loser = team_2 if team_1 == winner else team_1

        #Hago pelear a los dos equipos elegidos, y al ganador le doy "privilegios", tambien determino el perdedor
        #Hago una lista con sus pokemones 

        loser_mutated = []
        for j in range(len(loser.pokemons)):
            if random.random() <= 0.003:
                #Por cada pokemon del perdedor hay un 3% de probabilidades de que muten
                pokemon_mutation = random.choice(objects)
                while pokemon_mutation in loser.pokemons:
                    pokemon_mutation = random.choice(objects)
                    #Me aseguro de que no este ya en el equipo
                #Le saco el pokemon que muta
                loser.pokemons[j] = pokemon_mutation
                mutation_counter += 1
            loser_mutated.append(loser.pokemons[j])

        mutated_teams.append(mutate_teams(winner.pokemons, loser_mutated, i))

    if mutation_counter > 0:
        cprint(f'Ha(n) habido {mutation_counter} pokemutacion(es)!', 'yellow')

    return mutated_teams


def improve_rivals(objects, legendaries, results):
    # Se toman los primeros 350 rivales
    first_350_rivals = list(results.keys())[:350]
    # Se crean 50 nuevos rivales para completar los 400
    random_50_rivals = gen.create_teams_with_legendaries(50, objects, legendaries) 
    final_list = []

    for w in range(50):
        
        final_list.append(random_50_rivals[w])
        
        for q in range(7):
            final_list.append(first_350_rivals[q * 50 : 50 + q * 50][w])
    
    return final_list

def improve_stats(rivals):
    for team in rivals:
        for pokemon in team.pokemons:
            pokemon.level += 2
    return rivals

def mutate_teams(winner: list, loser: list, i: int):
    team_set = set(winner + loser)
    set_list = list(team_set)
    set_names = []

    for poke in set_list:
        set_names.append(poke.name)
    
    x = 0
    final_team = []
    final_team_names = []
    
    while len(final_team) < 6 and len(set_list) > 0:
        selected_team = winner if random.random() < 0.7 else loser
        chosen_pokemon = selected_team[x]
        if chosen_pokemon.name in set_names and chosen_pokemon.name not in final_team_names:
            set_names.remove(chosen_pokemon.name)
            set_list.remove(chosen_pokemon)
            
            final_team.append(chosen_pokemon)
            final_team_names.append(chosen_pokemon.name)
            x += 1

    return Team(f'Equipo {i}', final_team, 0)