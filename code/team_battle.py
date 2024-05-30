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

teams = team_gen.create_teams(50)
rivals = team_gen.create_teams(400)

def fights(teams, rivals):
    wins_per_team = {}
    for team in teams:
        wins = 0
        for encounter in rivals:
            winner = utils.combat.get_winner(team, encounter, effectiveness_chart) #Un sistema bastante simple, toma el ganador y le suma 1.
            if winner == team:
                wins +=1
        wins_per_team[team] = wins
    return wins_per_team #Nota: Organizar el diccionario

print(fights(teams, rivals))