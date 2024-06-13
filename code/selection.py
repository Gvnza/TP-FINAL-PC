import random
import team_battle
import utils.pokemon as pokemon
def selection(number_of_teams, number_of_battles):
    winsperteam = team_battle.fights(number_of_teams, number_of_battles)
    total_wins = sum(list(winsperteam.values()))
    probability = {}
    for key in winsperteam.keys():
        probability[key] = int(winsperteam[key])/total_wins

    keys = list(probability.keys())
    values = list(probability.values())
    r1 = random.choices(population= keys, weights=values)[0]
    r2 = random.choices(population= keys, weights=values)[0]
    
selection(50, 400)