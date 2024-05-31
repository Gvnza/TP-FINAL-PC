import team_gen
import utils.combat
import csv 
import utils.team
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


def fights():
    effectiveness_chart = read_effectiveness_chart('effectiveness_chart.csv')
    teams = team_gen.create_teams(50)
    rivals = team_gen.create_teams(400)
    wins_per_team = {}
    for i, team in enumerate(teams, start=1):
        wins = 0
        for encounter in rivals:
            winner = utils.combat.get_winner(team, encounter, effectiveness_chart) #Un sistema bastante simple, toma el ganador y le suma 1.
            if winner == team:
                wins +=1
        wins_per_team[f'Equipo {i}'] = wins
    ordered_wins = list(wins_per_team.values())
    reversed_dicc = {}
    for key in wins_per_team.keys():
        reversed_dicc[wins_per_team[key]] = key
    ordered_wins.sort(reverse=True)
    final_dicc = {}
    for num in ordered_wins:
        final_dicc[reversed_dicc[num]] = num
    return final_dicc #Nota: Organizar el diccionario

print(fights())