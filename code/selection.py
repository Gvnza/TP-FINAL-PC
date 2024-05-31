import random
import team_battle

def selection():
    teams = team_battle.fights(50, 400)
    half = len(teams) // 2
    # Crear un nuevo diccionario con la mitad de elementos (la mitad superior)
    half_teams = {k: teams[k] for k in list(teams)[:half]}
    probability = {}
    for result in half_teams:
        probability[str(result.keys())] = round(int(result.values())/400, 2)
    for number in probability:
        elected1, elected2 = random.choice(probability), random.choice(probability)
        veredict = random.random()
        if float(elected2.values()) > veredict and float(elected1.values()) > veredict:
            elected1.values()[random.randint(0, 6)], elected2.values()[random.randint(0, 6)] 

selection()

