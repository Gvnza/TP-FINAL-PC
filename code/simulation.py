from selection import crossing, improve_rivals, improve_stats
from team_gen import create_teams, define_pokemons_objects, define_pokemons_objects_with_legendaries, create_teams_with_legendaries
from team_battle import fights
import time
import random
from termcolor import cprint

def main():
    average_list = []
    key_epochs = []
    stats_improvement_epochs = []
    time_per_epoch = {}
    init_time = time.time()
    counter = 0
    #Recoleccion de datos, medianamente irrelevante.

    pokemon_objects, legendaries = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams_with_legendaries(400, pokemon_objects, legendaries)
    #Inicializacion de los rivales y los equipos.
    print('-'*70)
    resulsts, average, rivals_results = fights(teams, rivals, 0) 
    average_list.append(average)
    #Los resultados de las batallas
    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
    #Mutar

    tiempo1 = time.time()
    minutes = (tiempo1 - init_time)//60
    print(f'La época 0 tardo {minutes:.0f} minuto(s) y {tiempo1 - init_time - minutes*60:.0f} segundo(s)')
    print('-'*70)
    time_per_epoch[0] = tiempo1 - init_time
    #Basicamente, muestra de datos y recoleccion.

    for i in range(1, 51):
        epoch_begg = time.time()

        resulsts, average, rivals_results = fights(mutated_teams, rivals, i)
        average_list.append(average)
        #Por ahora, lo mismo que el proceso de la epoca 0.
        previous_averages = (sum(average_list[i-3:i])/3)
        #Proceso de mejora de los rivales
        if previous_averages + 7 >= average >= previous_averages - 7:
            if random.random() >= 0.45:
                if 10 >= counter and average >= 335:
                    rivals = improve_stats(rivals)
                    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
                    stats_improvement_epochs.append(i)
                    cprint('ALERTA! Los rivales han aumentado sus pokestats!', 'red')
                    counter += 1
                else:
                    rivals = improve_rivals(pokemon_objects, legendaries, rivals_results)
                    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
                    cprint('ALERTA! Los rivales han pokemutado!', 'red')
                    key_epochs.append(i)
                #Se mejoran, se muestra un aviso en la terminal y se guarda el dato 
            else:
                mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
        else:
            mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))

        epoch_end = time.time()
        minutes = (epoch_end - epoch_begg)//60
        print(f'La época {i} tardo {minutes:.0f} minuto(s) y {epoch_end - epoch_begg - minutes*60:.0f} segundo(s).')
        cprint('-'*70)
        time_per_epoch[i] = epoch_end - epoch_begg
        #Datos...

    end_time = time.time()
    minutes = (end_time - init_time)//60
    print(f'La simulacion tardó {minutes:.0f} minuto(s) y {end_time - init_time - minutes*60:.0f} segundo(s).')
    #Mas datos 
    print("+-----+-----+")
    print("| Epc | Win |")
    print("+-----+-----+")
    for i in range(50):
        if i < 10:
            print("| ", i, "  |", " ", average_list[i], "  |")
            print("+-----+-----+")
        else:
            print("| ", i, " |", " ", average_list[i], "  |")
            print("+-----+-----+")
    return key_epochs, end_time, time_per_epoch, average_list

if __name__ == '__main__':
    main()


