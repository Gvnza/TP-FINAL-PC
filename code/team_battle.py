import team_gen as gen
from utils.combat import get_winner
import csv 
from termcolor import cprint


def read_effectiveness_chart(csv_file: str) -> dict:
    effectiveness_chart = {}
    # Abriendo el archivo csv
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Por cada linea del archivo...
        for row in reader:
            # Se guarda el tipo de ataque
            attack_type = row['attacking']
            # Se guarda la efectividad
            effectiveness_values = {
                'normal': float(row['normal']), 'fire': float(row['fire']),
                'water': float(row['water']), 'electric': float(row['electric']),
                'grass': float(row['grass']), 'ice': float(row['ice']),
                'fighting': float(row['fighting']), 'poison': float(row['poison']),
                'ground': float(row['ground']), 'flying': float(row['flying']),
                'psychic': float(row['psychic']), 'bug': float(row['bug']),
                'rock': float(row['rock']), 'ghost': float(row['ghost']),
                'dragon': float(row['dragon']), 'dark': float(row['dark']),
                'steel': float(row['steel']), 'fairy': float(row['fairy'])
            }
            # Se guarda en el diccionario el tipo de ataque con el valor de efectividadd
            effectiveness_chart[attack_type] = effectiveness_values

    return effectiveness_chart


def fights(teams, rivals, epoch):
    effectiveness_chart = read_effectiveness_chart('effectiveness_chart.csv')
    wins_per_team = {team: 0 for team in teams}
    wins_per_rival = {rival: 0 for rival in rivals}
    for team in teams:
        for encounter in rivals:
            # Determina el ganador del combate
            winner = get_winner(team, encounter, effectiveness_chart)
            # Incrementa el contador de victorias si el equipo actual es el ganador
            if winner == team:
                wins_per_team[team] += 1
            else:
                wins_per_rival[encounter] += 1
    
    final_dicc_teams = dict(sorted(wins_per_team.items(), key=lambda item: item[1], reverse=True))

    final_dicc_rivals = dict(sorted(wins_per_rival.items(), key=lambda item: item[1], reverse=True))

    best_team = list(final_dicc_teams.values())[:1]
    
    average_wins = sum(list(final_dicc_teams.values()))/50
    print(f'ÉPOCA: {epoch} \t MEJOR RESULTADO: {best_team[0]} \t PROMEDIO DE VICTORIAS: {sum(list(final_dicc_teams.values()))/50}')
    
    return final_dicc_teams, average_wins, final_dicc_rivals, best_team[0], list(final_dicc_teams.keys())[0]