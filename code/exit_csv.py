import csv

def dicc_pokemons_epochs(teams):
    list_pokemons = []
    for epoch in teams:
        pokemon_count = {}
        for team in epoch:
            for pokemon in team.pokemons:
                if pokemon.name in list(pokemon_count.keys()):
                    pokemon_count[pokemon.name] += 1
                else:
                    pokemon_count[pokemon.name] = 1
        pokemon_count  = dict(sorted(pokemon_count.items(), key=lambda item: item[1], reverse=True))
        list_pokemons.append(pokemon_count)
    return list_pokemons

def epochs_csv(pokemon_count):
    number = 0
    with open('epochs.csv','w', newline='') as epochs:
        writer = csv.writer(epochs)
        for idx, dictionary in enumerate(pokemon_count, start=1):
            row = [idx]  
            for pokemon, number in dictionary.items():
                row.extend([number, pokemon])
            writer.writerow(row)

def best(best_restuls, results):
    with open('best_teams.csv', 'w', newline='') as best_teams:
        fieldnames = ['epoch', 'aptitude', 'team_name', 'pokemon_1', 'pokemon_2', 'pokemon_3', 'pokemon_4', 'pokemon_5', 'pokemon_6']
        writer = csv.writer(best_teams)
        best_teams.seek(0)
        writer.writerow(fieldnames)
        for idx, team in enumerate(best_restuls, start=1):
            row = [idx]
            team = team
            number = results[idx -1]
            team_pokemons = [pokemon.name for pokemon in team.pokemons]
            row.extend([number, team.name, '0'])
            for pokemon in team_pokemons:
                row.extend([pokemon])
            writer.writerow(row)