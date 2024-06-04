import random
import team_combat


def get_teams(number_of_teams: int, number_of_fights):
    teams = team_combat.fights(number_of_teams, number_of_fights)
    return teams

def get_probabilities(teams):
    total_wins = sum(list(teams.values()))
    probability = {}
    for team in teams.keys():
        probability[str(team)] = int(teams[team])/total_wins
    

get_probabilities(get_teams(10, 100))