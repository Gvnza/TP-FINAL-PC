import matplotlib as plt
import team_gen as tg

def thousand_simulations():
    mutations_cuantity_list = []
    for _ in range(1000):
        pokemon_objects = tg.define_pokemons_objects()
        worst_Team = tg.create_teams(1, pokemon_objects)
        for pokemon in worst_Team.pokemons:
            pokemon.level = 1
        