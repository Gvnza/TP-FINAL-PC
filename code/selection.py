import random
import team_battle
from utils.pokemon import Pokemon
from utils.team import Team
from utils.combat import get_winner
import team_gen as gen

def parents_selection(teams):
    total_wins = sum(list(teams.values()))
    
    probability = {}
    for key in teams.keys():
        probability[key] = int(teams[key])/total_wins
    keys = list(probability.keys())
    values = list(probability.values())

    random_team_1 = random.choices(population = keys, weights = values)[0]
    random_team_2 = random.choices(population = keys, weights = values)[0]

    while random_team_2 == random_team_1:
        random_team_2 = random.choices(population = keys, weights = values)[0]
    return random_team_1, random_team_2

def crossing(teams, number, objects):
    mutation_counter = 0
    effectiveness_chart = team_battle.read_effectiveness_chart('effectiveness_chart.csv')
    mutated_teams = []

    for i in range(number):
        team_1, team_2 = parents_selection(teams)
        winner = get_winner(team_1, team_2, effectiveness_chart)
        loser = team_2 if team_1 == winner else team_1

        teams_pokemons_1 = team_1.pokemons
        teams_pokemons_2 = team_2.pokemons
        
        for _ in loser.pokemons:
            if random.random() < 0.003:
                pokemon_mutation = random.choice(objects)
                while pokemon_mutation in loser.pokemons:
                    pokemon_mutation = random.choice(objects)

                teams_pokemons_1.remove(random.choice(teams_pokemons_1))
                teams_pokemons_1.append(pokemon_mutation)
                mutation_counter += 1

        mutated_teams.append(mutate_teams(teams_pokemons_1, teams_pokemons_2, i, winner.pokemons))

    if mutation_counter > 0:
        print(f'Han habido {mutation_counter} mutacione(s) pokemon!')

    return mutated_teams

def improve_rivals(rivals, objects):
    first_350_rivals = rivals[:350]
    random_50_rivals = gen.create_teams(50, objects)

    final_list = []
    for w in range(50):

        final_list.append(random_50_rivals[w])
        
        for q in range(7):
            final_list.append(first_350_rivals[q*50:50 + q*50][w])
    
    return final_list

def mutate_teams(team_1: list, team_2: list, i: int, winner: list):
    team_set = set(team_1 + team_2)
    set_list = list(team_set)
    set_names = []
    
    for poke in set_list:
        set_names.append(poke.name)
    
    x = 0
    final_team = []
    final_team_names = []
    
    while len(final_team) < 6 and len(set_list) > 0:
        if random.random() < 0.75:
            selected_team = winner
        else:
            selected_team = team_2 if winner == team_1 else team_1
    
        chosen_pokemon = selected_team[x]
        if chosen_pokemon.name in set_names and chosen_pokemon.name not in final_team_names:
            set_names.remove(chosen_pokemon.name)
            set_list.remove(chosen_pokemon)

            final_team.append(chosen_pokemon)
            final_team_names.append(chosen_pokemon.name)
            x += 1

    return Team(f'Equipo {i}', final_team, 0)