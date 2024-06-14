from selection import crossing
from team_gen import create_teams, define_pokemons_objects
from team_battle import fights

def main():
    pokemon_objects = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams(400, pokemon_objects)
    resulsts = fights(teams, rivals, 0)
    mutated_teams = crossing(resulsts)
    for i in range(1, 3):
        resulsts = fights(mutated_teams, rivals, i)
        mutated_teams = crossing(resulsts)
    return mutated_teams
main()