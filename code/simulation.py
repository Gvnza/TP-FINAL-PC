from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects
from team_battle import fights, read_effectiveness_chart
import time
import random
def main():
    average_list = []
    epocas_de_cambio = []
    tiempo_inicial = time.time()
    effect = read_effectiveness_chart('effectiveness_chart.csv')
    pokemon_objects = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams(400, pokemon_objects)
    resulsts, average = fights(teams, rivals, 0) 
    average_list.append(average)
    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
    tiempo1 = time.time()
    minutos = (tiempo1-tiempo_inicial)//60
    print(f'La época 0 tardo {minutos} minuto(s) y {round(tiempo1-tiempo_inicial-minutos*60)} segundo(s)')
    print('-'*70)
    for i in range(1, 51):
        tiempo = time.time()
        resulsts, average = fights(mutated_teams, rivals, i)
        average_list.append(average)
        previous_averages = (sum(average_list[i-3:i])/3)
        if previous_averages + 5 >= average >= previous_averages - 5:
            if random.random() >= 0.45 and i / 5 == i // 5:
                    print('CAMBIO A LOS RIVALES!\nCambios: Mutan 50, 50 se cruzan con los equipos de su época. Se mantienen 300.')
                    rivals = improve_rivals(rivals, resulsts, pokemon_objects, effect)
                    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
                    epocas_de_cambio.append(i)
        else:
            mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
        tiempo1 = time.time()
        minutos = (tiempo1-tiempo)//60
        print(f'La época {i} tardo {minutos} minuto(s) y {round(tiempo1-tiempo-minutos*60)} segundo(s).')
        print('-'*70)
    tiempo_final = time.time()
    minutos = (tiempo_final - tiempo_inicial)//60
    print(f'La simulacion tardó {minutos} minuto(s) y {round(tiempo_final-tiempo_inicial-minutos*60)} segundo(s).')
    return mutated_teams
main()