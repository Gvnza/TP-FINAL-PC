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

    r1 = random.choices(population = keys, weights = values)[0]
    r2 = random.choices(population = keys, weights = values)[0]
    while r2 == r1:
        r2 = random.choices(population = keys, weights = values)[0]
    return r1, r2

def crossing(teams, number, objects):
    effectiveness_chart = team_battle.read_effectiveness_chart('effectiveness_chart.csv')
    mutated_teams = []
    for i in range(number):
        team_1, team_2 = parents_selection(teams)
        winner = get_winner(team_1, team_2, effectiveness_chart)
        teams_pokemons_1 = team_1.pokemons
        teams_pokemons_2 = team_2.pokemons
        if teams_pokemons_1 != winner:
            mutation = random.random()
            if mutation < 0.003:
                mutated = random.choice(objects)
                while mutated in teams_pokemons_1:
                    mutated = random.choice(objects)
        mutated_teams.append(change_teams(teams_pokemons_1, teams_pokemons_2, i, winner.pokemons))
    return mutated_teams

def improve_rivals(rivals, teams, objects):
    first_200 = rivals[200:]
    rivals.remove(rivals[300:])
    random_100 = gen.create_teams(100, objects)
    mutated_100 = []
    for i in range(100):
        rival = random.choice(rivals)
        random_team = random.choice(teams)
        winner = get_winner(rival, random_team)
        if random_team == rival:
            mutated_100.append(Team(f'Equipo: {i}', rival, 0))
        else:
            mutated_100.append(change_teams(rival.pokemons, random_team.pokemons, i, winner.pokemons))
    return [first_200, mutated_100, random_100]

def change_teams(team_1: list, team_2: list, i: int, winner: list):
    team_set = set(team_1 + team_2)
    set_list = list(team_set)
    x = 0
    final_team = []
    while len(final_team) < 6 and len(set_list) > 0:
        if random.random() < 0.75:
            selected_team = winner
        else:
            selected_team = team_2 if winner == team_1 else team_1
            not_selected = team_2 if winner == team_2 else team_1
        chosen_pokemon = selected_team[x]
        if chosen_pokemon in set_list and chosen_pokemon not in final_team:
            final_team.append(chosen_pokemon)
            set_list.remove(chosen_pokemon)
            x += 1
        else:
            chosen_pokemon = not_selected[x]
            if chosen_pokemon in set_list and chosen_pokemon not in final_team:
                final_team.append(chosen_pokemon)
                set_list.remove(chosen_pokemon)
                x += 1
    return Team(f'Equipo {i}', final_team, 0)