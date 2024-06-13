import team_gen as gen
import utils.combat as combat
import csv 
#Variables necesarias

def read_effectiveness_chart(csv_file):
    effectiveness_chart = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            attack_type = row['attacking']
            effectiveness_values = {
                'normal': float(row['normal']),
                'fire': float(row['fire']),
                'water': float(row['water']),
                'electric': float(row['electric']),
                'grass': float(row['grass']),
                'ice': float(row['ice']),
                'fighting': float(row['fighting']),
                'poison': float(row['poison']),
                'ground': float(row['ground']),
                'flying': float(row['flying']),
                'psychic': float(row['psychic']),
                'bug': float(row['bug']),
                'rock': float(row['rock']),
                'ghost': float(row['ghost']),
                'dragon': float(row['dragon']),
                'dark': float(row['dark']),
                'steel': float(row['steel']),
                'fairy': float(row['fairy'])
            }
            effectiveness_chart[attack_type] = effectiveness_values
    return effectiveness_chart


def fights(number_of_teams: int, number_of_rivals: int):
    effectiveness_chart = read_effectiveness_chart('effectiveness_chart.csv')
    teams = gen.create_teams(number_of_teams)
    rivals = gen.create_teams(number_of_rivals)
    wins_per_team = {}
    for team in teams:
        wins = 0
        for encounter in rivals:
            winner = combat.get_winner(team, encounter, effectiveness_chart) #Un sistema bastante simple, toma el ganador y le suma 1.
            if winner == team:
                wins +=1
        wins_per_team[team] = wins
    ordered_wins = list(wins_per_team.values())
    reversed_dicc = {}
    for key in wins_per_team.keys():
        reversed_dicc[wins_per_team[key]] = key
    ordered_wins.sort(reverse=True)
    final_dicc = {}
    for num in ordered_wins:
        final_dicc[reversed_dicc[num]] = num
    return final_dicc

print(fights(50, 400))