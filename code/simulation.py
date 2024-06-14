from selection import crossing, improve_rivals
from team_gen import create_teams, define_pokemons_objects
from team_battle import fights
import time

def main():
    tiempo = time.time()
    pokemon_objects = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams(400, pokemon_objects)
    resulsts, average = fights(teams, rivals, 0) 
    mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
    tiempo1 = time.time()
    minutos = (tiempo1-tiempo)//60
    print(f'La época 0 tardo {minutos} minuto(s) y {round(tiempo1-tiempo-minutos*60)} segundo(s)')
    print('-'*10)
    for i in range(1, 51):
        tiempo = time.time()
        resulsts, average = fights(mutated_teams, rivals, i)
        if average >= 350:
            print('CAMBIO DE RIVALES!')
            rivals = improve_rivals(rivals, mutated_teams, pokemon_objects)
            mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
        else:
            mutated_teams = crossing(resulsts, 50, list(pokemon_objects.values()))
        print(f'La época {i} tardo {minutos} minuto(s) y {round(tiempo1-tiempo-minutos*60)} segundo(s)')
        print('-'*20)
        tiempo1 = time.time()
        minutos = (tiempo1-tiempo)//60
    return mutated_teams
main()