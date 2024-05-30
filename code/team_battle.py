import team_gen
import utils.combat
import csv 
#Variables necesarias

def read_effectiveness_chart(csv_file):
    effectiveness_chart = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            attack_type = row['attacking']  
            effectiveness_values = {
                'normal': row['normal'],
                'fire': row['fire'],
                'water': row['water'],
                'electric': row['electric'],
                'grass': row['grass'],
                'ice': row['ice'],
                'fighting': row['fighting'],
                'poison': row['poison'],
                'ground': row['ground'],
                'flying': row['flying'],
                'psychic': row['psychic'],
                'bug': row['bug'],
                'rock': row['rock'],
                'ghost': row['ghost'],
                'dragon': row['dragon'],
                'dark': row['dark'],
                'steel': row['steel'],
                'fairy': row['fairy']
            }
            effectiveness_chart[attack_type] = effectiveness_values
    return effectiveness_chart


def fights():
    effectiveness_chart = read_effectiveness_chart('effectiveness_chart.csv')
    teams = team_gen.create_teams(50)
    rivals = team_gen.create_teams(400)
    wins_per_team = {}
    for team in teams:
        wins = 0
        for encounter in rivals:
            winner = utils.combat.get_winner(team, encounter, effectiveness_chart) #Un sistema bastante simple, toma el ganador y le suma 1.
            if winner == team:
                wins +=1
        wins_per_team[team] = wins
    return wins_per_team #Nota: Organizar el diccionario

print(fights())