import team_gen
import utils.combat
import csv
from typing import List, Dict
#Variables necesarias

def read_effectiveness_chart(csv_file):
    effectiveness_chart = {}
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  #Ignorar la primera fila
        for row in reader:
            attack_type = row[0]  #Primer elemento -> El tipo del ataque
            effectiveness_values = row[1:]  #El resto -> Valores de efectividad
            effectiveness_chart[attack_type] = effectiveness_values
    return effectiveness_chart

csv_file = 'effectiveness_chart.csv'
effectiveness_chart = read_effectiveness_chart(csv_file)

first_teams = team_gen.team_generator(50)
fixed_teams = team_gen.no_duplicates(first_teams)
encounters = team_gen.generate_encounters()

def fights(teams, encounters):
    wins_per_team = {}
    for team in teams:
        wins = 0
        for encounter in encounters:
            winner = utils.combat.__fight__(team, encounter, effectiveness_chart)
            if winner == team:
                wins +=1
        wins_per_team[team] = wins
    wins_per_team.sort()
    return wins_per_team

print(fights(fixed_teams, encounters))