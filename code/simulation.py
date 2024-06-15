from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects
from team_battle import fights, read_effectiveness_chart
import time
import random

def main():
    average_list = []
    key_epochs = []
    time_per_epoch = {}
    init_time = time.time()
    #Recoleccion de datos, medianamente irrelevante.

    pokemon_objects = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams(400, pokemon_objects)
    #Inicializacion de los rivales y los equipos.
    resulsts, average = fights(teams, rivals, 0) 
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

        resulsts, average = fights(mutated_teams, rivals, i)
        average_list.append(average)
        #Por ahora, lo mismo que el proceso de la epoca 0.
        previous_averages = (sum(average_list[i-3:i])/3)
        if previous_averages + 5 >= average >= previous_averages - 5:
            if random.random() >= 0.45:
                    rivals = improve_rivals(rivals, pokemon_objects)
                    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
                    key_epochs.append(i)
                    print('ALERTA! Los rivales han mejorado!')
            else:
                mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
        else:
            mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))

        epoch_end = time.time()
        minutes = (epoch_end - epoch_begg)//60
        print(f'La época {i} tardo {minutes:.0f} minuto(s) y {epoch_end - epoch_begg - minutes*60:.0f} segundo(s).')
        print('-'*70)
        time_per_epoch[i] = epoch_end - epoch_begg
    
    end_time = time.time()
    minutes = (end_time - init_time)//60
    print(f'La simulacion tardó {minutes:.0f} minuto(s) y {end_time - init_time - minutes*60:.0f} segundo(s).')
    
    return key_epochs, end_time, time_per_epoch, average_list

if __name__ == '__main__':
    main()