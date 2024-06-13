import team_gen as gen
import utils.combat as combat
import csv 

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
            # Se guarda en el diccionario el tipo de ataque con el valor de efectividadd
            effectiveness_chart[attack_type] = effectiveness_values
    return effectiveness_chart


def fights(number_of_teams: int, number_of_rivals: int):
    effectiveness_chart = read_effectiveness_chart('effectiveness_chart.csv')
    # Creación de los equipos y rivales
    teams = gen.create_teams(number_of_teams)
    rivals = gen.create_teams(number_of_rivals)
    wins_per_team = {team: 0 for team in teams}
    for team in teams:
        for encounter in rivals:
            # Se obtiene el ganador de la pelea y se le suma 1 al contador de victorias
<<<<<<< HEAD
            winner = combat.get_winner(team, encounter, effectiveness_chart)
            if winner == team:
                wins +=1
        wins_per_team[team] = wins
    # Ordenamiento del diccionario de victorias por equipo
    ordered_wins = list(wins_per_team.values())
    reversed_dicc = {}
    # Se invierte el diccionario para poder ordenar las victorias
    for key in wins_per_team.keys():
        reversed_dicc[wins_per_team[key]] = key
    ordered_wins.sort(reverse=True)
    final_dicc = {}
    for num in ordered_wins:
        final_dicc[reversed_dicc[num]] = num
    return final_dicc

print(fights(50, 400))
=======
            winner = combat.get_winner(team, encounter, effectiveness_chart) #Un sistema bastante simple, toma el ganador y le suma 1.
            if winner == team:
                wins_per_team[team] += 1
    # Ordenamiento del diccionario de victorias por equipo
    final_dicc = dict(sorted(wins_per_team.items(), key=lambda item: item[1], reverse=True))
    return final_dicc
>>>>>>> 8d731400a3e409cdcc48b76a728c9fa65f3482f4
