from selection import crossing
from team_gen import create_teams, define_pokemons_objects
from team_battle import fights

def main():
    pokemon_objects = define_pokemons_objects()
    teams = create_teams(50, pokemon_objects)
    rivals = create_teams(400, pokemon_objects)
    resulsts = fights(teams, rivals)
    mutated_teams = crossing(resulsts)
    print(fights(mutated_teams, rivals))

main()