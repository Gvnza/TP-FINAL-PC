import random
import team_battle
from utils.pokemon import Pokemon
from utils.team import Team
from utils.combat import get_winner
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

def crossing(number_of_teams:int , number_of_rivals: int):
    effectiveness_chart = team_battle.read_effectiveness_chart('effectiveness_chart.csv')
    teams = team_battle.fights(number_of_teams, number_of_rivals)
    mutated_teams = []
    for i in range(number_of_teams):
        team = []
        team_1, team_2 = parents_selection(teams)
        winner = get_winner(team_1, team_2, effectiveness_chart)
        for j in range(6):
            pokemon_1 = Team.pokemons(team_1)[j]
            pokemon_2 = Team.pokemons(team_2)[j]
            if pokemon_1 in team or pokemon_2 in team:
                    team.append(pokemon_2) if pokemon_1 in team else team.append(pokemon_1)
            if not pokemon_1 == pokemon_2:
                r = random.random()
                if winner == team_1:
                    team.append(pokemon_1) if r > 0.25 else team.append(pokemon_2)
                else:
                    team.append(pokemon_2) if r > 0.25 else team.append(pokemon_1)
            else:
                team.append(pokemon_1)
        mutated_teams.append(Team(f'Equipo {i}', team, 0))
    return mutated_teams

print(crossing(50, 400))

