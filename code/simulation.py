from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects, create_teams_with_legendaries
from team_battle import fights
import situationalGraphs
import standardGraphs as sg
import time
import random
from termcolor import cprint

def main():
    average_list = []
    rivals_results_list = []
    key_epochs = []
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
    for i in range(1, 3):
        epoch_begg = time.time()
        resulsts, average, rivals_results, best_result = fights(mutated_teams, rivals, i)
        best_result_list.append(best_result)
        average_list.append(average)
        rivals_results_list.append(list(rivals_results.values())[0])

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

    # Presenta las opciones
    print('----------------------------------------------------------------------')
    print('OPCIONES:')
    option = 0
    option_list = [1, 2, 3]
    while int(option) not in option_list:
        option = int(input('[1] Gráficos\n[2] Pelea final\n[3] Salir'))
        if option == 1:
            graphics = -1
            while graphics != 0:
                graphics = int(input('[0] Regresar\n[1] Diversidad de Pokémon en los Equipos por Época\n[2] Evolución de la Aptitud a lo largo de las Épocas\n[3] Distribución de Pokémon en los Equipos en la última Época\n[4] Distribución de Tipos de Pokémon en los Equipos en la última Época\n[5] Distribución de Tipos de Pokémon en los Equipos por Época\n[6] Estadísticas del mejor equipo encontrado\n[7] Mejor equipo encontrado\n[8] Promedio de Victorias de equipos y rivales por Época\n[9] Tiempo por Época\n[10] Victorias por Época del mejor equipo\n[11] Gráfico de Gauss\n'))

                if graphics == 1:
                    sg.pokemon_diversity(all_teams)

                elif graphics == 2:
                    sg.fitness_evolution(best_result_list)

                elif graphics == 3:
                    sg.pokemon_distribution(mutated_teams)

                elif graphics == 4:
                    sg.second_pokemon_type_distribution(mutated_teams)

                elif graphics == 5:
                    sg.pokemon_type_distribution(all_teams)

                elif graphics == 6:
                    sg.radar_chart(best_result)

                if graphics == 7:
                    best_teams = mutated_teams[-1][0]['best_pokemon']['identifiers']
                    sg.show_best_team(best_teams)

                elif graphics == 8:
                    average_list = []
                    result_list = []

                    for epoch in mutated_teams:
                        average_list.append(epoch['average_wins'])
                        result_list.append(epoch['average_opponent_wins'])

                    sg.average_wins(average_list, result_list)

                elif graphics == 9:
                    time_per_epoch = []
                    for epoch in mutated_teams:
                        time_per_epoch.append(epoch['time'])
                    sg.time_per_epoch(time_per_epoch)
                
                elif graphics == 10:
                    best_teams = []
                    for epoch in mutated_teams:
                        best_teams.append(epoch[0]['best_pokemon']['identifiers'])
                    sg.best_teams_wins(best_teams)

                elif graphics == 11:
                    sg.gauss()

        elif option == 2:
            return key_epochs, end_time, time_per_epoch, average_list
        else:
            return key_epochs, end_time, time_per_epoch, average_list

    return key_epochs, end_time, time_per_epoch, average_list

if __name__ == '__main__':
    main()