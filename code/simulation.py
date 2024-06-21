from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects, create_teams_with_legendaries
from team_battle import fights
from graphs import standard_graphs
import time
import random
from termcolor import cprint

def main():
    average_list = []
    rivals_results_list = []
    key_epochs = []
    best_result_list = []
    stats_improvement_epochs = []
    time_per_epoch = []
    init_time = time.time()
    counter = 0
    #Recoleccion de datos, medianamente irrelevante.

    pokemon_objects, legendaries = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams_with_legendaries(400, pokemon_objects, legendaries)
    #Inicializacion de los rivales y los equipos.
    print('-'*70)
    resulsts, average, rivals_results, best_result = fights(teams, rivals, 0) 
    
    best_result_list.append(best_result)
    average_list.append(average)
    rivals_results_list.append(list(rivals_results.values())[0])
    #Los resultados de las batallas
    mutated_teams = crossing(resulsts, 50, pokemon_objects)
    #Mutar
    tiempo1 = time.time()
    minutes = (tiempo1 - init_time)//60
    print(f'La época 0 tardo {minutes:.0f} minuto(s) y {tiempo1 - init_time - minutes*60:.0f} segundo(s)')
    print('-'*70)
    time_per_epoch.append(tiempo1 - init_time)
    #Basicamente, muestra de datos y recoleccion.
    for i in range(1, 51):
        epoch_begg = time.time()
        resulsts, average, rivals_results, best_result = fights(mutated_teams, rivals, i)
        best_result_list.append(best_result)
        average_list.append(average)
        rivals_results_list.append(list(rivals_results.values())[0])
        #Por ahora, lo mismo que el proceso de la epoca 0.
        #Proceso de mejora de los rivales
        if 10 >= counter and average >= 350 and i-1 not in stats_improvement_epochs:
            rivals = improve_rivals(rivals_results)
            mutated_teams = crossing(resulsts, 50, pokemon_objects)
            stats_improvement_epochs.append(i)
            cprint('ALERTA! Los rivales han aumentado sus pokestats!', 'red')
            counter += 1
                #Se mejoran, se muestra un aviso en la terminal y se guarda el dato 
        else:
            mutated_teams = crossing(resulsts, 50, pokemon_objects)      

        epoch_end = time.time()
        minutes = (epoch_end - epoch_begg)//60
        print(f'La época {i} tardo {minutes:.0f} minuto(s) y {epoch_end - epoch_begg - minutes*60:.0f} segundo(s).')
        cprint('-'*70)
        time_per_epoch.append(tiempo1 - init_time)

        #Datos...

    end_time = time.time()
    minutes = (end_time - init_time)//60
    print(f'La simulacion tardó {minutes:.0f} minuto(s) y {end_time - init_time - minutes*60:.0f} segundo(s).')

    standard_graphs(average_list, rivals_results_list, time_per_epoch, best_result_list)

    return key_epochs, end_time, time_per_epoch, average_list

if __name__ == '__main__':
    main()

# * Ahora mismo es normal que el progreso del promedio de victorias de los equipos se estanque, mucho antes de llegar a 350 (App 270 y hubieron 4 mutaciones del los rivales)
# * Lean el README, ahi puse un par de ideas.
