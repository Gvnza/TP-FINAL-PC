from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects, create_teams_with_legendaries
from team_battle import fights
from situationalGraphs import gauss
import standardGraphs as sg
import time
import random
from termcolor import cprint
from exit_csv import epochs_csv, best, dicc_pokemons_epochs
def main():
    average_list = []
    rivals_best_results = []
    all_teams = []
    best_result_list = []
    stats_improvement_epochs = []
    time_per_epoch = []
    init_time = time.time()
    counter = 0
    #Recoleccion de datos, medianamente irrelevante.

    pokemon_objects, legendaries = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    all_teams.append(teams)
    rivals = create_teams_with_legendaries(400, pokemon_objects, legendaries)
    #Inicializacion de los rivales y los equipos.
    print('-'*70)
    resulsts, average, rivals_results, best_result = fights(teams, rivals, 0) 
    
    best_result_list.append(best_result)
    average_list.append(average)
    rivals_best_results.append(list(rivals_results.values())[0])
    #Los resultados de las batallas
    mutated_teams = crossing(resulsts, 50, pokemon_objects)
    #Mutar
    tiempo1 = time.time()
    minutes = (tiempo1 - init_time)//60
    print(f'La época 0 tardo {minutes:.0f} minuto(s) y {tiempo1 - init_time - minutes*60:.0f} segundo(s)')
    print('-'*70)
    time_per_epoch.append(tiempo1 - init_time)
    #Basicamente, muestra de datos y recoleccion.
    for i in range(1, 2):
        epoch_begg = time.time()
        resulsts, average, rivals_results, best_result = fights(mutated_teams, rivals, i)
        best_result_list.append(best_result)
        average_list.append(average)
        rivals_best_results.append(list(rivals_results.values())[0])

        if 15 >= counter and average >= 350 and i-1 not in stats_improvement_epochs:
            rivals = improve_rivals(rivals_results)

            mutated_teams = crossing(resulsts, 50, pokemon_objects)
            all_teams.append(mutated_teams)
            
            stats_improvement_epochs.append(i)
            cprint('ALERTA! Los rivales han aumentado sus pokestats!', 'red')
            counter += 1

        else:
            mutated_teams = crossing(resulsts, 50, pokemon_objects)
            all_teams.append(mutated_teams)

        epoch_end = time.time()
        minutes = (epoch_end - epoch_begg)//60
        print(f'La época {i} tardo {minutes:.0f} minuto(s) y {epoch_end - epoch_begg - minutes*60:.0f} segundo(s).')
        cprint('-'*70)
        time_per_epoch.append(tiempo1 - init_time)
        #Datos...

    end_time = time.time()
    minutes = (end_time - init_time)//60
    print(f'La simulacion tardó {minutes:.0f} minuto(s) y {end_time - init_time - minutes*60:.0f} segundo(s).')

    #Diversidad
    #Funciona pero nombres
    sg.pokemon_diversity(all_teams)

    #Funciona pero nombres?
    sg.pokemon_distribution(mutated_teams)

    #Funciona medio extraño
    sg.second_pokemon_type_distribution(mutated_teams)
    sg.pokemon_type_distribution(all_teams)
    
    #Tiempo
    sg.time_per_epoch(time_per_epoch)

    #Resultados
    sg.average_wins(average_list)
    sg.best_teams_wins(best_result_list, rivals_best_results)
    
    #Mejores equipos
    sg.show_best_team(list(resulsts.keys())[0])
    sg.radar_chart(list(resulsts.keys())[0])

    #Stats
    gauss()
        
    #CSV
    pokemon_count = dicc_pokemons_epochs(all_teams)
    epochs_csv(pokemon_count)
    best(best_result_list)

    return best_result_list[-1]